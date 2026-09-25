# LOW-POLY MODEL PLAN — Example: Pickup Truck (3 reference images, Unreal target)

> Worked example. User request: *"Turn these photos into a low-poly pickup truck for Unreal. It's a drivable hero vehicle."*
> Demonstrates: multi-image analysis, Observed/Inferred/Recommended labeling, instancing, game-ready block, and a Section 10 for a named target.

## 1. Model Overview

**Object:** Mid-size pickup truck (crew cab, short bed)
**Intended use:** Drivable hero vehicle, third-person camera, Unreal Engine
**Visual style:** Stylized-realistic hard surface — believable proportions, simplified surfaces
**Input type:** Multiple reference images (3) + text

**Reference Read**

| Image | View | What it confirms |
| ----- | ---- | ---------------- |
| 1 | Front 3/4, daylight | Overall proportions, cab/bed split, grille shape, headlight layout, wheel arch shape |
| 2 | Side, slightly low | Wheelbase vs body length, roofline, window count (2 per side), bed depth |
| 3 | Rear 3/4, shade | Tailgate, taillight layout, rear bumper, exhaust side |

- **Observed:** 4 wheels; 2 doors per side; separate cab and bed; roofline slightly tapered rearward; 5-lug hubs; rectangular headlights; front grille spans nearly the full front width; side mirrors on stalks; wheel arches flare slightly beyond the body; bed walls at approximately seat-belt height relative to the cab.
- **Inferred:** the far side mirrors the near side (only one flank is clearly visible in each image); the underside is flat with a frame and an exhaust run; the tailgate is a flat panel hinged at the bottom; door handles exist at approximately Y = 2.0 (visible as a shape, not resolved in detail).
- **Recommended (not visible in any reference):** underside is a flat plate with a simple box frame — no suspension geometry is modeled except what is visible below the arches; no interior beyond a seat block, a steering wheel torus, and a dashboard box visible through the glass; the bed interior is a simple open box.
- **Recognizability drivers:** boxy cab + separate open bed; tall stance with large wheels; broad rectangular grille; flared wheel arches; two-tone separation of glass and paint.
- **Detail deferred to material:** door handles, panel seams, door shut lines, the manufacturer badge, wheel lug nuts, tire tread, panel gaps, the tailgate handle, and any text on the tailgate.
- **Silhouette risks:** at low poly, a pickup is dangerously close to "a box with wheels." Mitigations: exaggerate the cab/bed height step, widen the wheel arch flare to 0.12 units, raise the ride height to 0.55, and taper the roof rearward by 8% so the cab does not read as a plain cube.

**Assumptions**
1. Modern crew-cab pickup, not a classic or a chassis-cab work truck. *Blocking — changes the cab entirely.*
2. Wheels do not need to steer visually at LOD0 (steering is a separate note).
3. Real-world length ≈ 5.4 m; the plan is authored at 10 units and scaled at export.

## 2. Target Style

- **Polygon density:** hero/large object — **900–1,600 triangles** at LOD0. It is the focus of the screen for long stretches, so it gets a real budget, but it is not a cinematic asset.
- **Silhouette:** must read as "pickup" at 30 m from the outline alone. Priority features: cab/bed step, arch flares, stance, grille mass.
- **Shading:** mostly **flat**, with **selective smoothing**: wheel cylinder bands smoothed and cap edges hardened so the tires do not look like stop signs; everything else flat.
- **Proportions:** realistic measured proportions — no stylization, because a distorted vehicle reads as a toy.
- **Level of detail:** silhouette + functional parts + major surface detail (arches, grille bars, light housings, window frames). No interior detail beyond a silhouette-blocking block.
- **Estimated triangle budget:** **~1,050 triangles** with all parts as planned; headroom to 1,600 for extras.

## 3. Coordinate System

- **Up axis:** Y (author here; Unreal is Z-up and the conversion is handled at export)
- **Forward direction:** **+X** (the truck faces +X)
- **Origin:** center of the wheel-contact plane, at ground level, mid-wheelbase — the Unreal standard for vehicle pivots
- **Base unit:** total vehicle length = **10.0 units** (≈ 5.4 m real → export scale 0.54)
- **Overall dimensions:** **10.0 L (X) × 3.30 H (Y) × 4.00 W (Z)**, including mirrors

## 4. Component Breakdown

| Part | Base Shape | Dimensions | Position | Rotation | Polygon Level |
| ---- | ---------- | ---------- | -------- | -------- | ------------- |
| Body lower | Cube (chamfered) | 9.6 × 1.25 × 3.80 | (0, 1.38, 0) | 0, 0, 0 | Low — 60 tris |
| Cab | Cube (tapered) | 3.2 × 1.15 × 3.50 | (1.10, 2.58, 0) | 0, 0, 0 | Low — 44 tris |
| Roof | Cube (tapered) | 3.0 × 0.18 × 3.40 | (1.05, 3.16, 0) | 0, 0, 0 | Very low — 20 tris |
| Bed walls + floor | 3 cubes / extruded U-profile | 4.4 × 0.75 × 3.70 | (−2.60, 2.05, 0) | 0, 0, 0 | Low — 40 tris |
| Tailgate | Cube | 0.22 × 0.72 × 3.60 | (−4.75, 2.05, 0) | 0, 0, 0 | Very low — 12 tris |
| Hood | Cube (tapered) | 2.0 × 0.22 × 3.60 | (3.70, 2.16, 0) | 0, 0, 0 | Very low — 24 tris |
| Grille | Inset panel + 3 bars | 0.20 × 0.90 × 3.10 | (4.85, 1.45, 0) | 0, 0, 0 | Low — 36 tris |
| Front bumper | Extruded profile | 0.45 × 0.55 × 3.80 | (4.85, 0.90, 0) | 0, 0, 0 | Very low — 20 tris |
| Rear bumper | Extruded profile | 0.35 × 0.45 × 3.70 | (−4.85, 0.85, 0) | 0, 0, 0 | Very low — 20 tris |
| Wheel arch ×4 | Extruded curved profile | r 1.05, width 0.22 | (±3.05, 1.35, ±1.90) | 0, 90°, 0 | Very low — 24 tris each (instanced) |
| Windshield | Plane (raked) | 0.30 × 1.05 × 3.30 | (2.72, 2.60, 0) | 0, 0, −22° | Very low — 2 tris + 18 frame |
| Side windows ×2 | Plane | 0.10 × 0.85 × 3.20 | (1.10, 2.62, ±1.76) | 0, 0, 0 | Very low — 2 tris + 16 frame each |
| Rear window | Plane | 0.10 × 0.80 × 3.10 | (−0.48, 2.62, 0) | 0, 0, 0 | Very low — 18 tris w/ frame |
| Wheel ×4 | Cylinder 12 sides, capped | d 1.70, width 0.55 | (±3.05, 0.85, ±1.72) | 0, 90°, 0 | Low — 44 tris each (instanced) |
| Hub ×4 | Cylinder 8 sides + inset | d 0.85, depth 0.08 | (±3.05, 0.85, ±1.99) | 0, 90°, 0 | Very low — 20 tris each (instanced) |
| Headlight ×2 | Cube | 0.18 × 0.35 × 0.90 | (4.84, 1.55, ±1.30) | 0, 0, 0 | Very low — 12 tris each |
| Taillight ×2 | Cube | 0.16 × 0.55 × 0.70 | (−4.83, 1.55, ±1.35) | 0, 0, 0 | Very low — 10 tris each |
| Mirror ×2 | Cube + stalk | 0.28 × 0.30 × 0.16 (+stalk) | (2.35, 2.45, ±2.05) | 0, 0, 0 | Very low — 26 tris each |
| Exhaust | Cylinder 6 sides | d 0.16, L 1.2 | (−4.60, 0.55, 1.30) | 0, 0, 90° | Very low — 20 tris |
| Interior block | 2 cubes + torus | seats 1.2 × 0.9 × 3.0 | (0.90, 1.95, 0) | 0, 0, 0 | Very low — 70 tris |

*Total ≈ 1,050 triangles. Instanced: wheels (44 × 4 = 176 physical, 44 unique), arches (96 physical, 24 unique), hubs (80 physical, 20 unique).*

## 5. Step-by-Step Construction

### 5.1 Body lower (cube, ~60 tris)

1. Create a cube. Scale to **9.6 (X) × 1.25 (Y) × 3.80 (Z)**.
2. Move to **(0, 1.38, 0)** — spanning Y = 0.75 to 2.00, i.e. above the wheel centers (Y = 0.85) with 0.75 of ground clearance below.
3. No rotation.
4. Select the top ring of edges and scale it 0.98× in Z so the body tumbles home slightly.
5. Select the bottom ring and scale 0.96× so the sills tuck under.
6. Bevel the four long horizontal edges once, width 0.08, 1 segment.
7. Delete the top face — it is covered by the cab, hood, and bed. Delete the bottom face only if the underside plate is added separately (recommended: keep the bottom, delete the underside plate).
8. Assign `MAT_Paint`. Shading: **flat**.

### 5.2 Cab (cube, ~44 tris)

1. Create a cube. Scale to **3.2 (X) × 1.15 (Y) × 3.50 (Z)**.
2. Move to **(1.10, 2.58, 0)** — sitting on the body top (Y = 2.00), spanning X = −0.50 to 2.70.
3. Select the **rear** face ring and scale it to 0.92× in both Y and Z — this is the 8% rearward taper that stops the cab reading as a cube.
4. Select the top edge ring and bevel once, width 0.10, to catch light at the roofline.
5. Select the front face and rotate its normal plane by −22° to match the windshield rake (or simply place the windshield plane in front of it and delete the front face behind the glass).
6. Delete the bottom face (buried against the body).
7. Assign `MAT_Paint`. Shading: **flat**.

### 5.3 Roof, hood, bed, tailgate (cubes, 20 / 24 / 40 / 12 tris)

1. **Roof:** cube 3.0 × 0.18 × 3.40 at (1.05, 3.16, 0). Taper the rear ring to 0.92× to match the cab. Bevel the perimeter once at 0.06. Delete the bottom face.
2. **Hood:** cube 2.0 × 0.22 × 3.60 at (3.70, 2.16, 0); scale the front ring to 0.90× in Z for the hood's nose taper; bevel the two long edges at 0.07; delete the bottom face.
3. **Bed:** extrude a U-shaped profile (two side walls + floor) — draw the U in the YZ plane (outer 3.70 × 0.75, wall thickness 0.14), extrude along X by 4.4, center at (−2.60, 2.05, 0). Delete the front face where it meets the cab. Cap the open top edges with a 0.06 bevel so the bed rails catch light.
4. **Tailgate:** cube 0.22 × 0.72 × 3.60 at (−4.75, 2.05, 0), flush with the bed's rear opening. Bevel the top edge at 0.05.

### 5.4 Grille (inset panel, ~36 tris)

1. Select the body's **+X front face** (at X = 4.80).
2. **Inset** it by 0.18 on all sides, leaving a painted border.
3. Extrude the inset face **inward** by 0.20 to create a recess.
4. Inside the recess, place **3 horizontal bars**: cubes 0.10 × 0.10 × 3.00, at Y = 1.15, 1.45, 1.75, X = 4.78.
5. Assign `MAT_Dark` to the recessed back face and `MAT_Trim` to the bars. Shading: **flat** on everything.
6. *Do not model a mesh pattern* — at this scale a grille mesh is pure noise. Three bars plus a dark recess read correctly and cost 36 triangles instead of 400.

### 5.5 Bumpers (extruded profiles, ~20 tris each)

1. Draw a simple C-profile in the YZ plane: 0.55 tall, 0.45 deep, with a 0.08 lip at the top.
2. Extrude along Z by 3.80 (front) / 3.70 (rear).
3. Position at (4.85, 0.90, 0) and (−4.85, 0.85, 0) so they overlap the body ends by 0.05 (buried faces deleted).
4. Assign `MAT_Trim`. Shading: **flat**.

### 5.6 Wheel arches (×4, ~24 tris each — model once, instance)

1. Draw a half-ring profile: outer radius 1.05, inner radius 0.90, spanning 0–180°.
2. Extrude along the wheel axis by 0.22.
3. Rotate 90° about Y so the ring opens downward, and position at (±3.05, 1.35, ±1.90).
4. **Instance** for the other three corners (mirror across X and Z; do not negative-scale, mirror the transform).
5. Assign `MAT_Paint` or `MAT_Trim` (a darker trim reads better on light paint). Shading: **flat**.
6. The arch flare is the single most important stylization on this model — do not reduce it below 0.18.

### 5.7 Glass (windshield, side, rear)

1. Create a **plane** for the windshield, 1.05 tall × 3.30 wide; move to (2.72, 2.60, 0); rotate **−22° about Z** so it leans back from the cab's front face.
2. Create two side window planes at (±1.76 in Z), 0.85 × 3.20, vertical.
3. Rear window plane at (−0.48, 2.62, 0), 0.80 × 3.10.
4. For each: **inset** the surrounding cab face by 0.08 and extrude **inward** by 0.05 to create a frame recess, then assign `MAT_Glass` to the plane and `MAT_Trim` to the frame.
5. Push each glass plane 0.05 inward from the frame so it sits below the surface (no z-fighting, reads as real glass).
6. Glass planes: **smooth** shading, single-sided, with a small transparency (0.75).

### 5.8 Wheels and hubs (×4 each — model once, instance)

1. Create a **cylinder, 12 sides, capped**, diameter 1.70, width 0.55.
2. Rotate 90° about **Z** (or about the axis that makes the cylinder's axis point along Z) so the tire rolls about the Z axis.
3. Move to (3.05, 0.85, 1.72).
4. Select both cap faces, inset by 0.22, and extrude inward by 0.03 to form the hub recess.
5. Bevel the two outer rim edges once, width 0.06.
6. **Shading:** smooth the cylindrical band (**soft edges**), keep the two cap rims **hard** — this is the selective smoothing that makes the tire read as round without extra polygons.
7. **Hub:** 8-sided cylinder, diameter 0.85, depth 0.08, placed in the recess at the outer cap; add 5 small boxes as lug studs if the camera gets close (recommended: skip the studs, use a material dot — *Observed: 5-lug, but at 1.70 diameter the studs are tertiary*).
8. Assign `MAT_Tire` to the band, `MAT_Trim` to the hub.
9. **Instance** to the other three corners. Set each wheel's pivot at its own center so it can spin.

### 5.9 Lights, mirrors, exhaust, interior

1. **Headlights:** cube 0.18 × 0.35 × 0.90 at (4.84, 1.55, ±1.30); bevel the front edge at 0.04; assign `MAT_Glass_Emissive`.
2. **Taillights:** cube 0.16 × 0.55 × 0.70 at (−4.83, 1.55, ±1.35); assign `MAT_Light_Red` (emissive at low strength).
3. **Mirrors:** a 0.28 × 0.30 × 0.16 shell plus a 0.20 stalk, at (2.35, 2.45, ±2.05). Mirror one across Z. Overhang the body by 0.20 so the silhouette gets a deliberate bump.
4. **Exhaust:** 6-sided cylinder, diameter 0.16, length 1.2, rotated 90° about Z, at (−4.60, 0.55, 1.30); delete the hidden end cap; assign `MAT_Metal`.
5. **Interior (visible through glass only):** two seat boxes (1.2 × 0.9 × 1.4) at (0.90, 1.95, ±0.85), a dashboard box (0.5 × 0.35 × 3.20) at (2.20, 2.05, 0), and a torus (r 0.28, 8×6) as the steering wheel at (2.05, 2.20, 0.85) rotated −20° about Z. Assign `MAT_Interior` (dark, low contrast). **No pedals, no switches, no vents.**

## 6. Assembly

- **Stack, bottom to top:** wheels (Y 0 → 1.70, centers at 0.85) → body lower (Y 0.75 → 2.00) → cab/bed/hood (Y 2.00 → 3.30) → roof → glass → trim and lights.
- **Body/arch relationship:** arches sit at Y = 1.35 with an outer radius of 1.05, so their lower edge meets the body side at Y ≈ 0.30 — they wrap the wheels with a visible 0.15 gap above the tire at full compression. Check this gap exists; a tire touching an arch reads as broken.
- **Wheels** stay as **separate objects** with individual pivots at their centers (they rotate for driving). Parent them to the vehicle root, do not merge them.
- **Arches** can be **merged into the body** (same material, never moves) — merging saves 3 draw calls.
- **Lights and mirrors** stay separate: they need their own materials and are the first things removed at LOD1/LOD2.
- **Z-fighting:** every plane that sits on a face (glass, grille bars) is offset inward by 0.03–0.05 units. Never leave two coplanar faces.
- **Roots and pivots:** vehicle root at (0, 0, 0) as defined; each wheel's pivot at its own center; no other part moves.

## 7. Materials

| Material | Color | Roughness | Metallic | Shading |
| -------- | ----- | --------- | -------- | ------- |
| `MAT_Paint` | `#2E4A5C` | 0.45 | 0.0 | Flat |
| `MAT_Trim` | `#3A3E44` | 0.55 | 0.7 | Flat |
| `MAT_Tire` | `#1F2124` | 0.92 | 0.0 | Flat (band smooth-shaded, see 5.8) |
| `MAT_Glass` | `#4A6B73` | 0.10 | 0.0 | Smooth, transparent 0.75 |
| `MAT_Glass_Emissive` | `#E8E2C4` | 0.20 | 0.0 | Flat, emission 2.0 |
| `MAT_Light_Red` | `#B23A2E` | 0.30 | 0.0 | Flat, emission 1.2 |
| `MAT_Dark` | `#15171A` | 0.85 | 0.0 | Flat |
| `MAT_Metal` | `#8A9099` | 0.35 | 1.0 | Flat |
| `MAT_Interior` | `#23262B` | 0.85 | 0.0 | Flat |

**Palette**

| Slot | Hex | Used on |
| ---- | --- | ------- |
| Dominant | `#2E4A5C` | Body paint (52% of visible surface) |
| Secondary | `#3A3E44` | Trim, arches, bumpers, hubs |
| Neutral | `#1F2124` | Tires, dark recesses |
| Accent | `#E8E2C4` | Headlights (the only bright note) |

**Detail deferred to material:** door handles and shut lines, the tailgate badge and any text, wheel lug studs, tire sidewall lettering and tread, panel gaps, the tailgate handle, wipers, and the grille mesh. All are tertiary at 1,050 triangles. If a richer look is needed: one **1024×1024** trim sheet shared across the body for panel seams, or vertex-color seam lines.

## 8. Low-Poly Optimization

- **Delete:** the body's top face (covered by cab/hood/bed), the cab's bottom face, the roof's bottom face, the hood's bottom face, buried ends of the bumpers, the exhaust's hidden cap, and the interior seat bottoms. **−7 faces, ~−14 tris.**
- **Dissolve:** nothing — no redundant loops were created.
- **Weld:** after merging arches into the body, weld at 0.01. Do **not** weld across the bevels or the paint/trim boundary — material borders must stay as hard edges.
- **Mirror:** the truck is symmetric across Z = 0. Model the +Z half (cab, glass, mirrors, lights, arches), mirror the whole half, weld the seam, then break symmetry only with the exhaust (already on +Z only).
- **Instance:** wheels (4× the same mesh), hubs (4×), arches (4×). Unique geometry: 1 wheel (44 tris) + 1 hub (20) + 1 arch (24) = 88 unique triangles serving 12 objects.
- **Reuse:** the wheel and hub work for any other vehicle in the project at a different scale. Export them as their own asset.
- **Do not reduce:** the wheel to fewer than 10 sides (it stops reading as round), or the arch flare below 0.18 (the truck stops reading as a truck).
- **LOD chain:**
  | LOD | Tris | Changes |
  | --- | ---- | ------- |
  | LOD0 | ~1,050 | Full |
  | LOD1 | ~520 | Drop mirrors, lights become recessed color patches, wheels to 8 sides, dissolve interior, merge cab+roof |
  | LOD2 | ~220 | Wheels become 6-sided, glass merges into the body as dark faces, bumpers merge into the body |
  | LOD3 | ~90 | Single silhouette mass: one extruded side profile with a flat-shaded tire block per corner |
- **Triangle estimate:** 1,180 before cleanup → **~1,050 after** → within the 900–1,600 budget with headroom.

## 9. Final Validation

| # | Check | Pass condition | Status |
| - | ----- | -------------- | ------ |
| 1 | Silhouette recognizable | As a black shape at 30 m: cab step + open bed + 4 wheels + flared arches = pickup, not an SUV or a van | ☐ |
| 2 | Proportions correct | Length 10.0 = front bumper −4.85→4.85 plus mirrors within 0.30; wheelbase 6.10 = 0.61 of length (typical 0.60–0.63) | ☐ |
| 3 | No unnecessary geometry | 7 buried faces deleted; no tertiary detail modeled | ☐ |
| 4 | Normals correct | Mirrored half has recomputed normals; no black faces at the Z = 0 seam | ☐ |
| 5 | Materials assigned | 9 materials, no default/gray faces anywhere | ☐ |
| 6 | No duplicate geometry | Weld at 0.01 passes; wheel instances are transforms of one mesh | ☐ |
| 7 | Polygon budget respected | ~1,050 tris inside 900–1,600 | ☐ |
| 8 | Ready for export | FBX, Y-up baked, 1 unit = 1 m, triangulated, modifiers applied, origin at wheel-contact center | ☐ |

**Extended:** pivots at each wheel center ☐ · collision = 1 box + 4 cylinders ☐ · LOD chain present ☐ · glass is the only transparent material ☐ · naming `VEH_Pickup_*` throughout ☐

## 10. Optional Software Implementation — Unreal Engine

**Operation mapping:** build in any DCC using the universal steps; no Unreal-specific modeling is required. Recommended DCC setup: Mirror modifier on Z with Clipping, Array/Instance for wheels, Weighted Normal or hard-edge marking for the tire cap rims.

**Axis / unit handling:**
- Author Y-up, +X forward, meters. Export **FBX with `+Z up`** (Unreal's convention) or import and rely on Unreal's conversion — the reliable path is: author in the plan's coordinates, export with **Convert Scene Unit off**, `Up Axis = Z`, `Forward = X`.
- 1 Unreal unit = 1 cm. The model is 10 units ≈ 5.4 m → set **Import Uniform Scale = 54** (or author at 540 units).
- Verify on import: the truck measures **540 × 178 × 216 cm** in Unreal.

**Normal & shading settings (critical):**
- In the FBX import options set **Normal Import Method = Import Normals** and **Recompute Normals = false**. Unreal's default recompute will smooth your flat-shaded body and destroy the low-poly look.
- Ensure the DCC exported **hard edges/split normals** on all flat-shaded parts (split the edges, do not rely on smoothing groups alone).
- Material Instances from one master `M_Vehicle_Master` with `BaseColor`, `Roughness`, `Metallic`, `EmissiveStrength` parameters — lets you make color variants with zero extra textures.

**Instancing:** wheels are separate Static Meshes parented under the vehicle; use a **Skeletal Mesh** only if the suspension animates. For background traffic, convert to Instanced Static Meshes.

**Collision:** in the Static Mesh editor, add one **box** (540 × 120 × 200, centered at Z = 90) plus **4 cylinder/capsule** colliders at the wheels; or auto-convex with a max of 8 hulls. Do not use the render mesh as collision.

**LODs:** import the LOD chain (`LOD0..LOD3` named `VEH_Pickup_LOD0` …); set screen sizes 100% / 45% / 18% / 6%; enable **LOD cull** below 2%.

**Export settings:** FBX 2020, triangulate on, apply modifiers/transforms on, embed textures off (materials are recreated in Unreal), smoothing: **export hard/soft edge data**, not just smoothing groups.

**Gotchas:**
1. Unreal's default import recomputes normals — the #1 cause of a low-poly model arriving smooth. Verify with `Lit → Wireframe` and a normals view before anything else.
2. Centimeter scale: forgetting it makes the truck 100× too small (or too large) and breaks physics.
3. Transparent glass sorts against itself; keep glass as **one** material and set it to `Translucent` with low opacity, or `Masked` if you prefer cheap sorting.
4. Nanite is not appropriate here — it will not improve a 1,050-triangle asset and can defeat the faceted shading.

**Scripted variant (if generating procedurally):** drive the plan from a Blueprint/Houdini Digital Asset exposing `length`, `wheelbase`, `wheel_diameter`, `arch_flare`, `cab_length`, `bed_length`, `paint_color`, and `lod_level` — every dimension in Section 4 becomes a parameter, and the LOD chain regenerates from the same source.
