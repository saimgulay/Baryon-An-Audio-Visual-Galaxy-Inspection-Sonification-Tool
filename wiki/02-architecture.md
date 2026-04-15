# 02 · Architecture

The project is intentionally a **single self-contained HTML file**. No
bundlers, no package manager, no transpilation. The whole UI, render
pipeline, audio engine and ML solver live in one file so the artefact is
trivially reproducible and citable.

## Files in the repo

| Path | Role |
|---|---|
| `sky_patch_interactive.html` | The application. ~3700 lines, HTML+CSS+JS. |
| `galaxy_catalog.csv` | Embedded as a JS literal at boot; original CSV kept for provenance. |
| `download_spectra.py` | Helper to mirror MPA-JHU spectra subsets locally. |
| `sky_patch_image.png` | Static reference render of the default field. |
| `sky_patch_image_labeled.png` | Same, with sdss_name labels. |
| `wiki/` | This documentation tree. |
| `README.md` | Repo entry point; links here. |

## Module boundaries inside the HTML

The script is divided into commented sections. From top to bottom:

1. **Catalogue & data** — the embedded short-key array, parser, and
   `buildCatalogForField()` which projects RA/Dec → image (x, y) for the
   current field-of-view.
2. **Projection & layout** — gnomonic TAN projection, viewport sizing, the
   resize-safe `layout()` and `display()` guards.
3. **Render pipeline** — Sérsic light profiles, flux compositing, asinh
   colour mapping (Lupton 2004), a sky-noise blender for visual realism.
4. **Camera & input** — drag/wheel handlers, slew rate, the bottom-right
   `#camHUD` overlay.
5. **Audio engine** — `AudioContext`, master limiter bus, oscillator + 3
   formants + 16-harmonic `PeriodicWave`, ADSR.
6. **Sonification registry** — `SONIF_INPUTS` and `SONIF_OUTPUTS` arrays,
   group merge rule, monophonic vs. graph mode.
7. **Linear regression** — Ridge solver (Gauss–Jordan), normaliser,
   training table, fill-from-galaxy / fill-from-osc helpers, JSON
   import/export.
8. **Route engine** — k-NN proximity graph + Dijkstra and a greedy nearest
   walk for comparison.
9. **UI panels** — Sonification settings, Sound-check, Dataset, LR,
   Accessibility, Help. All panels are mutually exclusive (`.ss-panel`).

## Data flow at a glance

```
CSV → cat[] (short-key records)
       │
       ├── buildCatalogForField → cat[i]._x, _y (screen coords)
       │             │
       │             └── render() → off-screen flux buffer → ctx.putImageData
       │
       ├── routeEngine(cat, start, end) → route[]
       │             │
       │             └── audioEngine.play(route, sonifMappings)
       │
       └── lrTraining(cat, mappings, oscState) → ridgeSolve → W → predictLR
```

## Why a single file

- **Reproducibility.** A reader can hash the file and reproduce every figure
  in the paper, audio sample in the appendix, and table in the supplement.
- **Auditability.** A reviewer can read the whole pipeline top-to-bottom in
  one editor tab.
- **Zero install.** No npm, no Python venv, no MathJax, no D3. The only
  external thing is the browser.

## Coding conventions

- ES2020+ vanilla JS. No frameworks. No JSX.
- Globals are deliberate and grouped at the top of each section.
- DOM ids match short, scannable names (`#camHUD`, `#sonifPanel`,
  `#lrPanel`).
- Catalogue keys are 1–2 characters (`a`, `d`, `z`, `mu`, `mg`, `mr`, `mi`,
  `mz`, `r50`, `nser`, `lgms`, …) to keep the embedded literal small. A
  short-key→long-name table lives in [03 · Catalogue schema](03-catalogue-schema.md).
