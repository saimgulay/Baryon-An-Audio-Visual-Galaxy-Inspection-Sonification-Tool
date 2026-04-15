# 04 · Rendering pipeline

The on-screen image is computed from the catalogue, not loaded from a FITS
cutout. This means every pixel is reproducible from the schema.

## 1. Projection: gnomonic TAN

For a tangent point (α₀, δ₀) and a target (α, δ):

```
ξ = cos δ · sin(α − α₀) / D
η = (sin δ · cos δ₀ − cos δ · sin δ₀ · cos(α − α₀)) / D
D = sin δ · sin δ₀ + cos δ · cos δ₀ · cos(α − α₀)
```

Then `_x = W/2 + (ξ / FoV_rad) · W`, similarly for `_y`. The viewer keeps
the field square (`W = H`) when possible; if not, the smaller side governs
the angular scale so circles stay circular.

## 2. Sérsic light profile

Each galaxy contributes a circular Sérsic profile:

```
I(r) = I_e · exp( −b_n · ( (r / R_e)^(1/n) − 1 ) )
b_n  ≈ 2 n − 1/3 + 4/(405 n) + …          (Ciotti & Bertin 1999)
```

with `R_e = r50` (arcsec) converted to pixels using the current
arcsec/pixel scale, and `n = nser`. Total flux is normalised so that the
integrated AB magnitude matches `modelMag_r`.

For performance, profiles below 1.5 px FWHM are rendered as a single
Gaussian splat; profiles larger than 6× the field are clipped at the
field edge.

## 3. Flux compositing

Per-band flux buffers (g, r, i) accumulate light from all visible
galaxies. Saturation is handled by clipping in flux space, not by
post-hoc tone mapping.

## 4. Colour: asinh stretch (Lupton 2004)

The composited (g, r, i) → (B, G, R) mapping uses the standard SDSS asinh
stretch:

```
y = asinh( α · I / β ) / asinh(α)
```

with α = 8 and β chosen per-band so that the median sky pixel maps to
~0.05. This preserves dynamic range across 5+ orders of magnitude
without crushing bright galaxy cores or losing faint outskirts.

Reference: Lupton, Blanton, Fekete et al. (2004),
*PASP* **116**, 133.

## 5. Sky blend

A static blue-noise pattern is added at very low amplitude before display
so the background does not look digitally flat. The seed is fixed for
reproducibility; the same field renders byte-identical between sessions.

## 6. Display

The composed RGBA buffer is written via `ctx.createImageData(W,H)` →
`ctx.putImageData`. The function is guarded by:

```js
if (!(W > 0 && H > 0) || !isFinite(W) || !isFinite(H)) {
  try { layout(); } catch (e) {}
  if (!(W > 0 && H > 0)) return;
}
```

This avoids the “source width or height is zero” class of errors during
panel toggles and accessibility scaling transitions.

## Performance notes

- All flux maths run in `Float32Array` typed arrays.
- The colour pass runs in one tight loop over `W*H` pixels; on a 2020
  laptop this completes in ≤8 ms for a 1024² viewport.
- No GPU/WebGL is used by design — keeping the pipeline auditable and
  device-independent matters more here than raw FPS.
