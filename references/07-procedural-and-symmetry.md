# Procedural Modeling & Symmetry

## 1. Symmetry types

| Type | Axis / rule | Parts to model once |
| ---- | ----------- | ------------------- |
| **Bilateral (mirror)** | Reflection across one plane (typically X = 0 for characters, or the vehicle centerline) | Arms, legs, eyes, ears, wheels, fenders, headlights, wings, doors |
| **Radial** | Rotation about one axis by 360/n | Wheel spokes, gear teeth, flower petals, tower columns, dome ribs, screw threads |
| **Translational** | Repeated offset along a line or curve | Fence pickets, windows, floor bands, railings, treads, bricks, pipes |
| **Grid / surface** | Repeated placement on a surface | Roof tiles, brick courses, screws, studs, scales |
| **Path / curve** | Placement along a spline | Cables, hoses, chains, roads, vines, ropes |

For each, state: the unit, the axis/plane, the count, the spacing, and the variation strategy.

---

## 2. Procedural candidates

Reach for procedural construction whenever you see these:

| Element | Unit | Duplication strategy |
| ------- | ---- | -------------------- |
| Wheels | 1 wheel (10–12 sides) | Instance 4× at corner positions; mirror hubs |
| Wheel spokes | 1 spoke box | Radial array 5–8×, merged into the hub |
| Fence posts / pickets | 1 tapered box | Linear array with spacing; vary height ±5% |
| Windows | 1 framed window unit | 2D array across facade and floors; vary lit/unlit by material |
| Bricks / blocks | 1 box | Offset grid array; rotate a few units ±2° |
| Trees | 1 trunk + 1 canopy cluster | Scatter instances with randomized rotation and uniform-varied scale |
| Buildings | 1 floor module | Stack with variation per floor (window pattern, ledge, color) |
| Bolts / rivets / studs | 1 tiny cylinder or **a dark material dot** | Array, or prefer material — bolts are usually tertiary |
| Spikes / teeth | 1 cone | Radial or linear array; randomize length ±10% |
| Leaves / foliage | 1 crossed plane or 1 leaf cluster | Instance 10–40× on the canopy; never model individually |
| Pipes / rails | 1 pipe segment | Path array along a curve |
| Stairs / treads | 1 step | Linear array up a slope |
| Chains | 1 torus or 1 low-side torus | Path array with alternating 90° rotation |
| Crowd / background props | 1 base prop | Instance with per-instance color variation |

---

## 3. Writing a procedural instruction

Specify all six of these, or the instruction is not executable:

```
Unit:        <what one element is, with dimensions>
Generator:   <mirror | linear array | radial array | curve array | surface scatter>
Axis / Path: <the plane, axis, or curve it follows>
Count:       <n>  (or "n = floor(length / spacing)")
Spacing:     <distance or angle>
Variation:   <rotation / scale / color randomization, with ranges>
Weld / Join: <whether the copies merge into one mesh or stay as instances>
```

Example:

```
Fence: Unit = tapered box 0.18 W × 1.6 H × 0.18 D, flat shaded.
Generator: linear array along +X. Spacing 0.34. Count = floor(wall_length / 0.34).
Variation: height ±5%, rotation about Y ±1.5°, two rail boxes bridging at Y = 0.4 and Y = 1.2.
Weld: keep as instances until export, then merge into one mesh with one material.
```

---

## 4. Instancing vs copying

| | Instance | Copy (duplicate) |
| - | -------- | ---------------- |
| Memory | Shares one mesh | Duplicates it |
| Editing | Edit one, all update | Edit each |
| Variation | Per-instance transform and (usually) material only | Full per-copy geometry edits |
| Use for | Wheels, foliage, background props, repeated hardware | Anything that must differ in shape, or that needs unique UVs/deformation |

Rule: **instance everything until a part needs to differ.** Then convert only that one.

---

## 5. Mirror modeling workflow

1. Model the half on the positive side of the mirror plane (e.g. +X).
2. Do **not** model the centerline seam geometry; leave the edge open at the plane.
3. Apply the mirror (or keep it live while iterating).
4. Weld/merge vertices along the seam after applying — a duplicate seam causes shading splits.
5. Recalculate normals: mirrored geometry often needs them flipped.
6. Break symmetry deliberately: equipment, hair, pose, damage, or an asymmetric color accent. Perfect symmetry looks CG.

**Centerline caution:** if a part crosses the mirror plane (a nose, a hood, a spine), model it as one piece centered on the plane; do not mirror it or you get an interior wall.

---

## 6. Radial symmetry workflow

1. Model one unit with its pivot at the center of rotation.
2. Set the count: 6–8 for coarse, 10–16 when it must read as a circle.
3. Radial array 360° about the axis.
4. Merge the touching vertices between neighbors, or leave separate if each unit is an instance.
5. For a round object made of flat facets (a low-poly wheel), 10–12 sides with flat shading reads as round enough and stays cheap.

---

## 7. Randomization parameters worth exposing

When the plan feeds a procedural system, list the tunable parameters so the generator has knobs:

| Parameter | Typical range | Applies to |
| --------- | ------------- | ---------- |
| `count` | integer | arrays |
| `spacing` / `pitch` | float | arrays, treads |
| `radius` | float | radial arrays |
| `length` / `height` | float | pickets, spikes, legs |
| `jitter_position` | 0–10% of spacing | natural scatter |
| `jitter_rotation` | 0–15° | foliage, debris |
| `scale_variance` | 0.85–1.15 | scatter |
| `bend_angle` | float | tapered/bent parts |
| `seed` | integer | reproducibility |
| `lod_level` | 0–3 | LOD chains |
