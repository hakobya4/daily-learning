# Day 61, Task 8 -- Git: signing commits and tags with an SSH key, `allowed_signers`, and verifying signatures (`verify-commit`, `%G?`, `log --show-signature`)

## THE TASK

In a SCRATCH repo (`/tmp/day61-lab`, `git init -b main`) and with a THROWAWAY key made just for this lab (`ssh-keygen -t ed25519 -f /tmp/day61-key -N "" -C lab`), learn how Git signs and verifies commits. Never use or change your real keys, and never touch your global config for this lab -- keep every setting either repo-local in the scratch repo or one-off with `git -c ...`. Answer the questions by actually running the commands.

1. Configure SSH signing for the lab repo only: `gpg.format`, `user.signingkey` (path to the PUBLIC key file, or the literal `key::ssh-ed25519 ...`), and make one commit with `git commit -S` and one without. What does `git cat-file -p HEAD` show for the signed commit (which header holds the signature, and what exactly is signed -- the tree? the parents? the message? the author date)? What does `commit.gpgSign=true` change?
2. Run `git verify-commit HEAD` and `git log --show-signature -1` BEFORE configuring `gpg.ssh.allowedSignersFile`. Why does it fail even though the signature is mathematically valid? Create `/tmp/day61-allowed_signers` in the right format (`<principal> <key-type> <key>`, principal = the committer email), point the repo at it, and verify again. What do `%G?`, `%GS`, `%GK` print in `git log --format='%h %G? %GS %GK %s'` for the signed commit, the unsigned commit, and (after the next step) a tampered one? List the meaning of the `%G?` letters you saw (`G`, `B`, `U`, `N`, `E`, ...).
3. Tamper: take the signed commit's raw object, change ONE character of its message, write it back with `git hash-object -t commit -w --stdin`, and run `git verify-commit` on the new hash. What happens and why? Then amend the signed commit with `git commit --amend --no-edit` WITHOUT `-S` (and with `commit.gpgSign` unset) -- is the signature kept? What about after `git rebase` or `git cherry-pick` of a signed commit -- who signs the rewritten commit, if anyone?
4. Tags: create a signed annotated tag with `git tag -s v0.1 -m "lab"` and verify it with `git tag -v v0.1` / `git verify-tag`. Why can a LIGHTWEIGHT tag never be signed? Finally explain, in your own words, what a "Verified" badge on a hosting site does and does NOT prove (signature vs. committer email vs. author email vs. who actually pushed), and why signing with a key the site doesn't know about shows "Unverified" even if `git verify-commit` locally says "Good".

## WHAT I RAN

```bash
# Lab setup: throwaway key, scratch repo, no global config, one-off identity via env
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_AUTHOR_NAME=Narek GIT_AUTHOR_EMAIL=narek@example.invalid
export GIT_COMMITTER_NAME=Narek GIT_COMMITTER_EMAIL=narek@example.invalid
ssh-keygen -q -t ed25519 -f /tmp/day61-key -N "" -C lab
mkdir /tmp/day61-lab && cd /tmp/day61-lab && git init -q -b main

# Q1: repo-local SSH signing, one unsigned + one signed commit
git config gpg.format ssh
git config user.signingkey /tmp/day61-key.pub
echo a > f; git add f; git commit -qm unsigned
echo b >> f; git add f; git commit -q -S -m "signed commit"
git cat-file -p HEAD

# Q2: verify before / after allowed_signers
git verify-commit HEAD; echo "exit=$?"
git log --format='%h %G? [%GS] [%GK] %s'
echo "narek@example.invalid $(cut -d' ' -f1,2 /tmp/day61-key.pub)" > /tmp/day61-allowed_signers
git config gpg.ssh.allowedSignersFile /tmp/day61-allowed_signers
git verify-commit HEAD; echo "exit=$?"
git log --format='%h %G? [%GS] [%GK] %s'

# Q3: tamper with the message, amend without -S, cherry-pick / rebase
T=$(git cat-file -p HEAD | sed 's/signed commit/signed c0mmit/' | git hash-object -t commit -w --stdin)
git verify-commit $T; echo "exit=$?"
git log -1 --format='%h %G? [%GS] %s' $T
git commit -q --amend --no-edit;  git log -1 --format='%h %G? %s'   # then: git reset --hard HEAD@{1}
git checkout -q -b other HEAD~1; echo z > g; git add g; git commit -qm side
git cherry-pick main;             git log -1 --format='%h %G? %s'
git checkout -q main; git rebase -q other; git log --format='%h %G? %s'

# Q4: signed vs. lightweight tags, commit.gpgSign, a key that isn't in allowed_signers
git tag -s v0.1 -m lab; git tag -v v0.1; git cat-file -p v0.1
git tag light; git tag -v light; echo "exit=$?"
git config commit.gpgSign true; echo c >> f; git commit -qam auto; git log -1 --format='%h %G? %s'
ssh-keygen -q -t ed25519 -f /tmp/day61-key2 -N ""
echo d >> f; git -c user.signingkey=/tmp/day61-key2.pub commit -qam otherkey
git log -1 --format='%h %G? [%GS] [%GK] %s'; git verify-commit HEAD; echo "exit=$?"
```

## WHAT I OBSERVED

1. **Signing setup / what is signed:**
   ```
   tree 6cf76faefcefa1121f2a3e663edc331d21fe9797
   parent 5f4ee065e0c8c28b64ab229cfc0178c57139ac89
   author Narek <narek@example.invalid> 1795152855 +0000
   committer Narek <narek@example.invalid> 1795152855 +0000
   gpgsig -----BEGIN SSH SIGNATURE-----
    U1NIU0lHAAAAAQAAADMAAAALc3NoLWVkMjU1MTkAAAAgevPdAzlHg7C+nU32euHlTN13o7
    ...
    -----END SSH SIGNATURE-----

   signed commit
   ```
   The signature lives in an extra **`gpgsig`** header (same header name for GPG and SSH; continuation lines start
   with a space). What gets signed is the whole commit object **without** that header: the `tree` line (so the
   entire snapshot, since the tree hash covers every file), the `parent` line(s) (so the whole history behind it),
   `author` and `committer` including their timestamps, and the message. The unsigned commit simply has no `gpgsig`
   header. `gpg.format=ssh` tells git to call `ssh-keygen -Y sign` instead of gpg; `user.signingkey` pointed at the
   public key file (git finds the private key next to it / in the agent). `commit.gpgSign=true` makes every commit
   behave as if `-S` were given: the `auto` commit came out `G` without `-S`.

2. **allowed_signers and `%G?` letters:**
   Before configuring it, `git verify-commit HEAD` failed with
   `error: gpg.ssh.allowedSignersFile needs to be configured and exist for ssh signature verification` (exit 1),
   and `%G?` showed `N` for both commits. Unlike GPG there is no keyring with trust levels for SSH keys: an SSH
   signature only proves "the holder of *this* key signed it", so git needs a file that says **which key is
   allowed to sign for which identity**. Format: `<principal> <key-type> <base64-key>`, e.g.
   `narek@example.invalid ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHrz3QM...`. After pointing
   `gpg.ssh.allowedSignersFile` at it:
   ```
   Good "git" signature for narek@example.invalid with ED25519 key SHA256:Ju/OzilsOZ/99z//mU9QK9tv7rXTQd4jw6gx+SHP0UA
   cebdb66 G [narek@example.invalid] [SHA256:Ju/Ozils...SHP0UA] signed commit
   5f4ee06 N [] [] unsigned
   1f1139d B [] signed c0mmit                       <- tampered copy (Q3)
   07a7c53 U [] [SHA256:n/iCCphV...JcKoc] otherkey  <- signed with a key not in allowed_signers
   ```
   `%GS` = signer (the matched principal), `%GK` = the key (fingerprint for SSH). Letters seen:
   **G** good signature from an allowed key, **B** bad signature (doesn't match the content), **U** good signature
   but from a key with unknown validity (not in allowed_signers -- `verify-commit` printed "Good ... signature" and
   then "No principal matched.", exit 1), **N** no signature. Others in the docs: **X** good but expired signature,
   **Y** good signature by an expired key, **R** good signature by a revoked key, **E** signature can't be checked
   (e.g. missing key / verification tool error).

3. **Tampering, amend, rebase/cherry-pick:**
   Changing one character of the message ("commit" -> "c0mmit") and writing the object back with
   `git hash-object -t commit -w --stdin` gave a new hash (`1f1139d`) that still carries the old `gpgsig` header.
   `git verify-commit` said `Signature verification failed: incorrect signature` (exit 1) and `%G?` is **B**:
   the signature was made over the old bytes, and the signed content now differs. (Any change -- tree, parent,
   dates, message -- has the same effect, which is why a signature on the tip vouches for the whole history.)
   `git commit --amend --no-edit` without `-S` and with `commit.gpgSign` unset produced `e960a8a N` -- **the
   signature is dropped**, because amend creates a brand-new commit object (new committer date at least) and the
   old signature can't apply to it. Same for `cherry-pick` (`9946532 N`) and `rebase`: the rewritten commits are
   new objects signed by **nobody**, unless whoever runs the rewrite passes `-S` / has `commit.gpgSign=true`, in
   which case they are signed with **the rewriter's** key, not the original author's.

4. **Signed tags and "Verified" badges:**
   `git tag -s v0.1 -m lab` (with `gpg.format=ssh`) creates an annotated tag object; `git tag -v v0.1` printed the
   tag (`object` / `type commit` / `tag v0.1` / `tagger ...` / message) and
   `Good "git" signature for narek@example.invalid ...`, exit 0. For tags the signature is appended to the end of
   the tag message instead of a header. A **lightweight** tag is only a ref (`refs/tags/light` -> commit hash);
   there is no object of its own to put a signature into, so `git tag -v light` fails with
   `cannot verify a non-tag object of type commit`.
   A hosting site's **"Verified"** badge means: the signature is valid for the commit's content AND the signing key
   is registered as a *signing key* on an account AND that account has verified the **committer** email in the
   commit (for SSH: the key must be added specifically as a signing key). It does NOT prove who pushed the commit
   (anyone can push someone else's signed commit), it says nothing about the author when author != committer, and
   it does not prove the code is good. A key the site doesn't know -- or a committer email not verified on the
   key owner's account -- gives "Unverified" even when my local `git verify-commit` says "Good", because locally
   *my* allowed_signers file decides which keys I trust, while the site uses its own registry of account keys.

## WHAT SURPRISED ME

- Without `gpg.ssh.allowedSignersFile`, git can't even say "good signature, unknown signer" for SSH -- it errors
  out and `%G?` shows `N`, as if the commit weren't signed at all.
- A perfectly valid signature from a second key showed up as `U` and `verify-commit` exited 1 with
  "No principal matched." -- valid crypto, but not trusted.
- `commit --amend` silently drops the signature; a "signed" branch becomes unsigned after any rebase unless
  signing is on for the person rebasing.
- The tampered commit still *looks* signed in `cat-file` (the `gpgsig` header is there) -- only verification
  reveals that it doesn't match.

## ONE-LINE TAKEAWAY

An SSH signature (`gpgsig` header) covers tree, parents, identities, dates and message, so any rewrite drops or breaks it; `allowed_signers` (locally) or a registered signing key + verified committer email (on the host) is what turns "valid signature" into "trusted signer".
