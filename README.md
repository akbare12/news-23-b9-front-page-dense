[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b9-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b9-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# The World Today — Monday 23 November 2026

A dense front page summing up Monday 23 November 2026 in one image: 31 stories
across 6 regions, led by the day's three biggest stories.

## The day

- **AI rout hits Asia** — the Kospi falls 3.3% to 4,708.54 (intraday -5.8%),
  Samsung -3.1%, SK Hynix -2.5%, as the AI sell-off spreads from Wall Street.
- **Guterres: regulate AI before it's too late** — the UN chief urges global AI
  safety rules at the Bridgetown summit; 150 delegates back a risk framework.
- **US lead over China at record low** — Asia Power Index 2026: US 78.9,
  China 73.6, gap 5.3, the narrowest since 2018; India third at 40.5.

The number strip carries the day's figures: -3.3% Kospi, 5.3 US–China gap,
11,762 Ebola cases in the DRC, a 10T-won Seoul rescue fund, the $450M Skubal
Mets deal and Anthropic's $107.3B IPO (raised at $83 a share on 19 Nov).

## How to read it

- **Hero scenes** (3): the three stories above, drawn as scenes.
- **Small cards** (10): stories 4–13, each with its source and a certainty chip
  (REPORTED / CLAIM / ONGOING).
- **The world map**: all 31 stories pinned by number — red = reported,
  amber = claim (unverified), blue = ongoing.
- **Also on Monday** (18): the remaining stories, grouped by region.
- **Date check**: stories that look like 23 November but are not — Democrats
  reach 258 (22 Nov), the Sparta II fire (22 Nov), El Chapo Isidro captured
  (22 Nov), the EU–Indonesia pact (21 Nov), the Nigeria boat (21 Nov) and the
  ICJ Myanmar ruling (19 Nov) — plus what is not yet known.

Scenes are drawn illustrations, not photographs.

## Build

`draw.py` (Python standard library + Pillow) draws `entry.png` (1024×1024).
`main.py` copies it to `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the copy
is byte-identical.

## License

MIT — see `LICENSE`.
