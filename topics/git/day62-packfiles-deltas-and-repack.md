# Day 62, Task 8 -- Git: loose objects vs. packfiles, delta chains, `verify-pack`, `count-objects`, and `repack`

## THE TASK

In a SCRATCH repo (`/tmp/day62-lab`, `git init -b main`), find out how Git actually stores objects on disk and when it compresses them as deltas. Never run any of this against a real repository you care about (and never `git gc --prune=now` there). Keep all config repo-local or one-off with `git -c ...`. Answer the questions by actually running the commands.

1. Make 3 commits that each change ONE line of a ~2000-line text file (e.g. `seq 1 2000 > big.txt`, then edit a line, commit, repeat). Look inside `.git/objects/` with `find .git/objects -type f`: how many loose objects are there and which kinds (`git cat-file -t`)? How big is each blob version on disk (`ls -l` of the object file) compared with the raw file size, and why is every version stored IN FULL even though only one line changed? What compression is applied to a loose object (try `python3 -c "import zlib,sys; print(zlib.decompress(open(sys.argv[1],'rb').read())[:30])" .git/objects/xx/yyyy...`) and what is the header you see before the content?
2. Run `git count-objects -v` before and after `git gc` (or `git repack -a -d`). Explain every line of its output (`count`, `size`, `in-pack`, `packs`, `size-pack`, `prune-packable`, `garbage`, `size-garbage`). What files appeared in `.git/objects/pack/` (`.pack`, `.idx`, maybe `.rev`/`.bitmap`) and what is each for?
3. Run `git verify-pack -v .git/objects/pack/pack-*.idx`. For each blob version of `big.txt`, read the columns (SHA, type, size, size-in-packfile, offset, depth, base SHA). Which version is stored whole and which as a delta -- and is the full one the OLDEST or the NEWEST version? Why does Git prefer that direction? What does the "chain length = N: M objects" histogram at the bottom tell you?
4. Experiment with `git repack -a -d -f --depth=1 --window=1` vs. `--depth=50 --window=250` on a repo with ~20 versions of the file (script it in a loop). Compare `size-pack` and the max chain depth. What do `--window` and `--depth` trade off (pack size vs. CPU at repack time vs. CPU when reading a deep object)? What does `-f` change? Finally: what do `git cat-file --batch-check='%(objectname) %(objecttype) %(objectsize) %(objectsize:disk) %(deltabase)' --batch-all-objects` and `git rev-list --objects --all --disk-usage` add, and how would you use them to find the files that bloat a real repository?

## WHAT I RAN

```bash
# --- Q1: loose objects -------------------------------------------------------
rm -rf /tmp/day62-lab && mkdir /tmp/day62-lab && cd /tmp/day62-lab
git init -q -b main
git config user.email lab@example.com; git config user.name lab
git config gc.auto 0                       # repo-local: no surprise auto-gc during the lab
seq 1 2000 > big.txt; git add big.txt; git commit -qm v1
for i in 2 3; do sed -i "1000s/.*/changed $i/" big.txt; git commit -qam v$i; done

find .git/objects -type f | sort
for f in $(find .git/objects -type f -path '*/??/*'); do
  sha=$(echo "$f" | sed 's#.git/objects/##; s#/##')
  echo "$sha $(git cat-file -t $sha) disk=$(stat -c %s $f) raw=$(git cat-file -s $sha)"
done
wc -c big.txt
b=$(git rev-parse HEAD:big.txt)
python3 -c "import zlib,sys; d=open(sys.argv[1],'rb').read(); print(d[:2].hex()); print(zlib.decompress(d)[:30])" \
  .git/objects/${b:0:2}/${b:2}

# --- Q2: count-objects before / after packing ---------------------------------
git count-objects -v
git gc -q
git count-objects -v
ls -l .git/objects/pack/

# --- Q3: what is inside the pack ----------------------------------------------
git verify-pack -v .git/objects/pack/pack-*.idx
git rev-list --objects --all | grep big.txt        # newest blob is listed first

# --- Q4: 20 versions, different --window / --depth -----------------------------
rm -rf /tmp/day62-lab4 && mkdir /tmp/day62-lab4 && cd /tmp/day62-lab4
git init -q -b main; git config user.email lab@example.com; git config user.name lab; git config gc.auto 0
seq 1 2000 > big.txt; git add big.txt; git commit -qm v1
for i in $(seq 2 20); do sed -i "$((i*97))s/.*/changed $i/" big.txt; git commit -qam v$i; done
maxdepth() { git verify-pack -v .git/objects/pack/pack-*.idx | awk 'NF>=7 {if($6>m)m=$6} END{print m+0}'; }
for opts in "--depth=1 --window=1" "--depth=50 --window=250" "--depth=1 --window=250" "--depth=50 --window=1"; do
  git repack -q -a -d -f $opts
  echo "$opts: size-pack=$(git count-objects -v | awk '/size-pack/{print $2}')KiB pack=$(stat -c %s .git/objects/pack/*.pack)B maxdepth=$(maxdepth)"
  git verify-pack -v .git/objects/pack/pack-*.idx | grep chain
done
git cat-file --batch-check='%(objectname) %(objecttype) %(objectsize) %(objectsize:disk) %(deltabase)' \
    --batch-all-objects | sort -k4 -n -r | head
git rev-list --objects --all --disk-usage

rm -rf /tmp/day62-lab /tmp/day62-lab4                 # scratch only
```

(git 2.34.1 on Linux.)

## WHAT I OBSERVED

1. **Loose objects, full copies, zlib header:** After 3 commits there were **9 loose objects**: 3 commits, 3 trees, 3 blobs (one of each per commit; `big.txt` is the only file, so each tree has one entry). Each blob is stored **in full**: raw size 8893 bytes for v1 (`seq 1 2000`) and 8898 for v2/v3, and on disk about **3759-3775 bytes** each -- roughly 42%, which is just zlib doing its job on repetitive digits, not any sharing between versions. That's because a loose object is by definition self-contained: its name is the SHA-1 of `"<type> <size>\0<content>"`, and the file `.git/objects/xx/yyyy...` is simply that byte string **zlib-deflated** (the file starts with `78 01`, a zlib header with the fastest/lowest compression level, which is the default `core.loosecompression`). Decompressing it shows `b'blob 8898\x001\n2\n3\n...'` -- the header is the type, a space, the decimal content length and a NUL byte, then the raw file content. No deltas exist at this stage: writing a commit should be cheap, and finding a good delta base is expensive, so Git postpones that work to packing.
2. **`count-objects -v` before/after, files in `objects/pack/`:** Before: `count: 9` (loose objects), `size: 36` (KiB used by them on disk), `in-pack: 0`, `packs: 0`, `size-pack: 0` (KiB of pack files), `prune-packable: 0` (loose objects that ALSO exist in a pack and could be deleted by `git prune-packed`), `garbage: 0` / `size-garbage: 0` (files in the objects directory that are neither valid loose objects nor packs, e.g. a stray temp file or a `.pack` without its `.idx`). After `git gc`: `count: 0`, `size: 0`, `in-pack: 9`, `packs: 1`, `size-pack: 6` -- 36 KiB of loose objects became one 6 KiB pack. `objects/pack/` got `pack-<hash>.pack` (4836 bytes: the objects themselves, each zlib-compressed, some stored as deltas) and `pack-<hash>.idx` (1324 bytes: a sorted SHA -> offset index with a fan-out table so a lookup is a binary search). Newer Git versions / settings also write `pack-<hash>.rev` (reverse index: pack offset -> object position, so Git can map offsets back to objects and compute on-disk sizes without rebuilding that mapping in memory; written by default since Git 2.41) and `pack-<hash>.bitmap` (reachability bitmaps for fast clone/fetch counting, written with `repack -b` or on servers); my 2.34 wrote neither by default.
3. **`verify-pack -v` columns, delta direction, chain histogram:** The rows are `SHA type size size-in-pack offset [depth base-SHA]`. For `big.txt`: `c5fd08a… blob 8898 4228 396` -- **v3, the NEWEST version, stored whole** (8898 bytes of content, 4228 compressed in the pack); `8e8628f… blob 14 25 4791 1 c5fd08a…` (v2) and `7972c09… blob 17 29 4716 1 c5fd08a…` (v1) are **deltas of depth 1 against v3**: 14 and 17 bytes of delta instructions ("copy bytes 0-N from the base, insert these few bytes, copy the rest"), 25-29 bytes in the pack. So the full copy is the newest, and older versions are reconstructed backwards from it. Git prefers that direction because the most recent objects are the ones read most often (checkout, diff, blame of HEAD), so they should be cheapest to access; it also helps that files usually grow, and deleting from a larger base is a tiny delta while adding needs the inserted bytes. (Git's delta heuristic sorts candidates by type, name hash and size *descending*, and recency order also influences it -- it's a heuristic, not a hard rule.) The footer `non delta: 7 objects` / `chain length = 1: 2 objects` is a histogram: 7 objects are stored whole (3 commits, 3 trees, the v3 blob -- commits and tiny trees aren't worth deltifying here) and 2 objects sit at delta depth 1. Long chains in that histogram mean reading an old object requires applying many deltas in a row.
4. **`--window` / `--depth` / `-f` trade-offs, finding bloat:** With 20 versions (one changed line each):

   | options | pack size | max chain depth |
   |---|---|---|
   | `--depth=1 --window=1` | 13 320 B (`size-pack` 15) | 1 (18 deltas) |
   | `--depth=50 --window=250` | **8 596 B** (`size-pack` 11) | 8 (19 deltas spread over depths 1-8) |
   | `--depth=1 --window=250` | 9 923 B (`size-pack` 12) | 1 (19 deltas) |
   | `--depth=50 --window=1` | 13 444 B (`size-pack` 15) | 1 |

   `--window=N` is how many neighbouring objects (in Git's sorted list) each object is tried against as a delta base: bigger window = better bases found = smaller pack, but repack CPU/memory grows roughly linearly with the window. `--depth=N` caps the delta chain length: deeper chains let every version delta against its most similar neighbour (smaller pack), but **reading** an object at depth d means inflating the base and applying d deltas, so very deep chains make checkout/blame/log -p of old history slower (Git caches delta bases to soften this). Depth alone did nothing with `--window=1` -- with only one candidate per object there's no chance to build a chain worth having -- so the window is what actually finds the savings; depth only allows them to stack. `-f` (`--no-reuse-delta`) makes Git throw away the existing deltas and recompute them from scratch; without it, repack happily reuses deltas already in the old pack, so changing `--window`/`--depth` would barely show any effect (that's also what `git gc --aggressive` does: `-f` with a large window). For hunting bloat: `git cat-file --batch-check='%(objectname) %(objecttype) %(objectsize) %(objectsize:disk) %(deltabase)' --batch-all-objects` lists **every** object (even unreachable ones) with its real size, its size on disk after compression/deltas, and its delta base (all zeros = stored whole); sort by `objectsize:disk` to find what really costs space -- in my lab the two non-delta blobs (~4.2 KB each on disk) were at the top. `git rev-list --objects --all` adds the **path** for each blob, so you join the two lists (SHA -> path) to answer "which file in history is huge" -- typically a committed binary, a dump or a `node_modules` that was later deleted but still lives in old commits. `git rev-list --objects --all --disk-usage` prints the total on-disk bytes of everything reachable (13 412 here); you can scope it, e.g. `git rev-list --disk-usage --objects main..feature` = how much a branch adds. (`--disk-usage=human` only exists in newer Git; 2.34 rejected it.) The fix for real bloat is then rewriting history (`git filter-repo --strip-blobs-bigger-than 10M`, or `--path big.bin --invert-paths`) plus Git LFS going forward.

## WHAT SURPRISED ME

- Loose objects use zlib's *fastest* level (`78 01` header) -- each version still took ~3.7 KB even though only one line changed, so a repo full of loose objects is much bigger than it needs to be until `gc` runs.
- The full copy in the pack is the **newest** blob and the old ones are deltas pointing forward in time -- the opposite of how I'd naively store history (base + forward patches).
- The deltas were absurdly small: 14-17 bytes to describe "same 8.9 KB file with one line changed".
- `--depth=50` with `--window=1` did not help at all; the window is what finds good bases.
- My git (2.34) doesn't write `.rev` files by default and doesn't accept `--disk-usage=human` yet.

## ONE-LINE TAKEAWAY

Git writes every version whole (zlib'd loose objects) and only later, at `gc`/`repack` time, packs them with the newest version stored in full and older versions as tiny deltas -- `--window` buys smaller packs with repack CPU, `--depth` buys smaller packs at the cost of slower reads of old objects, and `cat-file --batch-check` + `rev-list --objects` tell you exactly which blobs make a repo fat.
