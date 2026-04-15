# 06 · Sonification mapping

Sonification turns catalogue rows into sound. The mapping layer sits
between the catalogue and the audio engine.

## Concepts

- **Input**: a function `(galaxy) → number` plus a `[lo, hi]` range for
  normalisation. Inputs are entries of `SONIF_INPUTS` (e.g. redshift,
  magnitude, log-mass, Sérsic n, half-light radius, RA, Dec).
- **Output**: a synth parameter setter plus its range. Outputs are
  entries of `SONIF_OUTPUTS` (e.g. fundamental frequency, amplitude,
  attack time, F1 centre, harmonic *k* amplitude).
- **Mapping**: an active pair (input, output, scale). Mappings are
  grouped into **Phonetics**, **Syntax**, and **Semantics**.

## The three groups

| Group | Intent | Typical mappings |
|---|---|---|
| Phonetics | Identity / timbre of a single galaxy | redshift → vowel formants; magnitude → amplitude. |
| Syntax | How notes are sequenced | step duration ← inverse density; route order ← Dijkstra. |
| Semantics | Higher-order properties | log-mass → harmonic richness; SFR → noise/breath. |

A mapping is enabled per-checkbox; multiple mappings can target the
same output and are combined by the **merge rule**.

## Merge rule

For a given output O with N enabled mappings M₁…M_N each producing a
normalised value v_i ∈ [0, 1]:

```
v_combined = Σ wᵢ · vᵢ      (sum over enabled mappings)
v_out      = clamp(v_combined / Σ wᵢ, 0, 1)
y_out      = lo_O + v_out · (hi_O − lo_O)
```

Default weights `wᵢ = 1`. The averaging (rather than summing) keeps the
output strictly inside its declared range regardless of how many
mappings are enabled.

## Click-to-sonify (single-galaxy trigger, no route required)

In addition to route-based playback, Baryon supports an *immediate*
per-galaxy trigger. When sonification is active, a plain **left-click
on any galaxy** plays exactly one note for that galaxy through the
current mapping. No start/end endpoints and no Dijkstra solve are
needed.

- **Duration.** A slider labelled `♪ click` in the bottom-left status
  strip controls the note duration (0.05–4 s, default 0.8 s). The
  value persists in `localStorage` under `baryon.clickNoteDur`.
- **Feedback.** A toast confirms the galaxy name and duration on
  every click-note; an `aria-live` status announcement makes the
  action audible to assistive technology.
- **When sonification is off.** A plain click is a no-op with a
  friendly toast telling the user how to enable a mapping.
- **Link-discovery preserved.** The per-galaxy SDSS Explore page is
  still reachable via **Alt-click / ⌘-click / Shift-click / Ctrl-click
  / middle-click** on the canvas, or by clicking the *"object
  summary ↗"* link in the right-hand side panel for that galaxy.
  Screen-reader and keyboard-only users can reach the link from the
  side panel without depending on pointer modifiers.

Under Wickens (2008) multiple-resource theory this is the minimal
interaction that maps a single visual object to a single aural event;
under Fitts (1954) it eliminates a two-target sequence (start + end
galaxy + press Play) and collapses it to one target. Route playback
remains available unchanged for users who want temporal grammar.

## Monophonic vs graph mode

- **Monophonic** (default): one voice at a time; route plays sequentially.
- **Graph mode**: each galaxy in the route becomes a brief overlapping
  voice with stereo pan ← right ascension. Useful for sensing density.

Both modes respect the master limiter and cap.

## Worked example: redshift → vowel

1. Enable Phonetics group.
2. Mapping A: input `z` (range `[0.0, 0.3]`) → output F1 centre
   (range `[300, 900]`). Result: nearby galaxies sound like /ɑ/, distant
   galaxies drift toward /i/.
3. Mapping B: input `mr` (range `[14, 20]`) → output amplitude
   (range `[0.05, 0.6]`). Result: bright galaxies are louder.

Re-route, press ▶, and you hear a vowel sequence whose timbre encodes
distance and whose volume encodes apparent brightness.

## Discoverability

The Sonification panel only shows inputs whose underlying field exists
in the active catalogue. Loading a CSV without `lgms`, for example,
hides every log-mass mapping until the field reappears.
