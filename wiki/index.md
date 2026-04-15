# Baryon — Wiki

A complete reference for **Baryon: A Galaxy Inspector & Sonification Tool**.

## Contents

| # | Page | What's in it |
|---|------|--------------|
| 01 | [Quick start](01-quickstart.md) | Five-minute walkthrough from open to first sonified route |
| 02 | [Architecture](02-architecture.md) | Files, data flow, module boundaries |
| 03 | [Catalogue schema](03-catalogue-schema.md) | The short-key data format and how to bring your own |
| 04 | [Rendering pipeline](04-rendering-pipeline.md) | Projection → Sérsic → flux → colour → sky blend |
| 05 | [Audio engine](05-audio-engine.md) | Web Audio graph, master bus, ADSR, formants, periodic wave |
| 06 | [Sonification mapping](06-sonification-mapping.md) | Inputs, outputs, groups, merge rule, graph mode |
| 07 | [Linear regression](07-linear-regression.md) | Ridge solver, training workflow, JSON model format |
| 08 | [Route engine](08-route-engine.md) | Dijkstra, k-NN graphs, greedy nearest-step |
| 09 | [Camera HUD](09-camera-controls.md) | Pointing, zoom, slew rate, drag/wheel semantics |
| 10 | [Accessibility](10-accessibility.md) | Layout-safe scaling, contrast, motion, audio attenuation |
| 11 | [Troubleshooting](11-troubleshooting.md) | Symptoms, diagnoses, fixes |
| 12 | [Development](12-development.md) | Source layout, testing, contributing |
| 13 | [Citations](13-citations.md) | Full reference list |
| 14 | [HCI evaluation](14-hci-evaluation.md) | Heuristic-by-heuristic analysis, WCAG 2.2 AA audit, SUS measurement plan |

## Conventions

- Code in `monospace`. Catalogue keys are the short keys (`a, d, z, …`); UI
  labels are the long names (RA, Dec, redshift, …).
- Coordinates are degrees on the ICRS, redshifts are SDSS spectroscopic
  pipeline values (`zWarning = 0`).
- Audio level conventions follow the digital broadcast standard
  ITU-R BS.1770-4 (peak ≤ 0 dBFS; sinusoidal RMS = peak − 3.01 dB).
- Mathematical notation follows the source comments verbatim.

## Glossary

| Term | Meaning |
|---|---|
| α (alpha) | Right ascension, the celestial-sphere "longitude". Degrees, 0–360. |
| δ (delta) | Declination, the celestial-sphere "latitude". Degrees, −90…+90. |
| z | Redshift, dimensionless. |
| FoV | Field of view — the angular width of the displayed sky region. |
| dBFS | Decibels relative to digital full scale. 0 dBFS is the loudest sample. |
| ADSR | Attack–Decay–Sustain–Release amplitude envelope. |
| Sérsic n | Light-profile index. n = 1 ≈ exponential disk; n = 4 ≈ de Vaucouleurs. |
| MPA-JHU | Max-Planck-für-Astrophysik / Johns Hopkins University value-added catalogue. |
| Ridge λ | L2 regularisation strength in linear regression. |
| PCHIP | Piecewise Cubic Hermite Interpolating Polynomial (monotonicity-preserving). |
