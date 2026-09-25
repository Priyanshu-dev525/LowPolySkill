# Optimization & Topology

## 1. Topology rules for low poly

1. **Quads for modeling, triangles for delivery.** Model in quads where convenient; export/game assets end up triangulated — make sure the triangulation is deliberate, not accidental.
2. **No n-gons in the final mesh.** Anything above 4 sides triangulates unpredictably.
3. **No poles with 5+ edges on visible smooth surfaces.** They cause shading pinches. On flat-shaded low poly this is much less critical.
4. **No interior faces.** Anything never seen from any allowed camera angle gets deleted.
5. **No coplanar overlapping faces.** Z-fighting. Delete the hidden one or offset by ~0.5–1% of object size.
6. **No duplicate vertices or overlapping geometry.** Weld within a tolerance of ~0.1% of object size.
7. **No zero-area faces or zero-length edges.** They break normals and exports.
8. **Consistent winding.** All normals outward; run a recalculation pass.
9. **Manifold where it matters.** Closed volumes if the model is 3D-printed, booleaned, or used for physics. Open shells are fine for games as long as the open edges are hidden.
10. **Edge flow follows form.** On anything that bends or deforms, run loops across the joint, not along it.

---

## 2. The optimization checklist (in order)

Run these in this order — the order matters because later steps clean up after earlier ones.

| # | Action | What it targets |
| - | ------ | --------------- |
| 1 | Delete interior / hidden faces | Undersides, enclosed volumes, faces behind other faces |
| 2 | Delete backfaces of flat elements | The back of a wall, the underside of a plane that never flips |
| 3 | Collapse bevels to 1 segment | Bevel width and segments are the fastest triangle multiplier |
| 4 | Reduce cylinder side counts to the minimum that reads | 16 → 12 → 10 → 8; test at target camera distance |
| 5 | Dissolve redundant edge loops | Loops that no longer hold a shape after other changes |
| 6 | Dissolve coplanar faces into one face | Flat panels built from several coplanar quads |
| 7 | Weld duplicate vertices | Post-boolean, post-mirror cleanup |
| 8 | Replace modeled detail with material | Bolts, panel lines, grilles, text, patterns |
| 9 | Mirror instead of modeling | Symmetric halves |
| 10 | Instance instead of copying | Wheels, foliage, hardware, background props |
| 11 | Merge static same-material meshes | Draw-call reduction (weigh against LOD and frustum culling) |
| 12 | Only now: decimate / reduce | Last resort; it destroys intentional topology |

**Triangle accounting in the plan:** list the estimate before and after optimization in Section 8, and show the two or three biggest savings.

---

## 3. Where NOT to optimize

Do not remove geometry that:
- defines the silhouette from any allowed camera angle
- forms an intersection line between two materials
- is needed for the part to bend, animate, or deform
- holds a UV seam needed for texturing
- creates the contact shadow that grounds the object
- is the difference between "recognizable" and "generic blob"

Low poly is not "fewest possible triangles." It is "no triangle that does no work."

---

## 4. Triangle cost reference

| Primitive | Tris (typical low-poly settings) |
| --------- | -------------------------------- |
| Plane | 2 |
| Cube | 12 |
| Cube with 1-segment bevel | 12 (corner triangles only, ~36 with full bevel) |
| Cone, 6 sides | 12 |
| Cylinder, 8 sides, capped | 32 |
| Cylinder, 12 sides, capped | 48 |
| UV sphere 8×6 | ~96 |
| Icosphere subdivision 0 | 20 |
| Icosphere subdivision 1 | 80 |
| Torus 12×8 | 192 |
| Capsule 8×2 | ~64 |

Use these to sanity-check the per-part polygon levels in the component table: they must add up to roughly the budget in Section 2.

---

## 5. LOD strategy (real-time)

| LOD | Triangles vs LOD0 | What to remove |
| --- | ----------------- | -------------- |
| LOD0 | 100% | Full detail |
| LOD1 | 45–60% | Dissolve loops, drop cylinder sides, remove accents and small parts |
| LOD2 | 20–30% | Merge components into silhouette masses, remove functional gaps |
| LOD3 / impostor | 5–10% or a billboard | Single silhouette shape with averaged vertex colors |

Rules: keep the silhouette identical between LOD0 and LOD1. LOD transitions should not pop — remove small high-contrast details first. Screen-size thresholds: LOD0 > 40% of screen height, LOD1 15–40%, LOD2 4–15%, LOD3/cull below 4%.

---

## 6. Collision guidance

| Object | Recommended collider |
| ------ | -------------------- |
| Box-ish prop | 1 box collider |
| Vehicle | 1 box for the body + 1 capsule/cylinder per wheel, or a convex hull |
| Character | Capsule |
| Complex static environment | Convex decomposition (a few hulls), or a simplified hand-made mesh |
| Small debris / foliage | None, or a single cheap box |
| Anything the player walks into | Convex only |

Collision meshes should be a small number of convex shapes — never a copy of the render mesh. In the plan, state the collider type and rough dimensions.
