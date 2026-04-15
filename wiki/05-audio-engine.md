# 05 · Audio engine

The synth is a custom Web Audio graph designed to be expressive enough for
phonetic-style mappings while staying broadcast-loudness safe.

## Signal chain

```
OscillatorNode (PeriodicWave, 16 harmonics)
    │
    ├── BiquadFilterNode F1 (peaking)
    ├── BiquadFilterNode F2 (peaking)
    └── BiquadFilterNode F3 (peaking)
            │
            └── userGain (ADSR-shaped) →
                    masterIn →
                        EQ₁ → EQ₂ → EQ₃ → EQ₄ → EQ₅ (5-band parametric, optional) →
                            masterLim (DynamicsCompressor as soft-knee limiter) →
                                masterCap (hard gain ceiling) →
                                    panicKill (emergency mute gate) →
                                        AudioContext.destination
```

Every voice instantiates its own oscillator + formants but shares the
master bus.

## Master-bus extensions

### Frequency EQ (optional)

Five peaking biquads are inserted between `masterIn` and `masterLim`.
They default to a flat response (gain 0 dB on every band) so the EQ is
transparent unless the user opens the 🎛 EQ panel and adjusts it.

| Band | Default centre (Hz) | Gain range | Q range |
|---|---|---|---|
| 1 | 80    | −24 … +24 dB | 0.1 … 18 |
| 2 | 250   | −24 … +24 dB | 0.1 … 18 |
| 3 | 1 000 | −24 … +24 dB | 0.1 … 18 |
| 4 | 4 000 | −24 … +24 dB | 0.1 … 18 |
| 5 | 12 000 | −24 … +24 dB | 0.1 … 18 |

The EQ sits *before* the limiter and cap, so any boost is still
bounded by the Sound-check ceiling. Three presets are exposed
(*Low-cut*, *Presence +*, *Soft*) plus a per-band *Bypass* and a
global *Reset* that returns all bands to flat 0 dB.

### PANIC emergency mute

`panicKill` is a dedicated `GainNode` inserted as the **last** node
before `AudioContext.destination`. Because nothing else in the graph
can route around it, forcing its gain to 0 silences every voice —
including stuck notes, graph-mode overlaps, and any future audio path
that is connected to the destination.

The toggle is exposed as:

```js
window.__panicEngage()   // gain → 0 (remembers previous level)
window.__panicRelease()  // restores previous level
window.__panicActive()   // → boolean
```

and is driven by the top-bar 🚨 PANIC button (<kbd>Ctrl</kbd>/<kbd>⌘</kbd> + <kbd>.</kbd>
keyboard shortcut).

## PeriodicWave (16 harmonics)

The waveform is built from `real[k]` and `imag[k]` Fourier coefficients
for `k = 0…15`. The first slider is DC (left at 0); sliders 1…15 set the
relative amplitude of harmonics 2…16. The “Sound-check” panel exposes
preset buttons (sine, triangle, square, saw, voiced approximations).

## Formant filters

Three biquad **peaking** filters in series approximate vocal-tract
resonances:

| Filter | Default centre (Hz) | Default Q | Default gain (dB) |
|---|---|---|---|
| F1 | 700 | 6 | +14 |
| F2 | 1220 | 8 | +12 |
| F3 | 2600 | 9 | +10 |

These defaults sit near the schwa/[ə]; the Phonetics group in the
Sonification panel can drive any of them.

## ADSR envelope

The user-gain node is automated per note:

```
attack:  0.00 → 1.00 over A seconds  (linearRampToValueAtTime)
decay:   1.00 → S      over D seconds
sustain: hold at S until note-off
release: S    → 0      over R seconds
```

A, D, R are in seconds; S is dimensionless gain (0…1).

## Master limiter

`masterLim` is a `DynamicsCompressor` configured as a brickwall-ish
limiter:

| Parameter | Value |
|---|---|
| threshold | −6 dB |
| knee | 0 dB |
| ratio | 20 |
| attack | 1 ms |
| release | 120 ms |

Followed by `masterCap`, a `GainNode` whose value is set in dBFS by the
Sound-check panel (default −12 dBFS). True-peak overshoot is bounded by
the cap; the limiter handles transient peaks above threshold.

This conforms to the digital broadcast loudness spirit of
**ITU-R BS.1770-4**: peak ≤ 0 dBFS at all times, with the user able to
target a comfortable listening level.

## Determinism

Audio is parameter-driven; no random oscillators, no noise generators in
the audible path. Re-playing the same route with the same mappings and
the same osc state produces the same waveform sample-for-sample (within
the floating-point determinism guarantees of the host browser).

## API for tests and the LR panel

```js
window.__oscReadAll()    // → { amp, freq, envA…envR, fmtF1…fmtW3, h0…h15 }
window.__audioSetCapDb(d) // hard cap in dBFS

// Frequency EQ
window.__eqBandCount()                 // → 5
window.__eqReadBand(i)                 // → { freq, gainDb, q, bypass }
window.__eqSetBand(i, { freq, gainDb, q, bypass })
window.__eqReset()                     // all bands to flat 0 dB

// PANIC emergency mute
window.__panicEngage()
window.__panicRelease()
window.__panicActive()                 // → boolean
```

These are deliberately exposed on `window` so the LR “⤓ Fill outputs from
osc” button can snapshot the synth state into training rows.
