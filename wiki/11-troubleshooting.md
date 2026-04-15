# 11 · Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Blank canvas, no error in console | Canvas measured at 0 × 0 during a panel toggle | Already guarded; resize the window once. If it persists, hard-reload. |
| Console: `createImageData … width or height is zero` | Same as above, in older builds | Update to current `sky_patch_interactive.html`; `display()` now retries `layout()`. |
| Console: `Cannot read properties of undefined (reading 'ra_deg' / '_x')` | Stale `hovered` / `routeStart` / `routeEnd` after a catalogue rebuild | `buildCatalogForField` now re-resolves these via `sdss_name`. Update to current build. |
| No sound at all | `AudioContext` suspended (browser policy) | Click anywhere in the page once. Modern browsers require a user gesture before audio resumes. |
| Distorted / clicky sound | Master cap too high or extreme F1/F2 gain | Open Sound-check, lower master cap (try −18 dBFS), reset formant gains. |
| LR Fit reports “singular system” | All training rows identical or λ = 0 with K ≥ N | Add more diverse rows, or set λ ≥ 0.01. |
| Clicking a galaxy opens SDSS in a new tab | You are holding a modifier (Alt / ⌘ / Ctrl / Shift) or using middle-click, which is the **explicit link shortcut** | Release the modifier and left-click normally; a plain click sonifies the galaxy when sonification is active. |
| Clicking a galaxy does nothing (no sound, no link) | Sonification is off and you used a plain click | Enable at least one mapping in Sonification Settings. The toast above the canvas tells you this when it happens. |
| Click-sonified note is too short / too long | `♪ click` slider in the bottom-left status strip is set to an extreme | Drag the slider; values range 0.05–4 s. Selection is remembered across sessions in `localStorage`. |
| LR Fit succeeds but R² is negative | Mappings are inconsistent (same input → different outputs) | Audit your training rows; remove contradictory ones. |
| Hovered galaxy reads as `null` after FoV change | Galaxy scrolled out of the field | Pan back; the re-resolve only succeeds for galaxies still visible. |
| Camera HUD covers the scale-bar | Window resized below 480 px wide | The HUD is positioned above the scale-bar at `bottom: 52px`; if a custom CSS overrides, restore it. |
| Font-size selector seems to do nothing | Old `body { font-size }` rule cached | Hard-reload (Cmd/Ctrl + Shift + R). Current build uses CSS `zoom`. |
| “Fill inputs from galaxy” shows red status | Empty catalogue, no inputs selected, or id out of range | Status text says which; load a dataset, enable an input, or use a valid id. |
| Performance < 30 fps on a fresh laptop | More than ~5000 visible galaxies | Zoom in to reduce visible count, or close other tabs (Web Audio shares timer thread). |
| Sudden dangerous volume / stuck note / runaway sound | Any cause — preset error, graph mode overlap, browser glitch | Press <kbd>Ctrl</kbd>/<kbd>⌘</kbd> + <kbd>.</kbd> or click the red 🚨 PANIC button in the top bar. It is the last node before the speakers so nothing can bypass it. Click a second time to restore the previous level exactly. |
| Audio sounds harsh / boomy / fatiguing on your playback chain | Room, headphone, or hearing-accommodation issue | Open 🎛 EQ from the top bar, try the *Soft* or *Low-cut* preset, or adjust individual bands. Default is flat (transparent). *Reset* returns to flat. |
| EQ does not seem to change the sound | All bands are at 0 dB (default), or every band is Bypassed | Move a band's gain slider, or click its Bypass button to re-enable it. |
| PANIC button label says "SOUND MUTED — click to resume" | Panic mute is engaged | Click the button again, or press <kbd>Ctrl</kbd>/<kbd>⌘</kbd> + <kbd>.</kbd> |

## Useful console commands

```js
// Snapshot current synth state (used by the LR fill button)
window.__oscReadAll();

// Hard-cap the master bus (in dBFS, e.g. -18)
window.__audioSetCapDb(-18);

// Show the active catalogue length
cat.length;

// Dump the current Dijkstra route as ids
route.map(g => g.sdss_name);

// Emergency mute (same as the 🚨 PANIC button and Ctrl/⌘+.)
window.__panicEngage();
window.__panicRelease();
window.__panicActive();

// Inspect or reset the 5-band EQ
window.__eqReadBand(0);              // { freq, gainDb, q, bypass }
window.__eqSetBand(2, { gainDb: -3 });
window.__eqReset();                  // all bands to flat 0 dB
```

## Reporting a bug

Open an issue on the repo with:

1. Browser + version, OS.
2. Steps to reproduce.
3. Console log (open dev-tools, copy errors).
4. If audio-related: master cap value, formant settings.
5. If catalogue-related: a minimal CSV that triggers the bug.
