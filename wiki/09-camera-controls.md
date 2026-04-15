# 09 · Camera HUD

The bottom-right `#camHUD` is a translucent overlay that exposes the
camera at a glance without occluding the canvas.

## Layout

- Position: `fixed; right: 10px; bottom: 52px;` (above the scale-bar).
- Default opacity: `0.55`, background `rgba(8,10,14,.18)`.
- Hover: opacity `1.0`, background `rgba(8,10,14,.72)`.
- Backdrop: `backdrop-filter: blur(4px)` for separation on bright
  fields.

## Controls

- **D-pad** (N / W / Home / E / S, 22×22 px) — slew by a step. Home
  recentres the field on the catalogue centroid.
- **Zoom** (＋ / − / ⤢, 22×20 px) — halve / double FoV / fit-all.
- **Slew slider** (`#camSlew`, 72 px) — step size 0.02° to 2°.

The readout (`#camInfo`) is shown only on hover, as a popover above
the HUD, so it never overlaps galaxy labels in the canvas.

## Pointer + wheel

Pointer drag on the canvas slews continuously; horizontal motion is
corrected by `1 / cos δ` so pixel speed maps to true sky speed
regardless of declination.

Wheel/pinch on the canvas zooms by a factor of √2 per detent. Zoom
preserves the cursor's RA/Dec so users can “zoom into” a feature.

## Why an overlay, not a window

Window panels broke the rest of the UI's mutual-exclusion model and
forced the user to dismiss them to resume browsing. The HUD stays out
of the way (low opacity), surfaces on hover, and never steals focus.
