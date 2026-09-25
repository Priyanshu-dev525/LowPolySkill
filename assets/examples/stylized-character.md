# LOW-POLY MODEL PLAN — Example: Stylized Adventurer (text + Godot)

> Worked example. User request: *"Low-poly stylized adventurer, game-ready for Godot, third-person."*
> Demonstrates: character decomposition, relative units, mirror modeling, joint loops, and a named engine in Section 10.

## 1. Model Overview

**Object:** Stylized human adventurer (androgynous, cloaked, with a short sword)
**Intended use:** Third-person game character, Godot, seen at 3–12 m
**Visual style:** Chunky stylized, large head, short limbs, fully flat shaded
**Input type:** Text only

**Assumptions**
1. Humanoid biped in a T-pose for rigging. *Blocking — a posed or quadruped body changes everything.*
2. Cloak is a simple cape shell, not cloth-simulated.
3. Face is a mask of planes (eyes, brow, mouth) — no sculpted features.
4. One material atlas of flat colors (or 4 materials) is enough; no textures.
5. Height ≈ 1.6 m real; authored at 10 units.

## 2. Target Style

- **Polygon density:** hero character — **800–1,800 triangles**. Face and hands get a disproportionate share.
- **Silhouette:** big head, triangular cloak, short thick legs, a sword at the hip. The cloak is the identity feature.
- **Shading:** fully **flat**.
- **Proportions:** stylized — head ≈ 2.4 / 10, legs shortened, hands oversized.
- **Level of detail:** silhouette + functional parts (cloak, belt, sword). Face is 6–8 planes.
- **Estimated triangle budget:** **~1,200 triangles** including the sword.

## 3. Coordinate System

- **Up axis:** Y
- **Forward direction:** −Z
- **Origin:** center of the feet contact, ground plane Y = 0
- **Base unit:** total height = **10.0 units**
- **Overall dimensions:** **3.2 W (X, including cloak) × 10.0 H (Y) × 2.0 D (Z)** in T-pose (arms add ~2.4 per side)

## 4. Component Breakdown

| Part | Base Shape | Dimensions | Position | Rotation | Polygon Level |
| ---- | ---------- | ---------- | -------- | -------- | ------------- |
| Pelvis | Cube (chamfered) | 1.40 × 0.90 × 0.90 | (0, 3.85, 0) | 0, 0, 0 | Low — 36 tris |
| Torso | Cube (tapered) | 1.70 × 2.40 × 1.00 | (0, 5.50, 0) | 0, 0, 0 | Low — 44 tris |
| Head | Icosphere subdiv 1, scaled | 2.20 × 2.40 × 2.00 | (0, 8.70, 0) | 0, 0, 0 | Medium — 80 tris |
| Neck | Cylinder 6 sides | d 0.55, H 0.40 | (0, 7.35, 0) | 0, 0, 0 | Very low — 20 tris |
| Upper arm L/R | Cylinder 6 sides | d 0.42, L 1.40 | (±1.20, 6.20, 0) | 0, 0, ±90° | Very low — 24 tris each |
| Lower arm L/R | Cylinder 6 sides | d 0.36, L 1.20 | (±2.50, 6.20, 0) | 0, 0, ±90° | Very low — 24 tris each |
| Hand L/R | Cube (block) | 0.50 × 0.35 × 0.70 | (±3.35, 6.20, 0) | 0, 0, 0 | Very low — 24 tris each |
| Upper leg L/R | Cylinder 6 sides | d 0.55, L 1.70 | (±0.40, 2.70, 0) | 0, 0, 0 | Very low — 24 tris each |
| Lower leg L/R | Cylinder 6 sides | d 0.42, L 1.50 | (±0.40, 1.10, 0) | 0, 0, 0 | Very low — 24 tris each |
| Foot L/R | Cube | 0.45 × 0.30 × 0.90 | (±0.40, 0.15, −0.20) | 0, 0, 0 | Very low — 12 tris each |
| Cloak | Extruded polygon | 3.00 × 4.80 × 0.12 | (0, 5.40, 0.55) | −8°, 0, 0 | Low — 48 tris |
| Belt | Torus 8×4 or cube ring | 1.50 × 0.22 × 1.00 | (0, 4.30, 0) | 0, 0, 0 | Very low — 32 tris |
| Face planes | 6 planes | eyes 0.35, brow 0.90, mouth 0.40 | on head front | — | Very low — 12 tris |
| Sword | Cube + tapered box | L 2.80, blade 0.18 × 0.08 | (−1.10, 3.60, 0.20) | 0, 0, −20° | Very low — 36 tris |

*Total ≈ 1,180 triangles. Model +X half of the body, mirror across X = 0. Head, cloak, belt, and sword are centered and not mirrored as halves.*

## 5. Step-by-Step Construction

### 5.1 Pelvis and torso

1. Create a cube. Scale to **1.40 × 0.90 × 0.90**. Move to (0, 3.85, 0). Bevel all edges once, width 0.08, 1 segment. Assign `MAT_Cloth`. Flat shading.
2. Create a cube. Scale to **1.70 × 2.40 × 1.00**. Move to (0, 5.50, 0) so it sits on the pelvis (pelvis top Y = 4.30, torso bottom Y = 4.30 — they share a plane; delete the buried faces).
3. Select the **bottom** ring of the torso and scale to 0.82× so it tapers into the pelvis.
4. Select the **top** ring and scale to 0.90× in Z (flatten the chest slightly).
5. Add **one loop cut** at Y ≈ 6.20 (shoulder height) so the arms have a clean attach ring.
6. Assign `MAT_Cloth`. Flat shading.

### 5.2 Head and neck

1. Create an **icosphere, subdivision 1** (80 tris). Scale non-uniformly to **2.20 × 2.40 × 2.00**.
2. Move to (0, 8.70, 0) — bottom of the head at Y ≈ 7.50.
3. Flatten the bottom 4–6 faces slightly so the neck has a seating plane.
4. Create a 6-sided cylinder, diameter 0.55, height 0.40, at (0, 7.35, 0). Delete both caps (buried). Assign `MAT_Skin`.
5. **Face:** three planes for the eyes (two 0.35 × 0.22 ovals approximated as 4-sided polygons) at ( ±0.38, 8.75, −0.95); one brow plane 0.90 × 0.12 at (0, 9.05, −0.92); one mouth plane 0.40 × 0.10 at (0, 8.20, −0.95). Push them 0.02 in front of the head surface. Assign `MAT_FaceDark`.
6. Head: `MAT_Skin`. Flat shading. Do **not** subdivide further.

### 5.3 Limbs (model one side, mirror)

1. **Upper arm:** 6-sided cylinder, diameter 0.42, length 1.40. Rotate 90° about Z. Place pivot at the **shoulder** end. Position so the inner end sits in the torso at (±0.85, 6.20, 0). Add **one loop** near the elbow.
2. **Lower arm:** 6-sided cylinder, diameter 0.36, length 1.20. Pivot at the elbow. Taper the wrist ring to 0.80×.
3. **Hand:** a cube 0.50 × 0.35 × 0.70, slightly rotated −10° about Y so it reads as a mitten. No fingers — at this style they become noise. Optional: one extra box 0.18 × 0.12 × 0.28 as a thumb.
4. **Upper / lower leg:** same recipe, vertical. Pivots at hip and knee. Add one loop at each joint. Taper the ankle to 0.75×.
5. **Foot:** cube 0.45 × 0.30 × 0.90 at (±0.40, 0.15, −0.20) so it overhangs forward. Bevel the front top edge once.
6. **Mirror** the entire limb set across X = 0. Recalculate normals. Do not negative-scale.

### 5.4 Cloak, belt, sword

1. **Cloak:** draw a 6-point polygon in the XY view — a trapezoid 3.00 wide at the shoulders, 2.40 at the hem, 4.80 tall, with a slight outward belly. Extrude 0.12 in Z. Move to (0, 5.40, 0.55) and rotate −8° about X so it drapes back. Delete the inner face if it z-fights the torso. Assign `MAT_Cloak`.
2. **Belt:** a flattened torus (8 major × 4 minor) or a cube ring 1.50 × 0.22 × 1.00 at (0, 4.30, 0). Assign `MAT_Leather`.
3. **Sword:** blade = tapered box 2.20 × 0.18 × 0.08; guard = box 0.70 × 0.10 × 0.18; grip = 6-sided cylinder length 0.55, diameter 0.14; pommel = cube 0.16. Assemble along the blade axis. Place at the left hip (−1.10, 3.60, 0.20), rotated −20° about Z. Assign `MAT_Steel` / `MAT_Leather` on the grip. Keep as a **separate object** parented to the pelvis (it can be sheathed/unsheathed).

## 6. Assembly

- **Stack:** feet (Y 0) → legs → pelvis (3.40–4.30) → torso (4.30–6.70) → neck → head (7.50–9.90). Sum ≈ 10.0.
- **Shoulders:** upper-arm inner ends bury 0.15 into the torso. Delete the buried caps.
- **Cloak** is a separate shell, not welded, so it can be hidden or swapped. Offset 0.05 from the back to avoid z-fighting.
- **Pivots for animation:** pelvis at its center; each limb segment at the **proximal joint**; head at the base of the skull; sword at the grip.
- **T-pose:** arms along +X / −X, palms down, feet parallel, looking −Z.

## 7. Materials

| Material | Color | Roughness | Metallic | Shading |
| -------- | ----- | --------- | -------- | ------- |
| `MAT_Skin` | `#E0B492` | 0.70 | 0.0 | Flat |
| `MAT_Cloth` | `#3D5A80` | 0.80 | 0.0 | Flat |
| `MAT_Cloak` | `#2B3A4A` | 0.85 | 0.0 | Flat |
| `MAT_Leather` | `#6B4A2F` | 0.75 | 0.0 | Flat |
| `MAT_Steel` | `#8A9099` | 0.35 | 1.0 | Flat, hard edges |
| `MAT_FaceDark` | `#2A2420` | 0.80 | 0.0 | Flat |

**Palette**

| Slot | Hex | Used on |
| ---- | --- | ------- |
| Dominant | `#3D5A80` | Tunic |
| Secondary | `#2B3A4A` | Cloak (silhouette) |
| Neutral | `#E0B492` | Skin |
| Accent | `#8A9099` | Sword |

**Detail deferred to material:** stitching, hair strands, belt buckle engraving, eye highlights (a 1-vertex color spec on the eye planes is enough).

## 8. Low-Poly Optimization

- **Delete:** buried limb caps, torso/pelvis shared faces, cloak inner face if unused, icosphere faces hidden against the neck.
- **Dissolve:** any loop that is not at a joint.
- **Weld:** after mirroring limbs, weld at 0.01 along X = 0 only on the torso/pelvis/head — not on separate limb objects.
- **Mirror:** body across X = 0. Cloak, belt, head, sword are centered uniques.
- **Instance:** none at character scale (the sword pommel/guard could share a cube primitive internally).
- **Do not reduce:** the head below icosphere subdiv 1 (it becomes a pyramid); joint loops (deformation collapses).
- **LOD:** LOD1 (~600 tris) merges hands into cubes, drops face planes to 2, cloak to 12 tris. LOD2 (~250) is a capsule body + box head + cloak plane.
- **Triangle estimate:** ~1,280 before cleanup → **~1,180 after.**

## 9. Final Validation

| # | Check | Pass condition | Status |
| - | ----- | -------------- | ------ |
| 1 | Silhouette recognizable | Big head + triangular cloak + hip sword = adventurer, not a generic humanoid | ☐ |
| 2 | Proportions correct | Head 2.4 + neck 0.4 + torso 2.4 + pelvis 0.9 + legs 3.2 + feet 0.3 ≈ 10.0 | ☐ |
| 3 | No unnecessary geometry | No fingers, no interior mouth, no modeled hair | ☐ |
| 4 | Normals correct | Mirrored limbs outward; cloak faces out | ☐ |
| 5 | Materials assigned | 6 materials, face planes dark, no defaults | ☐ |
| 6 | No duplicate geometry | Weld on the centerline; limbs are unique objects not duplicated meshes overlapping | ☐ |
| 7 | Polygon budget respected | ~1,180 inside 800–1,800 | ☐ |
| 8 | Ready for export | glTF, Y-up, meters, origin at feet, T-pose, pivots at joints | ☐ |

## 10. Optional Software Implementation — Godot

**Import:** export **glTF 2.0 / GLB** from the DCC. Godot is Y-up, right-handed, meters. Author 10 units = 1.6 m → scale the root to **0.16** on import, or author at real meters.

**Shading:** Godot respects split normals in glTF. Use `StandardMaterial3D` with shading mode per-material; disable unnecessary specular. Vertex colors work if you collapse to one material later.

**Setup:**
- Scene root: `CharacterBody3D` with a `CapsuleShape3D` (radius 0.35 m, height 1.6 m).
- Mesh: `MeshInstance3D` child. Sword as a separate `MeshInstance3D` parented to a `BoneAttachment3D` on the pelvis/hand.
- Skeleton: generate a simple humanoid skeleton (Godot 4 `Skeleton3D`) with bones at the pivots listed in Assembly.
- LOD: `GeometryInstance3D` visibility ranges, or separate LOD meshes swapped by distance.

**Gotchas:**
1. Apply all transforms before export or Godot shows sheared normals.
2. Double-sided cloak: enable `cull_disabled` on `MAT_Cloak` if both sides can be seen.
3. Keep material count ≤ 6 or merge into a palette atlas to stay in one draw call.

No target-specific modeling tools are required — follow Sections 1–9 in any DCC, then export glTF.
