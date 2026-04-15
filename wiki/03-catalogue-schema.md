# 03 · Catalogue schema

The catalogue is an array of plain objects. Each object describes one
galaxy. Keys are short to keep the embedded JS literal compact; the UI and
this wiki always show the long names.

## Fields

| Short | Long name | Unit | Source / definition |
|---|---|---|---|
| `sdss_name` | SDSS object name | — | DR8 `OBJID` formatted as `SDSS Jhhmmss.ss±ddmmss.s`. |
| `a` | Right ascension (α) | degree, ICRS | DR8 `RA`. |
| `d` | Declination (δ) | degree, ICRS | DR8 `DEC`. |
| `z` | Spectroscopic redshift | dimensionless | DR8 pipeline `Z`, with `zWarning = 0`. |
| `mu`, `mg`, `mr`, `mi`, `mz` | SDSS model magnitudes | mag (AB) | DR8 `modelMag_{ugriz}`, Galactic-extinction-corrected. |
| `r50` | Half-light radius (Sérsic) | arcsec | MPA-JHU `R50_R`. |
| `nser` | Sérsic index | dimensionless | MPA-JHU `N_R`. |
| `lgms` | log₁₀ stellar mass | dex M☉ | MPA-JHU `LGM_TOT_P50`. |
| `sfr` | log₁₀ SFR (optional) | dex M☉/yr | MPA-JHU `SFR_TOT_P50`. |
| `oh` | 12 + log(O/H) (optional) | dex | MPA-JHU `OH_P50`. |

Two derived fields are computed at load time and refreshed by every
`buildCatalogForField()` call:

| Field | Meaning |
|---|---|
| `_x`, `_y` | Pixel coordinates in the current viewport (gnomonic TAN). |

## Bring your own catalogue

The viewer accepts any array conforming to the schema above. Required keys
are `sdss_name`, `a`, `d`, `z`. Everything else is optional but unlocks
matching sonification inputs (e.g. without `lgms` the mass-driven mappings
are simply hidden).

To swap the bundled catalogue:

1. Open `sky_patch_interactive.html` in a text editor.
2. Locate `const EMBEDDED_CAT = […];` near the top of the script.
3. Replace the literal with your own array. Keep it valid JSON-like JS.

For larger catalogues, use the **📂 Dataset** panel to load a CSV at
runtime. The CSV must have a header row whose names match the long names
above (`RA`, `Dec`, `redshift`, `modelMag_g`, …) — the loader maps to short
keys automatically.

## Provenance and units

- Coordinates are ICRS J2000.
- Redshifts are heliocentric SDSS spectroscopic pipeline values.
- Magnitudes are AB system, model magnitudes, with Galactic-extinction
  correction already applied (Schlegel, Finkbeiner & Davis 1998).
- Stellar masses use a Kroupa initial mass function and the MPA-JHU
  spectro-photometric SED fits (Kauffmann et al. 2003; Salim et al. 2007).

See [13 · Citations](13-citations.md) for full references.
