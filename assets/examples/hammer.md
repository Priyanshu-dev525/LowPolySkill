# LOW-POLY MODEL PLAN — Example: Claw Hammer (text-only request)

> Worked example. User request: *"Make a low-poly hammer."* No images, no software named.
> Note how vague input is handled: assumptions are stated, not asked about.

## 1. Model Overview

**Object:** Claw hammer (curved-claw carpenter's hammer)
**Intended use:** Small game prop / inventory asset, readable at 1–3 m
**Visual style:** Stylized-hard-surface, chunky, flat shaded
**Input type:** Text only

**Assumptions** (none of these were specified by the user):
1. **Curved claw hammer**, not a sledge, ball-peen, or mallet. *Blocking assumption — a different hammer type changes the head entirely.*
2. **Wooden handle** with a rubber grip; modern, not antique.
3. **Real-time / game use**, so triangle economy and 1–3 materials matter.
4. **Not animated** — no separate pivots needed beyond the object origin.
5. Modeled at rest, standing on its handle butt, viewed from a 3/4 angle.

## 2. Target Style

- **Polygon density:** very simple prop — **120–250 triangles**. Hammers are small and rarely inspected closely; the silhouette does all the work.
- **Silhouette:** the cross-shape (long handle + perpendicular head) plus the claw hook. The claw must hook visibly downward — without it the model reads as a generic mallet.
- **Shading:** fully **flat**. Facets on the handle cylinder and a hard chamfer on the face are what sell it as low poly.
- **Proportions:** realistic-leaning, but handle thickened ~10% and claw enlarged ~15% so both survive at low resolution.
- **Level of detail:** silhouette + functional parts. No surface detail at all.
- **Estimated triangle budget:** **~140 triangles.**

## 3. Coordinate System

- **Up axis:** Y
- **Forward direction:** −Z (the face of the hammer points toward +X, the claw toward −X)
- **Origin:** center of the handle butt, at ground level (Y = 0)
- **Base unit:** total hammer height (butt to top of head) = **10.0 units**
- **Overall dimensions:** **4.3 W (X, claw tip to face) × 10.0 H (Y) × 1.3 D (Z)**

## 4. Component Breakdown

| Part | Base Shape | Dimensions | Position | Rotation | Polygon Level |
| ---- | ---------- | ---------- | -------- | -------- | ------------- |
| Handle | Cylinder, 6 sides, capped | L 8.6, r 0.45 → 0.36 | (0, 4.3, 0) | 0, 0, 0 | Very low — 20 tris |
| Grip | Cylinder, 6 sides, capped | L 2.8, r 0.56 | (0, 1.7, 0) | 0, 0, 0 | Very low — 20 tris |
| Head block | Cube | 3.2 × 1.15 × 1.15 | (0.30, 9.30, 0) | 0, 0, 0 | Low — 36 tris (chamfered) |
| Striking face | Cube | 0.50 × 1.25 × 1.25 | (2.15, 9.30, 0) | 0, 0, 0 | Low — 24 tris (chamfered) |
| Claw | Extruded 4-sided tapered profile | L 1.7, 0.9 → 0.35 wide | (−2.05, 8.90, 0) | 0, 0, +18° | Very low — 18 tris |
| Collar | Cylinder, 6 sides | L 0.35, r 0.40 | (0, 8.30, 0) | 0, 0, 0 | Very low — 20 tris |

*Total ≈ 138 triangles.*

## 5. Step-by-Step Construction

### 5.1 Handle (6-sided cylinder, ~20 tris)

1. Create a cylinder with **6 sides**, radius 0.45, height 8.6, **caps enabled**.
2. Keep it vertical along Y. Scale the **top** vertex ring to 0.80× (radius 0.36) to taper toward the head.
3. Move to (0, 4.30, 0) so it spans Y = 0.00 to 8.60.
4. No rotation.
5. Rotate the whole cylinder 30° about Y so a flat facet faces the camera in the default 3/4 view (flat facets catch light better than an edge-on seam).
6. Leave it un-subdivided — no loop cuts are needed.
7. Assign `MAT_Wood`. Shading: **flat**.
8. *Optional:* nudge the two lower rings +2% in Z to give the handle a very slight forward bow (reads as "used", costs 0 triangles).

### 5.2 Grip (6-sided cylinder, ~20 tris)

1. Create a 6-sided cylinder, radius 0.56, height 2.8, capped.
2. Move to (0, 1.70, 0) — covering Y = 0.30 to 3.10, i.e. the lower third of the handle.
3. Rotate to match the handle's 30° Y rotation so the facets align.
4. Select the top and bottom rings and scale them to 0.94× for a subtle barrel shape.
5. Select the bottom cap face and **delete it** — it is hidden inside/under the handle (the grip is a sleeve over the handle, so its end caps are interior).
6. Assign `MAT_Rubber`. Shading: **flat**.

### 5.3 Head block (cube, ~36 tris)

1. Create a cube. Scale to **3.2 (X) × 1.15 (Y) × 1.15 (Z)**.
2. Move to **(0.30, 9.30, 0)** — it spans X = −1.30 to 1.90, Y = 8.72 to 9.87.
3. No rotation; it is perpendicular to the handle by construction.
4. Select the four long edges (the ones running along X) and **bevel once**, width 0.10, **1 segment**. This is the only bevel in the model — it creates the highlight line that makes the head read as steel.
5. Select the +X end face (at X = 1.90) and leave it flat — the face block will abut it exactly.
6. Select the −X end face (at X = −1.30) and leave it flat — the claw base will abut it.
7. Delete nothing; the head is a closed solid.
8. Assign `MAT_Steel`. Shading: **flat**, hard edges on the bevel.

### 5.4 Striking face (cube, ~24 tris)

1. Create a cube. Scale to **0.50 (X) × 1.25 (Y) × 1.25 (Z)** — slightly larger in cross-section than the head so it steps out.
2. Move to **(2.15, 9.30, 0)** — its −X face sits exactly at X = 1.90, flush with the head's +X face.
3. No rotation.
4. Select the four long edges and bevel once, width 0.08, 1 segment.
5. Select the **−X face** (the one buried against the head) and **delete it** — never visible, and its absence prevents z-fighting.
6. Assign `MAT_Steel_Bright` so the face reads brighter than the head body — this value difference is what makes the hammer read across a room.
7. Shading: **flat**.

### 5.5 Claw (extruded tapered profile, ~18 tris)

1. Draw a 4-point polygon in the XY side view: a wedge 1.70 long, 0.90 tall at the root, tapering to 0.35 tall at the tip, with the top edge straight and the bottom edge curving upward toward the tip.
2. Extrude along Z by 0.90, then **taper the extrusion to 0.75×** so the claw narrows in depth as well as height.
3. Move to **(−2.05, 8.90, 0)** — its root face sits at X = −1.30, flush with the head's −X face, and it spans down to about X = −2.90, Y = 8.55.
4. Rotate **+18° about Z** so the tip hooks downward (in this orientation, +Z rotation lowers the −X tip).
5. Select the root face and **delete it** (buried in the head).
6. Select the tip's two lower edges and bevel once, width 0.06, 1 segment, so the tip does not look razor-sharp at distance.
7. Assign `MAT_Steel`. Shading: **flat**.
8. *Optional at ~6 extra triangles:* split the tip into two prongs with a single notch cut; only worth it if the camera gets close to the head.

### 5.6 Collar (6-sided cylinder, ~20 tris)

1. Create a 6-sided cylinder, radius 0.40, height 0.35, capped.
2. Move to (0, 8.30, 0) — just below the head, where the handle enters the head's shadow.
3. Match the handle's 30° Y rotation.
4. Scale the top ring to 1.05× so it flares slightly where it meets the head.
5. Delete the bottom cap (hidden against the handle).
6. Assign `MAT_Steel`. Shading: **flat**.
7. *Cheap alternative:* delete the collar entirely and put a 0.35-tall `MAT_Steel` band on the handle's upper faces. Saves 20 triangles if the budget is tight.

## 6. Assembly

- **Stack order:** handle (Y 0 → 8.60) → head block (Y 8.72 → 9.87) → face and claw abutting the head's ±X ends → grip sleeved over the lower handle → collar at the handle/head junction.
- **Junction detail:** the handle top (Y = 8.60) does **not** reach the head's bottom (Y = 8.72). Extend the handle by 0.12 (or lower the head to 9.18) so the handle visibly enters the head — a 0.12 gap here is the single most common way a hammer model looks broken. Recommended fix: raise the handle's top ring to Y = 8.85 so it is solidly buried inside the head block.
- **Face and claw** are separate objects that abut the head with deleted shared faces. They can be joined to the head if the material is shared; keep the face separate only if you want its brighter material isolated.
- **Pivot:** the object origin stays at (0, 0, 0) — the handle butt. This is correct for placing the hammer on a surface and for a "standing in a toolbox" pose.
- **No z-fighting:** coplanar shared faces (face/head, claw/head, grip/handle caps) were deleted on one side of each pair.

## 7. Materials

| Material | Color | Roughness | Metallic | Shading |
| -------- | ----- | --------- | -------- | ------- |
| `MAT_Wood` | `#6B4A2F` | 0.80 | 0.0 | Flat |
| `MAT_Rubber` | `#26282B` | 0.90 | 0.0 | Flat |
| `MAT_Steel` | `#6E7378` | 0.38 | 1.0 | Flat, hard edges |
| `MAT_Steel_Bright` | `#9AA1A8` | 0.28 | 1.0 | Flat, hard edges |

**Palette**

| Slot | Hex | Used on |
| ---- | --- | ------- |
| Dominant | `#6B4A2F` | Handle |
| Secondary | `#6E7378` | Head, claw, collar |
| Accent | `#9AA1A8` | Striking face (the focal point) |
| Neutral | `#26282B` | Grip |

**Detail deferred to material:** wood grain, the handle's manufacturer stamp, the claw's seam, the head's weight marking. All are tertiary — at 140 triangles they would cost more than the whole model and read as noise. If a slightly richer look is needed later, a 256×256 base-color map on the handle only.

## 8. Low-Poly Optimization

- **Delete:** bottom cap of the grip, the face's buried −X face, the claw's root face, the collar's bottom cap. (−6 tris and 4 z-fighting risks removed.)
- **Dissolve:** nothing — there are no redundant loops by construction.
- **Weld:** after joining the face and claw to the head, weld within 0.01 units; do **not** weld across the bevel, or the highlight is lost.
- **Mirror:** the hammer is symmetric across the XY plane (Z = 0). Model the +Z half and mirror if you want to guarantee symmetry — but at this poly count it is faster to model the whole thing and eyeball it.
- **Instance / reuse:** the handle and grip are the same 6-sided cylinder at different scales — build one, duplicate, rescale.
- **Not worth optimizing further:** below ~110 triangles the claw stops hooking and the model becomes a mallet.
- **Triangle estimate:** 162 before cleanup → **~138 after.**

## 9. Final Validation

| # | Check | Pass condition | Status |
| - | ----- | -------------- | ------ |
| 1 | Silhouette recognizable | As a solid black shape: long shaft + perpendicular block + a downward hook on one side = hammer | ☐ |
| 2 | Proportions correct | Handle 8.6 + head 1.15 ≈ 9.75, plus taper ≈ 10.0 total (±3%) | ☐ |
| 3 | No unnecessary geometry | Every face is exterior or load-bearing; 4 buried faces deleted | ☐ |
| 4 | Normals correct | No inverted normals after the mirror/weld pass | ☐ |
| 5 | Materials assigned | Every face has one of the 4 materials; no defaults | ☐ |
| 6 | No duplicate geometry | Weld test at 0.01 passes | ☐ |
| 7 | Polygon budget respected | ~138 tris is inside 120–250 | ☐ |
| 8 | Ready for export | Scale = 1, origin at handle butt, transforms applied, Y-up | ☐ |

## 10. Optional Software Implementation

No target software specified — universal plan only.

*(If the user later names a package, generate the Section 10 block from `references/10-software-implementation.md`: operation mapping, axis/unit conversion, the flat-shading gotcha for that package, and the export preset.)*
