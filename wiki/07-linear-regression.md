# 07 · Linear regression

Baryon ships an in-app **ridge regression** tool that learns to predict
synth output settings from catalogue inputs. This lets a user
demonstrate, fit, and inspect a perception-style mapping without
exporting data.

## The model

For K inputs and M outputs, with N training rows:

```
X ∈ ℝ^(N × (K+1))    — inputs with a leading 1-column for bias
Y ∈ ℝ^(N × M)
W = (Xᵀ X + λ I')⁻¹ Xᵀ Y    — closed-form ridge solution
```

`I'` is the identity with `I'[0,0] = 0` so the **bias term is not
regularised**. The system is solved by Gauss–Jordan elimination with
partial pivoting; on singular augmentation the solver throws and the UI
shows a clear status message.

`predictLR(W, x_norm)` evaluates `[1, x_norm] · W` with no further
post-processing; the normaliser handles range fitting on both ends.

## Normalisation

Each input column is mapped to [0, 1] using its declared `[lo, hi]`:

```
v_norm = clamp((v − lo) / (hi − lo), 0, 1)
```

Outputs are stored in their natural units; rescaling happens at the
synth boundary, not in the model. This keeps W coefficients
interpretable as “units of output per fractional unit of input”.

## Training workflow

1. In the **Sonification Settings** menu, enable the inputs and outputs
   you care about.
2. Open the **Linear Regression** panel.
3. For each training row:
   - Type a galaxy id and click **⤓ Fill inputs from galaxy** to copy
     that row's catalogue values into the input cells.
   - Adjust the synth on the Sound-check panel until you like it.
   - Click **⤓ Fill outputs from osc** to snapshot the current synth
     state into the output cells.
4. Add more rows. 5–20 rows is usually enough to see structure.
5. Set λ (default 0.1; try 0.0 for OLS, 1.0 for strong shrinkage).
6. Click **Fit**. The status text reports per-output R² and residual
   RMS.
7. Click **Predict from hovered galaxy** to drive the synth from the
   model in real time.

## JSON model format

The **Export** button writes:

```json
{
  "version": 1,
  "createdAt": "ISO-8601",
  "inputs":  [{ "id": "z",  "lo": 0,    "hi": 0.3 }, … ],
  "outputs": [{ "id": "f",  "lo": 80,   "hi": 880 }, … ],
  "lambda":  0.1,
  "W":       [[…], …]    // shape (K+1) × M, bias row first
}
```

`Import` validates the schema, restores the input/output enabling and
λ, then loads W. The model is portable across machines.

## Validation

The bundled `lr_test.js` (run with `node lr_test.js`) executes 20
assertions across 10 tests:

- Bias-only λ-invariance.
- Noiseless OLS recovery to 1e-9.
- Noisy recovery within ±0.02 of truth.
- Multi-output 3×3 correctness.
- `predictLR` agreement with manual dot-product.
- End-to-end raw → norm → solve → predict.
- Ridge shrinkage of a spurious feature in the presence of noise
  (monotonic in λ).
- Singular system raises.
- Noiseless residual ≈ 0.
- Stress: K=10, M=5, N=300.

All 20 assertions PASS in CI.

## When ridge is the wrong tool

- Strongly non-linear perceptual mappings (e.g. pitch as log-frequency
  of redshift) need feature engineering: precompute `log10(z+1)` as
  a derived input.
- Categorical-to-continuous mappings (galaxy morphology label →
  formant) want one-hot encoding.
- For small N (≤ K), use larger λ; the closed-form is still well-defined.
