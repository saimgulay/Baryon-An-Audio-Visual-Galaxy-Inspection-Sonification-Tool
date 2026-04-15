# 01 · Quick start

Five minutes from cold open to a sonified route across a real SDSS field.

## Prerequisites

- A modern browser (Chromium 110+, Firefox 110+, Safari 16+).
- Audio output (headphones recommended for stereo panning).
- The single file `sky_patch_interactive.html`. No build step, no server.

## Open

Double-click `sky_patch_interactive.html`, or drag it onto a browser tab. The
viewer boots with the bundled SDSS DR8 sub-field (~2300 galaxies) already in
memory. The first paint should be visible within ~500 ms on a 2020-era laptop.

## The 60-second tour

1. **Drag** the canvas → the telescope slews. Hold and drag at the edge for
   continuous motion.
2. **Wheel** → zoom (FoV halves/doubles at each detent). Touchpad pinch works
   too.
3. **Hover** a galaxy → the side panel shows its short-key record (RA, Dec,
   redshift, magnitudes, half-light radius, stellar mass, …).
4. **Click** → set the route start. **Click** a second galaxy → set the end.
5. Press **▶ Play route**. The route engine builds a Dijkstra path across the
   k-NN proximity graph and plays each galaxy in turn through the synth.

## Fastest path to sound: click-to-sonify

No route required.

1. Top-bar → **Sonification Settings** → enable any mapping (e.g.
   redshift → F1 under Phonetics).
2. Top-bar → **🔊 Sound-check** → confirm master cap **−12 dBFS**.
3. Click any galaxy on the canvas. You'll hear one note synthesised
   from its catalogue values.
4. The `♪ click` slider in the bottom-left status strip sets the note
   duration (0.05–4 s; your choice persists across sessions).

To open the SDSS Explore page for a galaxy instead of sonifying it,
**Alt-click** (or ⌘-click / Shift-click / Ctrl-click / middle-click)
on the canvas, or use the *"object summary ↗"* link in the right-hand
side panel.

## First sonified route

1. Top-bar → **Sonification Settings** → switch on the **Phonetics** group
   (e.g. map redshift → vowel formant, magnitude → amplitude).
2. Top-bar → **🔊 Sound-check** → set master cap to **−12 dB** before you
   touch headphones.
3. Click two galaxies, press **▶**. You should hear a sequence of short
   vowel-like notes whose pitch and timbre track the catalogue values.

## Save and reload

The viewer is stateless between sessions. Settings (envelope, formants, etc.)
are not persisted by design — every demo starts from a known initial state.
Export trained linear-regression models as JSON from the LR panel if you want
to keep them.

## Where to go next

- [02 · Architecture](02-architecture.md) — what the file actually contains.
- [06 · Sonification mapping](06-sonification-mapping.md) — how inputs become
  sounds.
- [11 · Troubleshooting](11-troubleshooting.md) — if something looks off.
