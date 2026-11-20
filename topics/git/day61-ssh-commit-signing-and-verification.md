# Day 61, Task 8 -- Git: signing commits and tags with an SSH key, `allowed_signers`, and verifying signatures (`verify-commit`, `%G?`, `log --show-signature`)

## THE TASK

In a SCRATCH repo (`/tmp/day61-lab`, `git init -b main`) and with a THROWAWAY key made just for this lab (`ssh-keygen -t ed25519 -f /tmp/day61-key -N "" -C lab`), learn how Git signs and verifies commits. Never use or change your real keys, and never touch your global config for this lab -- keep every setting either repo-local in the scratch repo or one-off with `git -c ...`. Answer the questions by actually running the commands.

1. Configure SSH signing for the lab repo only: `gpg.format`, `user.signingkey` (path to the PUBLIC key file, or the literal `key::ssh-ed25519 ...`), and make one commit with `git commit -S` and one without. What does `git cat-file -p HEAD` show for the signed commit (which header holds the signature, and what exactly is signed -- the tree? the parents? the message? the author date)? What does `commit.gpgSign=true` change?
2. Run `git verify-commit HEAD` and `git log --show-signature -1` BEFORE configuring `gpg.ssh.allowedSignersFile`. Why does it fail even though the signature is mathematically valid? Create `/tmp/day61-allowed_signers` in the right format (`<principal> <key-type> <key>`, principal = the committer email), point the repo at it, and verify again. What do `%G?`, `%GS`, `%GK` print in `git log --format='%h %G? %GS %GK %s'` for the signed commit, the unsigned commit, and (after the next step) a tampered one? List the meaning of the `%G?` letters you saw (`G`, `B`, `U`, `N`, `E`, ...).
3. Tamper: take the signed commit's raw object, change ONE character of its message, write it back with `git hash-object -t commit -w --stdin`, and run `git verify-commit` on the new hash. What happens and why? Then amend the signed commit with `git commit --amend --no-edit` WITHOUT `-S` (and with `commit.gpgSign` unset) -- is the signature kept? What about after `git rebase` or `git cherry-pick` of a signed commit -- who signs the rewritten commit, if anyone?
4. Tags: create a signed annotated tag with `git tag -s v0.1 -m "lab"` and verify it with `git tag -v v0.1` / `git verify-tag`. Why can a LIGHTWEIGHT tag never be signed? Finally explain, in your own words, what a "Verified" badge on a hosting site does and does NOT prove (signature vs. committer email vs. author email vs. who actually pushed), and why signing with a key the site doesn't know about shows "Unverified" even if `git verify-commit` locally says "Good".

## WHAT I RAN

```bash
# TODO: paste the commands you actually ran, grouped by question
```

## WHAT I OBSERVED

1. **Signing setup / what is signed:** TODO
2. **allowed_signers and `%G?` letters:** TODO
3. **Tampering, amend, rebase/cherry-pick:** TODO
4. **Signed tags and "Verified" badges:** TODO

## WHAT SURPRISED ME

- TODO

## ONE-LINE TAKEAWAY

TODO
