# Contributing

Thanks for helping. This list is small on purpose — a rejected entry is usually
about fit, not quality.

## What belongs here

An entry must satisfy **all three**:

1. **Open source** — public repository, real source code, not just a binary drop
   or a product page.
2. **Actually usable on this board or the Arduino Nano ESP32** — a board
   definition, a firmware you can flash, a library that compiles, or a project
   built on one of those. "Supports every ESP32" is fine; "probably works" is not.
3. **Verifiable** — we can point at the file, board id, or README line that makes
   it work. If it cannot be verified, it is marked as such or left out.

Not accepted: closed-source products, link farms, abandoned forks with no diff,
or projects whose only relationship to the board is the word "ESP32".

## How to add an entry

All entries live in [`data/projects.yml`](data/projects.yml). The two READMEs are
generated — **do not edit the list inside them by hand**, CI will fail.

```bash
python3 -m pip install pyyaml

# 1. add your block under `projects:`
# 2. regenerate both READMEs
python3 scripts/build.py

# 3. check it
python3 scripts/build.py --check
python3 scripts/check_links.py
```

Commit `data/projects.yml` together with the two regenerated READMEs.

## Entry schema

```yaml
- repo: owner/name                      # required, must resolve to a GitHub repo
  section: projects                     # required, one of the ids in `sections:`
  support: full                         # full | generic | none
  license: MIT                          # SPDX id, or "unknown"
  en: One sentence, ends with a period.
  zh: 一句话说明，以句号结尾。
```

`support` is the honest bit:

| value | meaning |
|---|---|
| `full` | has a board definition or is written for this board / the Nano ESP32 |
| `generic` | works on any ESP32-S3, no board-specific support |
| `none` | related and useful, but does not run on the board |

Descriptions: one sentence, start with a capital, end with a period, no marketing
words ("amazing", "powerful", "blazing"). Say what it *does*, not how great it is.
Chinese and English should carry the same information — not a literal translation.

## Star counts

Do not hand-edit stars. They come from `data/stars.json`, refreshed by
`scripts/refresh_stars.py` (needs `GITHUB_TOKEN` to avoid rate limits).

## What gets merged

- The build check and the link check pass.
- The description survives the "so what?" test: a reader who has never seen the
  project knows whether to click.
- New sections are a maintainer decision — propose them in an issue first.

By contributing you agree to release your contribution under [CC0 1.0](LICENSE).
