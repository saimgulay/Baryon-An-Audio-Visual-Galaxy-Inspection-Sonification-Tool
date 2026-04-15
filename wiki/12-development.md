# 12 · Development

## Source layout

A single HTML file is split by clearly-marked comment banners. To find a
section, search for `// ===== <name> =====`. Current top-level sections:

```
===== EMBEDDED CATALOGUE =====
===== PROJECTION & LAYOUT =====
===== RENDER =====
===== CAMERA & INPUT =====
===== AUDIO ENGINE =====
===== SONIFICATION REGISTRY =====
===== ROUTE ENGINE =====
===== LINEAR REGRESSION =====
===== UI: TOP BAR =====
===== UI: SIDE PANEL =====
===== UI: PANELS (sonif / snd / data / lr / a11y / help) =====
===== BOOT =====
```

## Editing safely

- Run `node --check sky_patch_interactive.html` after extracting the
  `<script>` block to catch syntax errors before reload.
- The file uses no top-level `await`; everything is event-driven from
  `DOMContentLoaded`.
- Keep DOM ids stable — they are referenced by the help panel TOC and
  by external automation/tests.

## Testing

- **LR**: `node lr_test.js` runs 20 assertions. Add new tests by
  appending to the test array; the runner aggregates pass/fail.
- **Render**: there is no headless render harness. Diff
  `sky_patch_image.png` against a fresh export when changing the
  Sérsic / asinh paths.
- **Audio**: there is no headless audio harness. Add `console.log`
  near `userGain` automations and capture the `AudioContext.currentTime`
  trace for waveform debugging.

## Conventions

- 2-space indentation, semicolons, no trailing commas in object literals
  inside the embedded catalogue (kept JSON-friendly).
- Catalogue keys: short. UI labels and wiki: long. Never mix.
- Every output sound action is bounded by the master limiter and cap;
  do not bypass them.
- Every new input/output goes through `SONIF_INPUTS` / `SONIF_OUTPUTS`.
  Do not reach into the audio graph from mapping code.

## Adding an input

```js
SONIF_INPUTS.push({
  id:   'log_z',
  label:'log10(1 + z)',
  lo:   0.0,
  hi:   0.3,
  get:  g => Math.log10(1 + g.z)
});
```

The Sonification panel and the LR input list pick this up automatically.

## Adding an output

```js
SONIF_OUTPUTS.push({
  id:   'pan',
  label:'Stereo pan',
  lo:  -1, hi: 1,
  set:  v => panNode.pan.setTargetAtTime(v, ctx.currentTime, 0.01)
});
```

Outputs are responsible for clamping; ranges in the registry are
advisory.

## Releasing

1. Bump the version comment at the top of the HTML.
2. `node lr_test.js` — must be 20/20.
3. Open the file in Chromium and Firefox; verify the route plays end-to-end.
4. Tag the commit; attach the HTML + LICENSE to the release.

## Contributing

Pull requests welcome under the project license (see `LICENSE`).
Please attach test output for any change that touches the LR solver or
the audio bus, and a screenshot for any UI change.
