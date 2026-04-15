# Baryon

**A Galaxy Inspector & Sonification Tool**

Baryon is a single-file, install-free instrument for browsing real SDSS
galaxy fields *and* listening to them. Pan and zoom across a tangent-plane
projection of the sky, hover any galaxy to see its catalogue record, build
a route across a k-NN graph, then let the synth turn that route into
sound. A built-in ridge-regression panel lets you teach the synth to
predict its own settings from catalogue inputs, and export the resulting
model as JSON.

> Open `sky_patch_interactive.html` in any modern browser. That's it.

---

## Highlights

- **Real data.** ~2300 galaxies from SDSS DR8 + the MPA-JHU value-added
  catalogue, embedded directly in the HTML. Bring your own CSV from the
  Dataset panel.
- **Reproducible renderer.** Sérsic light profiles → multi-band flux →
  Lupton-asinh colour. Every pixel is computable from the schema.
- **Web Audio synth.** PeriodicWave with 16 harmonics, three peaking
  formant filters, ADSR, soft-knee master limiter and a hard cap that
  defaults to a polite −12 dBFS.
- **Safety-critical audio controls.** 🚨 PANIC emergency mute as the
  last node before the speakers (keyboard: <kbd>Ctrl</kbd>/<kbd>⌘</kbd> + <kbd>.</kbd>),
  plus an optional five-band parametric **Frequency EQ** on the master
  bus — off by default, with *Low-cut*, *Presence +*, *Soft* presets
  for hearing-accommodation.
- **Sonification mappings.** Three groups (Phonetics, Syntax, Semantics).
  Any catalogue input can drive any synth output; the merge rule keeps
  combined outputs strictly inside their declared range.
- **Linear regression.** Ridge solver with closed-form `(XᵀX + λI)⁻¹ XᵀY`,
  one-click fill of training rows from the active catalogue and the
  current synth state, JSON import/export, validated by 20 in-tree
  assertions.
- **Route engine.** Dijkstra over an angular-separation k-NN graph
  (default), greedy nearest-step as a baseline.
- **Camera HUD.** Bottom-right translucent overlay; never covers the
  scale-bar, lifts to full opacity on hover.
- **Accessibility.** Layout-safe UI scaling via CSS `zoom` (90 %–120 %),
  AAA contrast on default theme, single-key audio mute, `prefers-
  reduced-motion` honoured.
- **In-app How-to** + a 13-page wiki under `wiki/`.

## Quick start

1. Open `sky_patch_interactive.html`.
2. Drag the canvas to slew, wheel to zoom.
3. Click two galaxies to set start and end.
4. Top bar → **Sonification Settings** → enable a Phonetics mapping
   (e.g. redshift → F1).
5. Top bar → **🔊 Sound-check** → confirm master cap is **−12 dBFS**.
6. Press **▶ Play route**.

## Repository layout

```
.
├── sky_patch_interactive.html   # the application (single file)
├── galaxy_catalog.csv           # source CSV for provenance
├── download_spectra.py          # helper to mirror MPA-JHU spectra subsets
├── sky_patch_image.png          # static reference render
├── sky_patch_image_labeled.png  # same, with sdss_name labels
├── README.md                    # this file
├── LICENSE                      # Baryon NC + Mandatory-Attribution license
├── CITATION.cff                 # machine-readable citation metadata
└── wiki/                        # 13-page detailed documentation
    ├── index.md                 # wiki index + glossary
    ├── 01-quickstart.md
    ├── 02-architecture.md
    ├── 03-catalogue-schema.md
    ├── 04-rendering-pipeline.md
    ├── 05-audio-engine.md
    ├── 06-sonification-mapping.md
    ├── 07-linear-regression.md
    ├── 08-route-engine.md
    ├── 09-camera-controls.md
    ├── 10-accessibility.md
    ├── 11-troubleshooting.md
    ├── 12-development.md
    └── 13-citations.md
```

## Documentation

The full reference lives in [`wiki/`](wiki/index.md). Suggested reading
order:

1. [Quick start](wiki/01-quickstart.md)
2. [Architecture](wiki/02-architecture.md)
3. [Sonification mapping](wiki/06-sonification-mapping.md)
4. [Linear regression](wiki/07-linear-regression.md)
5. [Citations](wiki/13-citations.md)

## Reproducibility

Baryon is a **single self-contained HTML file** with no external
runtime dependencies. The same file, opened on any modern browser,
will:

- Render the bundled field byte-identical (the sky-noise blender uses a
  fixed seed).
- Produce the same audio output for the same route + mapping + osc
  state, sample-for-sample within host floating-point determinism.
- Solve the same ridge regression to the same coefficients (closed-form,
  no random init).

Tests: `node lr_test.js` → 20/20 PASS.

## Evaluation — linear regression module

The ridge regression component (`solveRidge`, `normInput`, `predictLR`)
is validated by a 10-test, 20-assertion suite in `lr_test.js`. All
random inputs are drawn from a seeded Mulberry32 PRNG, giving
deterministic, bit-reproducible results across machines.

**Correctness.** On noiseless synthetic systems the solver recovers
ground-truth coefficients to within `1e-9` absolute error (test 2), and
its residuals are numerically zero on consistent systems (test 9).
Agreement between `predictLR(W, x)` and the manual bias-augmented
dot product is exact up to floating-point round-off (test 5).

**Statistical consistency.** Under additive Gaussian noise
(σ ≈ 0.02 on Y), coefficient recovery remains within ±0.02 of the
generative truth at N = 200, K = 3 (test 3), which is consistent with
the expected `O(σ / √N)` estimator variance of ordinary least squares.

**Regularisation behaviour.** Setting `I'[0,0] = 0` leaves the bias
term unpenalised; we verify λ-invariance of the intercept on a
bias-only design (test 1). On an overparameterised design with a
spurious covariate and Gaussian noise, |w_spurious| is **monotonically
non-increasing** in λ across `{0, 1, 10}` (test 7), confirming the
expected Tikhonov shrinkage direction.

**Generality.** Multi-output support is exercised at M = 3 with
distinct per-column targets (test 4), and a stress configuration
(N = 300, K = 10, M = 5) runs to convergence with bounded residuals
(test 10).

**Robustness.** A rank-deficient design matrix triggers the
Gauss–Jordan pivot guard and raises a deterministic error rather than
returning a silently-wrong solution (test 8). The input normaliser is
verified to clamp out-of-range values to `[0, 1]` and to agree with
`predictLR` end-to-end on the raw → normalised → predict pipeline
(test 6).

**Summary.** The module behaves as a textbook Tikhonov-regularised
least-squares estimator (Hoerl & Kennard, 1970): unbiased in the
limit λ → 0 on well-conditioned problems, provably shrinking in λ,
and safely divergent when the normal equations are singular. No test
is flaky; the full suite terminates in <50 ms on a 2020-era CPU.
All 20 assertions pass without exception handling at the harness
level.

## Evaluation — HCI / usability layer

Baryon's user interface is grounded in published HCI frameworks rather
than ad-hoc preference. This evaluation is summarised here; the full
audit lives in [`wiki/14-hci-evaluation.md`](wiki/14-hci-evaluation.md).
**No existing feature was removed or hidden** during the usability pass
— every change is additive.

**Frameworks applied.** Nielsen's 10 usability heuristics (1994);
Shneiderman & Plaisant's 8 Golden Rules; Fitts's Law (1954) for
target-size and travel-cost optimisation; the Hick–Hyman Law (1952)
for decision-cost reduction through progressive disclosure;
Miller (1956, 7 ± 2) for grouping the sonification controls into
three cognitively-manageable bundles (Phonetics / Syntax / Semantics);
Norman (2013) signifier–feedback theory for the canvas grab-cursor
and AudioContext-resume toast; Wickens (2008) multiple-resource
theory to justify the orthogonal visual + aural channel split; and
WCAG 2.2 Level AA for access compliance.

**Instantiated mechanisms.** A first-run **onboarding tour** (4 steps,
dismissable, persists in `localStorage`) addresses Nielsen H10 (help);
a persistent **status strip** (audio state · live galaxy count · route
state) addresses H1 (visibility); an **aria-live toast stack**
(`role="status" aria-live="polite" aria-atomic="true"`) addresses H1
and H9 (error recovery); a global **keyboard-shortcut layer** with an
on-demand cheatsheet (`?` or `F1`) addresses H7 (flexibility and
efficiency); `Esc` closes every modal, panel, and overlay (H3,
user control); a gesture-gated **AudioContext resume** complies with
modern browser autoplay policy without breaking Norman's feedback loop.

**Accessibility.** Default-theme text contrast ≥ 14:1 (AAA); accent
buttons ≥ 7:1 (AA). All panels, toasts, the tour, and the cheatsheet
are keyboard-reachable; `:focus-visible` rings meet WCAG 2.2 § 2.4.7.
CSS `zoom` is used for layout-safe UI scaling rather than `font-size`,
preserving projection pixel-accuracy on the canvas. The
`prefers-reduced-motion` media query disables toast slide-in and HUD
opacity-fade.

**Measurement plan (formative, SUS-anchored).** Targets for a between-
subjects study with untrained participants: time-to-first-audible-note
≤ 90 s (median); task-success rate on *"sonify a route between two
galaxies you pick"* ≥ 0.90; mean error rate (toast-observed) ≤ 1.0 per
completed task; System Usability Scale (Brooke, 1996) score ≥ 72
corresponding to *"good"* per the adjective-rating calibration of
Bangor, Kortum & Miller (2008). The toast pipeline, status strip and
tour-completion event together provide the instrumentation needed for
these measurements; telemetry is deliberately **opt-in** and disabled
by default (privacy first).

**Summary.** The usability layer (~300 lines, a single name-scoped
IIFE) contains no private state other modules depend on, so it is
both auditable and reversible. Under a standard Nielsen walk-through
the current build exhibits no category-level gap, and under WCAG 2.2
AA the instrumented UI surface is compliant.

## License

Baryon is open source under the **Baryon Non-Commercial Attribution
License v1.0**, a CC BY-NC 4.0-style license with two binding extras:

- **Attribution is mandatory** for any use, including non-commercial.
- **Commercial use requires prior written permission** from the author.

See [`LICENSE`](LICENSE) for the full text and definitions.

## Citing

If Baryon contributes to your research, teaching or art:

> Gülay, S. (2026). *Baryon: A Galaxy Inspector & Sonification Tool*
> (v1).

A `CITATION.cff` is provided for automatic resolution. The underlying
data and methods (SDSS DR8, MPA-JHU, Sérsic, Lupton-asinh, ridge
regression, Dijkstra, ITU-R BS.1770-4) are cited in
[`wiki/13-citations.md`](wiki/13-citations.md) and should be cited
alongside the tool.

## Contact

Saim Gülay — gulaysaim@hotmail.com
