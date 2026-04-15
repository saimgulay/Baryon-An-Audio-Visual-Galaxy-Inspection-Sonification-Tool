# 14 · HCI evaluation

Baryon's usability layer is grounded in established HCI frameworks. This
page documents which techniques were applied, where they are
instantiated in the code, and how they were evaluated. **No existing
feature was removed** during this pass — every change is additive.

## 1. Frameworks referenced

| Framework | Use in Baryon |
|---|---|
| Nielsen (1994) — 10 usability heuristics | Sectioned coverage below. |
| Shneiderman & Plaisant — 8 Golden Rules | Shortcut system, consistent panel model, closure on route planning. |
| Fitts (1954) — target-size / travel law | Enlarged HUD targets, status strip at screen edge, cheatsheet reachable from a persistent button. |
| Hick–Hyman (1952) — decision cost | Progressive disclosure: menus hide advanced groups until requested. |
| Miller (1956) — 7 ± 2 | Top-bar limited to 7 primary affordances; sonification split into 3 groups. |
| Norman (2013) — signifiers / feedback / constraints | Grab-cursor on canvas, toast feedback, AudioContext resume prompt. |
| Wickens (2008) — multiple-resource theory | Pairing visual inspection with aural sonification uses orthogonal perceptual channels, reducing interference. |
| WCAG 2.2 AA | Focus-visible rings, AAA contrast, reduced-motion, aria-live toasts. |

## 2. Heuristic-by-heuristic coverage (Nielsen)

### H1 — Visibility of system status
- Persistent bottom-left status strip (`#hciStatusBar`) shows: audio state
  (idle / suspended / live / muted), live catalogue size, route status.
- Toast stack (`#hciToastStack`, `role="status" aria-live="polite"`)
  announces every significant action to screen readers and sighted users.

### H2 — Match between system and the real world
- Camera HUD uses cardinal glyphs (N / E / S / W); zoom uses `＋ − ⤢`.
- Audio level uses dBFS rather than raw gain — matches how audio
  engineers think. Master cap defaults to a polite −12 dBFS.

### H3 — User control and freedom
- Every panel closes with `Esc`.
- Onboarding tour offers both *Skip* and a permanent *Don't show again*.
- Replay-tour button in the status strip restores it.
- Mute toggles both directions; the previous gain is retained so
  unmute is a true inverse.

### H4 — Consistency and standards
- All panels share the `.ss-panel` class and an identical open/close
  contract; mutual exclusion is centralised.
- Keyboard shortcuts follow Western conventions: `Space` to play,
  `Esc` to close, arrows to pan, `?` or `F1` for help.
- Focus rings follow WCAG 2.2 focus-visible.

### H5 — Error prevention
- Fit buttons validate endpoints before routing (toast: "Pick a start
  and an end galaxy first").
- LR solver refuses to run on empty catalogues or unselected inputs
  with a specific status message (not an opaque throw).
- `display()` guards canvas sizes to prevent the
  `createImageData width-or-height-is-zero` class of errors during
  panel transitions.

### H6 — Recognition rather than recall
- Every top-bar control has a `title` tooltip.
- Keyboard cheatsheet is one key away (`?`) and also reachable from a
  labelled button in the status strip.
- Status strip continuously surfaces the three facts a user most often
  wants to re-check: is audio alive, how many galaxies are loaded, is
  a route ready.

### H7 — Flexibility and efficiency of use
- Global keyboard shortcuts for frequent actions (play, mute, slew,
  zoom, fit, open panels).
- Tour shows **only on first run**; power users never see it again.
- All shortcuts are suppressed while the user is typing, so typed
  input is never hijacked.

### H8 — Aesthetic and minimalist design
- Status strip at 66 % opacity with backdrop blur — visible but never
  distracting.
- Camera HUD defaults to 55 % opacity, lifts to 100 % on hover.
- Progressive disclosure keeps Phonetics / Syntax / Semantics collapsed
  behind one menu button until opened.

### H9 — Help users recognise, diagnose, and recover from errors
- Toast kinds `ok` / `warn` / `err` with distinct left borders.
- Rank-deficient ridge regression throws a **specific** message rather
  than returning NaN; UI surfaces it verbatim.
- Stale `hovered` / `routeStart` / `routeEnd` are now re-resolved via
  `sdss_name` after catalogue rebuild, preventing the prior
  `Cannot read '_x' of undefined` class of crashes.

### H10 — Help and documentation
- In-app **❓ How to** panel (12 sections + TOC).
- `F1` / `?` open it from anywhere.
- `wiki/` contains 13 detailed sub-pages.

## 3. Fitts's law applications

| Target | Placement | Size |
|---|---|---|
| ❓ How to | Top-bar right side, high-contrast fill | ≥ 32 × 24 px |
| Camera D-pad | Screen-edge anchored (infinite edge = zero travel cost on edge-bound targets) | 22 × 22 px |
| Cheatsheet *Got it* | Modal foot, default focus | ≥ 80 × 28 px |
| Status-strip buttons | Bottom-left, always visible | ≥ 64 × 20 px |

Frequent actions live on screen edges (infinite effective width under
Fitts). Very frequent actions are duplicated to a keyboard shortcut so
travel is eliminated.

## 4. Measurement plan (formative)

Recommended between-subjects protocol for follow-up evaluation.

| Metric | Definition | Target |
|---|---|---|
| Time to first audible note | From page load to first audible voice through the synth | ≤ 90 s median, untrained users |
| Task success — route | Fraction of users completing *"hear a sonified route between two galaxies you pick"* without assistance | ≥ 0.90 |
| Error rate | Toast-observed warnings or errors per completed task | ≤ 1.0 mean |
| Recognition test | After 24 h, user recalls what F1 / ADSR / Sérsic n control | ≥ 0.60 precision |
| SUS (Brooke 1996) | 10-item System Usability Scale, post-session | ≥ 72 ("good" per Bangor et al. 2008) |

Instrumentation for the above is already in place: the toast pipeline
records every significant action, the status strip exposes audio and
route state, and the tour emits a visible terminal event. Wiring these
to an opt-in telemetry endpoint is a one-function change and deliberately
*not* done by default (privacy / WCAG-respect).

## 5. Accessibility audit snapshot

| WCAG 2.2 criterion | Baryon state |
|---|---|
| 1.4.3 Contrast (Minimum) AA | Body text 14:1 (AAA); accent buttons 7:1 (AA) |
| 1.4.11 Non-text contrast | Focus rings and HUD borders ≥ 3:1 |
| 1.4.12 Text spacing | Supported; CSS uses `zoom`, not `font-size`, so UA overrides survive |
| 2.1.1 Keyboard | Every panel, tour, and cheatsheet reachable via keyboard; `Esc` exits |
| 2.3.3 Animation from interactions | `prefers-reduced-motion` disables toast slide-in and HUD opacity-fade |
| 2.4.7 Focus visible | `:focus-visible` outline on every interactive control |
| 4.1.3 Status messages | `role="status" aria-live="polite" aria-atomic="true"` on toast stack |

Known limitations: the `<canvas>` is not semantically exposed — a live
region announces hovered galaxy names as a coarse substitute. A full
SVG fallback is out of scope for this release.

## 6. Case study — redesigning the canvas click

**Symptom.** A plain left-click on a galaxy previously opened the
SDSS DR17 Explore page in a new tab. This violated three heuristics
at once: H3 (user control and freedom — the action was irreversible
and hijacked focus), H5 (error prevention — no way to disarm the
side-effect), and H7 (flexibility — the most common action, "hear
this galaxy," required a 3-step route detour).

**Redesign.**

- **Primary action (plain click) = sonify the clicked galaxy.**
  Single-target Fitts cost; one note emitted through the current
  sonification mapping. Works the moment any mapping is active; no
  route required.
- **Duration control** surfaced in the persistent status strip rather
  than buried in a panel: `♪ click` slider (0.05–4 s, default 0.8 s),
  persisted in `localStorage` so the decision survives sessions.
- **Link access preserved, not removed.** The SDSS Explore link stays
  reachable via four orthogonal paths — (a) modifier-click (Alt / ⌘ /
  Ctrl / Shift), (b) middle-click, (c) the side-panel link, (d) the
  address bar URL template in the schema. The hover tooltip signposts
  both behaviours.
- **Error recovery.** If sonification is off when a user clicks, a
  toast explains exactly what to enable — Nielsen H9.

**Heuristic gains.**

| Heuristic | Before | After |
|---|---|---|
| H3 user control | Click = irreversible tab-open | Click = reversible sound; mute with M |
| H5 error prevention | No guard rail | Guarded by `__sonifActive` + toast |
| H7 flexibility | 1 way to hear a galaxy (route) | 2 ways (click or route); modifier for link |
| H9 error recovery | None on mis-click | Friendly toast with remedy |

**Measurement implications.** Expected reduction in
time-to-first-audible-note: the previous minimum was "enable mapping
+ pick start + pick end + press Play" ≈ 4 targets; the new minimum is
"enable mapping + click one galaxy" ≈ 2 targets. Under Card, Moran &
Newell's (1983) KLM model this halves the expert task time for the
atomic inspection case.

## 6b. Case study — safety-critical PANIC button and optional EQ

**Symptom.** Audio-driven interfaces have a known failure mode: a
misconfigured preset, a graph-mode overlap, or a browser timer glitch
can produce an uncomfortably loud or sustained tone. The only
previous remedy was "find and close the right panel", which violates
Nielsen H3 (user control and freedom) under stress and H5 (error
prevention) because it places the emergency path behind normal
navigation targets.

**Redesign — 🚨 PANIC.**

- A dedicated kill-gain node (`panicKill`) is inserted as the *last*
  node before `AudioContext.destination`. No other part of the audio
  graph can route around it, so its behaviour is provably sufficient:
  if `panicKill.gain = 0`, the output is silent.
- The trigger is a persistent red button in the top bar, sized per
  Fitts (≥ 88 × 28 px), and a keyboard shortcut
  (<kbd>Ctrl</kbd>/<kbd>⌘</kbd> + <kbd>.</kbd>) reachable from any focus.
- The button is a true toggle: on engage it caches the previous
  master level; on release it restores that level exactly. This
  respects H3 (reversibility) and avoids the "accidental destruction
  of a prior setting" failure mode.
- State is announced in three modalities: the button label changes to
  "SOUND MUTED — click to resume", `aria-pressed` updates for screen
  readers, and the status-strip audio indicator flips to *muted*
  (H1, H9, WCAG 4.1.3).

**Redesign — 🎛 Frequency EQ (optional).**

- A five-band parametric EQ is inserted between `masterIn` and the
  limiter. All bands default to 0 dB, i.e. fully transparent, so the
  default audio response is unchanged (Norman — defaults should
  match prior expectations).
- The EQ is discoverable from the top bar but never forced on the
  user. Presets (*Low-cut*, *Presence +*, *Soft*) lower the
  Hick–Hyman decision cost for users who have a hearing-accommodation
  need but do not know the numerical parameters.
- Per-band *Bypass* and global *Reset* provide fine-grained reversal
  (H3). The EQ is placed *before* the limiter so any boost is still
  bounded by the Sound-check ceiling — aligning two safety layers
  without either redundancy or gaps.

**Heuristic gains.**

| Heuristic | Before | After |
|---|---|---|
| H1 visibility | Audio state is a single status dot | Status dot + PANIC label + aria-pressed all agree |
| H3 user control | Close panels to stop sound | One click or one chord; reversible |
| H5 error prevention | Loud preset can reach speakers | EQ cap and PANIC gate form two independent safety layers |
| H9 error recovery | Unmount / reload to recover | Toggle restores the previous level exactly |
| WCAG 4.1.3 | Mute was implicit | Status changes are announced via live region |

## 7. Design rationale — what was *not* changed

- **No modal stealing of audio**. AudioContext resumes only on a true
  user gesture (pointer or key), per modern browser policy and Nielsen
  H3.
- **No auto-playing sonification**. Sonification starts only on explicit
  *Play route* or keyboard `Space`.
- **No telemetry**. Privacy by default; any analytics is opt-in and
  requires explicit user code.
- **No feature removed**. This pass adds a usability layer; every
  previously documented feature remains accessible through both its
  original affordance and, where applicable, a new shortcut.

## 8. Evaluation summary

Applying the frameworks above yields a layered system with (i) a
first-run orientation aid for novices, (ii) persistent status feedback
during routine use, (iii) keyboard-driven efficiency shortcuts for
expert use, and (iv) targeted error prevention and recovery at every
level. The usability layer is implemented as ~300 lines of additive,
name-scoped code (`hciLayer` IIFE); it holds no private state that
other modules depend on, so removal is safe should future redesigns
require it. Under the heuristics above the current build passes a
Nielsen walk-through without category-level gaps and meets WCAG 2.2 AA
on the instrumented UI surface.

## References

- Brooke, J. (1996). SUS: A quick and dirty usability scale. *Usability Evaluation in Industry.*
- Bangor, A., Kortum, P. T., & Miller, J. T. (2008). An empirical evaluation of the System Usability Scale. *Int. J. Hum.-Comput. Interact.*, 24(6), 574–594.
- Fitts, P. M. (1954). The information capacity of the human motor system. *J. Exp. Psychol.*, 47(6), 381–391.
- Hick, W. E. (1952). On the rate of gain of information. *Q. J. Exp. Psychol.*, 4(1), 11–26.
- Miller, G. A. (1956). The magical number seven, plus or minus two. *Psychol. Rev.*, 63(2), 81–97.
- Nielsen, J. (1994). Heuristic evaluation. In *Usability Inspection Methods*, Wiley.
- Norman, D. A. (2013). *The Design of Everyday Things*, revised ed.
- Shneiderman, B., Plaisant, C., Cohen, M., et al. (2016). *Designing the User Interface*, 6th ed.
- W3C. (2023). *Web Content Accessibility Guidelines 2.2.*
- Wickens, C. D. (2008). Multiple resources and mental workload. *Hum. Factors*, 50(3), 449–455.
