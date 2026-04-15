# 10 · Accessibility

Baryon targets WCAG 2.2 AA where reasonable for a single-page tool.

## UI scaling that actually works

Earlier builds tried `body { font-size: … }`, which had no effect
because every chrome element used absolute pixel sizes. The current
implementation uses CSS `zoom` on the chrome containers only, leaving
`<canvas>` untouched so the projection stays pixel-accurate:

```css
body.a11y-font-s  #topbar, #side, .ss-panel, #oscPanel, #sonifPanel,
                  #routebar, #legend, #scaleBar, #camHUD,
                  #tooltip, #status { zoom: 0.90; }
body.a11y-font-m  …{ zoom: 1.00; }
body.a11y-font-l  …{ zoom: 1.10; }
body.a11y-font-xl …{ zoom: 1.20; }
```

Bounded 0.90×–1.20× with `max-width: calc(100vw - 8px)` guard-rails so
panels never overflow the viewport.

## Contrast

- Default background `#0a0d12` against text `#dfe7f0` — contrast ratio
  ≈ 14:1 (AAA).
- Active controls use `#1f4a73` background with white text — ratio ≈ 7:1
  (AA).
- The “How to” top-bar button is intentionally highlighted to be
  discoverable.

## Motion

- All panel toggles are step transitions, no slide animations.
- The route playback animation can be paused; the canvas is not strobed.
- Wheel-zoom is debounced to ≤ 60 events / s.

## Audio attenuation

- Default master cap is **−12 dBFS**, well below the loudness recommended
  by ITU-R BS.1770-4 for headphone listening.
- A single keystroke (`M`) mutes the master bus instantly.
- All long sustains respect the user-set release time so notes never
  cut off abruptly.

## Keyboard

- Tab order matches reading order in the top bar.
- All buttons are focusable; focus rings use `outline: 2px solid
  rgba(255,255,255,.7)`.
- The route engine and LR fit can be triggered without a mouse.

## Reduced motion preference

`@media (prefers-reduced-motion: reduce)` disables the hover
opacity-fade on the camera HUD and shortens the route step rate's
crossfade to zero.

## Known limitations

- Screen readers have no semantic exposure of the canvas; alt-text
  describes the field at a coarse level. A live region announces
  hovered galaxy names (`role="status" aria-live="polite"`).
- Internationalisation is partial; UI strings are English with
  Turkish-friendly punctuation.
