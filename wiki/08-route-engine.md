# 08 · Route engine

A “route” is an ordered sequence of galaxies the synth visits in order.
Two route algorithms ship in Baryon:

## 1. Dijkstra over a k-NN graph (default)

A symmetric k-nearest-neighbour graph is built over the visible
catalogue using angular separation (great-circle, not pixel distance).
Default `k = 6`, capped by the catalogue size. Edge weight is the
angular separation in arcseconds.

Dijkstra's algorithm finds the shortest path from `routeStart` to
`routeEnd`. Complexity is `O((V + E) log V)` using a binary heap; for
the bundled field this is sub-millisecond.

This route honours the local sky topology — adjacent galaxies tend to
be near each other on the sphere — which makes the resulting
sonification feel spatially coherent.

## 2. Greedy nearest-step (toggle)

Starting at `routeStart`, repeatedly jump to the nearest unvisited
galaxy until `routeEnd` is reached. Faster, but produces a noticeably
zig-zaggy traversal; useful as a baseline.

## Building the graph

```js
function knnGraph(cat, k) {
  // for each i, sort all j by angularSep(i, j), take first k
  // store edges as [j, w] pairs in adj[i]
}
function angularSep(a, b) {
  // standard haversine on (RA, Dec) in radians
}
```

Reasonable performance up to ~10⁴ nodes without spatial indexing. For
larger fields a kd-tree on (cos δ cos α, cos δ sin α, sin δ) would be a
straightforward upgrade.

## Re-routing

Any change to `routeStart`, `routeEnd`, the catalogue, or `k` triggers
a full rebuild and re-solve. After `buildCatalogForField` rebuilds the
catalogue (e.g. on FoV change), stale references are re-resolved by
`sdss_name`:

```js
hovered    = _refind(hovered);
routeStart = _refind(routeStart);
routeEnd   = _refind(routeEnd);
```

`_refind` returns `null` if the galaxy has scrolled out of the field;
the UI handles this gracefully.

## Playback

The audio scheduler walks the route at a step rate set in the
Sonification panel. For each galaxy:

1. Resolve all enabled mappings on that galaxy.
2. Apply the merge rule per output.
3. Trigger one ADSR voice.
4. Wait `step_ms`.

In **graph mode**, voices overlap with stereo pan controlled by RA, so
dense regions sound as cluster-like swells.
