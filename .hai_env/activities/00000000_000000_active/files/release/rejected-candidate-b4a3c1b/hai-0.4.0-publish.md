# Publish HAI 0.4.0

Prepared source commit: `b4a3c1b78694f47c586072f56fec91ade5ae867a`. Repository: `h111359/haide`, default branch `main`.

Assets:

- `dist/hai-0.4.0.zip`
- `dist/hai-0.4.0.zip.sha256`

Expected ZIP SHA-256: `f96393f7f0941263ab89efac8c18275b599365dd585f036077e048bd675ee563`.

The local release-source commit exists. No tag, push, GitHub draft or publication
was performed. The ZIP is an exact-commit core bundle; optional agents must be
obtained separately from this same source revision. Bundle state target is 3,
recognizing `[2, 3]`; 0.3.0 environments need explicit config-layout migration.

## 1. Confirm the candidate

Run from the repository workspace. Review `release-notes/0.4.0.md`, the checksum
and the source commit. Do not publish from a different revision or use a rebuilt
archive without renewed inspection/digest evidence.

```bash
git show --no-patch --oneline b4a3c1b78694f47c586072f56fec91ade5ae867a
sha256sum dist/hai-0.4.0.zip
```

Compare the output to the expected digest above. Check that no local or remote
`v0.4.0` already exists with different identity; if one does, stop and inspect it.
Do not move a published tag or overwrite published assets.

## 2. Push the exact source and annotated tag

These are manual publication steps for an authenticated repository writer.
They deliberately select the reviewed full commit rather than a later HEAD.
No force push is needed or authorized. Stop on remote divergence and resolve it
through normal review rather than rewriting remote history.

```bash
git tag -a v0.4.0 b4a3c1b78694f47c586072f56fec91ade5ae867a -m "HAI 0.4.0"
git push origin b4a3c1b78694f47c586072f56fec91ade5ae867a:refs/heads/main
git push origin refs/tags/v0.4.0
```

A tag push can trigger remote automation/webhooks. No repository release workflow
was added during preparation. If any step fails, inspect the actual tag/ref state
before resuming; do not blindly recreate or replace resources.

## 3. Create a GitHub draft and review it

If GitHub CLI is available on your publishing machine, authenticate there using
its normal supported method; no personal token is required by these instructions.
The CLI was not installed in the preparation environment. `--verify-tag` prevents
implicit tag creation from an unintended default-branch revision.

```bash
gh release create v0.4.0 dist/hai-0.4.0.zip dist/hai-0.4.0.zip.sha256 --repo h111359/haide --verify-tag --draft --title "HAI 0.4.0" --notes-file release-notes/0.4.0.md
gh release view v0.4.0 --repo h111359/haide --web
```

Review the tag/source, notes, both asset names and state-format/layout upgrade
information. Then publish the reviewed draft:

```bash
gh release edit v0.4.0 --repo h111359/haide --draft=false
```

Equivalent browser path: open https://github.com/h111359/haide/releases/new,
select the existing `v0.4.0` tag, set title `HAI 0.4.0`, paste the prepared notes,
upload the two assets, save a draft, review it and publish. Do not select an
unrelated target or create a new tag at a different commit through the browser.

## 4. Verify the published download

Verify that the release is published at
https://github.com/h111359/haide/releases/tag/v0.4.0 and the annotated tag peels
to `b4a3c1b78694f47c586072f56fec91ade5ae867a`. Download both uploaded assets into a new directory within your
workspace, then verify the checksum there. For GitHub CLI:

```bash
gh release download v0.4.0 --repo h111359/haide --pattern "hai-0.4.0.zip*" --dir dist/verify-0.4.0
```

From `dist/verify-0.4.0`, run `sha256sum --check hai-0.4.0.zip.sha256` and compare
the digest with `f96393f7f0941263ab89efac8c18275b599365dd585f036077e048bd675ee563` as independent preparation evidence. Verify archive
contents/version as well; a checksum file does not authenticate itself.

On partial upload/publication failure, inspect the existing draft/release and
assets before any recovery action. Do not use `--clobber`, delete published assets,
move tags or silently reuse version 0.4.0 for changed bytes. Published corrections
need a new release identity under the release policy.

Official CLI reference: https://cli.github.com/manual/gh_release_create,
https://cli.github.com/manual/gh_release_edit and
https://cli.github.com/manual/gh_release_download.
