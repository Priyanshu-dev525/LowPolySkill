# Software Implementation Notes

**Only read/generate this for software the user named.** The universal plan (Sections 1–9) must never depend on any of it.

Each section below: the mapping from universal concepts to that package's tools, plus the gotchas that break low-poly assets in that package.

---

## Blender

| Universal | Blender |
| --------- | ------- |
| Create primitive | `Add > Mesh` (Shift+A); set sides/radius in the redo panel (F9) |
| Extrude | `E` |
| Inset | `I` |
| Bevel | `Ctrl+B` (set segments = 1 for low poly) |
| Loop cut | `Ctrl+R` |
| Bridge | `Edge > Bridge Edge Loops` |
| Mirror | Mirror modifier (with Clipping) or `Mesh > Symmetrize` |
| Array | Array modifier; Array + Curve modifier for path arrays |
| Instance | `Alt+D` (linked duplicate) or Geometry Nodes instances |
| Boolean | Bool Tool / Mesh > Boolean; always follow with cleanup |
| Flat shading | `Object > Shade Flat`; add a **Weighted Normal** modifier with `Keep Sharp` for controlled smoothing |
| Hard edges | `Edge > Mark Sharp` + Auto Smooth (or a bevel/weighted normal) |
| Merge/weld | `M > By Distance` |
| Normals | `Shift+N` recalculate outside; `Mesh > Normals > Flip` |

**Gotchas:** apply scale (`Ctrl+A > Scale`) before export or non-uniform scale breaks normals; the Mirror modifier needs Clipping on to avoid a seam gap; triangulation happens at export, so check it in the export settings; glTF needs `+Y up` and correct unit scale (1 Blender unit = 1 m by default).

**Scripted generation:** use `bpy` — `bpy.ops.mesh.primitive_cylinder_add(vertices=8, ...)`, then manipulate `bmesh`. Prefer low-level `mesh.from_pydata(verts, edges, faces)` for procedural work, and always finish with `mesh.update()` + `mesh.validate()`.

---

## Maya

| Universal | Maya |
| --------- | ---- |
| Create primitive | `Create > Polygon Primitives` (set subdivisions in the option box) |
| Extrude | `Edit Mesh > Extrude` |
| Inset | `Edit Mesh > Extrude` with `Local Translate` off, or `Insert Edge Loop` + scale |
| Bevel | `Edit Mesh > Bevel` (segments = 1) |
| Loop cut | `Edit Mesh > Insert Edge Loop` |
| Bridge | `Edit Mesh > Bridge` |
| Mirror | `Mesh > Mirror` (check `Merge with Original`) or `Mirror Cut` |
| Array | `Edit > Duplicate Special` with transforms, or MASH |
| Instance | `Edit > Duplicate Special > Instance` |
| Boolean | `Mesh > Booleans`; run `Mesh > Cleanup` afterward |
| Flat shading | `Mesh Display > Soften/Harden Edges` → set All Hard (or `Harden Edge`) |
| Hard/soft edges | `Mesh Display > Soften/Harden` |
| Merge/weld | `Edit Mesh > Merge` (set a small distance) or `Mesh > Cleanup` |
| Normals | `Mesh Display > Reverse` / `Conform` |

**Gotchas:** Maya is Y-up (matches the plan convention); always `Delete History` and `Freeze Transformations` before export; construction history on arrays/booleans bloats scene files; use `Mesh > Cleanup` with "remove zero-area faces / lamina faces" as a final pass; Maya's default lambert1 must be replaced on every face.

---

## 3ds Max

| Universal | 3ds Max |
| --------- | ------- |
| Create primitive | `Create > Standard Primitives` (set sides/segments low) |
| Extrude | Editable Poly → `Extrude` |
| Inset | Editable Poly → `Inset` |
| Bevel | Editable Poly → `Bevel` or `Chamfer` on edges |
| Loop cut | `SwiftLoop` / `Connect` |
| Bridge | Editable Poly → `Bridge` |
| Mirror | `Mirror` tool with `Copy`, then `Weld` the seam |
| Array | `Array` / `Clone & Align` / `Spacing Tool` along a path |
| Instance | `Clone` → `Instance` (radio button) |
| Boolean | `ProBoolean` (cleaner than legacy Boolean); then `Relax`/cleanup |
| Flat shading | Assign hard smoothing groups per face, or `Clear All` smoothing groups |
| Hard/soft edges | Smoothing Groups (`Clear All` = fully faceted) |
| Merge/weld | `Edit Poly > Weld` with a small threshold |
| Normals | `Edit Normals` modifier / `Flip` |

**Gotchas:** 3ds Max is Z-up while most engines are Y-up — bake the conversion at export (`+Y-up` option in FBX); smoothing groups do not always survive FBX, so verify in the target engine; `Reset XForm` before export.

---

## Houdini

| Universal | Houdini |
| --------- | -------- |
| Create primitive | `Box`, `Tube`, `Sphere`, `Icosphere` (Poly) SOPs |
| Extrude | `Poly Extrude` SOP |
| Inset | `Poly Extrude` with `Inset` |
| Bevel | `Poly Bevel` SOP |
| Loop cut | `Group` by range + `Poly Split` / `Divide` |
| Bridge | `Poly Bridge` SOP |
| Mirror | `Mirror` SOP (with `Consolidate`) |
| Array | `Copy to Points` SOP (the canonical Houdini array) |
| Instance | `Copy to Points` with packed primitives |
| Boolean | `Boolean` SOP (`Detect and Fix Intersections` on) |
| Flat shading | `Facet` SOP → `Unique Points`, or `Normal` SOP with `Cusp` angle high |
| Hard/soft edges | `Facet` / `Normal` SOP cusp angle |
| Merge/weld | `Fuse` SOP (set a distance) |
| Normals | `Normal` SOP / `Reverse` SOP |

**Gotchas:** Houdini's strength is procedural — build the model as a parameter-driven SOP network, expose the randomization parameters from `references/07`, and use attribute-driven variation (`@ptnum`, random per copy). Packed primitives keep instances cheap. Y-up matches engines.

---

## Cinema 4D

| Universal | Cinema 4D |
| --------- | --------- |
| Create primitive | `Create > Mesh` / primitive objects; lower segments in the object properties |
| Extrude | `Mesh > Extrude` (or Extrude as a generator) |
| Inset | `Mesh > Extrude Inner` |
| Bevel | `Mesh > Bevel` (Bevel deformer or generator) |
| Loop cut | `Loop/Path Cut` tool |
| Bridge | `Mesh > Bridge` |
| Mirror | `Symmetry` object (keep it live; bake when exporting) |
| Array | `Cloner` (grid/radial) + `MoGraph` effectors for variation |
| Instance | `Instance` object or Cloner in `Instance` mode |
| Boolean | `Boole` object; then `Mesh > Optimize` |
| Flat shading | `Phong` tag off, or set the Phong angle low; use flat/hard normals |
| Hard/soft edges | `Mesh > Normals > ...`, Phong tag angle |
| Merge/weld | `Mesh > Optimize` (with points) |
| Normals | `Mesh > Normals > Reverse Normals` |

**Gotchas:** C4D is Y-up; many settings live in generators that must be made editable (`C` key) before export; Phong tag shading can make a low-poly model look smooth when the plan says flat — set the Phong angle or remove the tag.

---

## Unity

- **Import:** `.fbx` or `.glb` preferred. Set `Model` tab → `Scale Factor` (usually 1.0 if the model was authored in meters).
- **Units / axes:** Unity is Y-up, left-handed, meters. Blender/Maya FBX usually needs no axis flip if exported with `+Y up`.
- **Materials:** import with `Extract Materials`, or create Unity materials manually. Low-poly stylized work usually uses URP/Lit with smooth roughness, or a toon/shader-graph shader.
- **Flat shading:** Unity recomputes normals on import; to keep faceted shading, either split edges in the DCC (preferred) or set `Normals > Import` (not Calculate) in the model import settings — calculating with a high smoothing angle flattens facets.
- **Instancing:** use Prefabs for repeated props; enable GPU Instancing on materials; use Prefab Variants for color variation via `MaterialPropertyBlock`.
- **LODs:** `LOD Group` component with the LOD meshes; set screen-relative transition heights.
- **Collision:** `BoxCollider` / `MeshCollider` (convex); keep colliders as separate primitives.
- **Pivots:** Unity uses the object's transform origin; author the FBX with the pivot where the plan says, or wrap in a parent GameObject.

---

## Unreal Engine

- **Import:** FBX preferred. Unreal is Z-up, left-handed, centimeters.
- **Units:** 1 Unreal unit = 1 cm. A model authored in meters imports at 1/100 scale unless `Import Uniform Scale` is set to 100 or the model is authored at real scale.
- **Materials:** create Material Instances from a master material; use Material Instance parameters for per-asset color variation (great for instanced low-poly props).
- **Flat shading:** Unreal recomputes normals at import by default — in the FBX import options set `Normal Import Method = Import Normals` and enable `Recompute Normals = false`, or build with fully split/hard-edged geometry in the DCC.
- **Instancing:** `Instanced Static Mesh` (ISM) / `Hierarchical ISM` for foliage and repeated props; `Foliage` tool for scatter.
- **LODs:** auto-generate or import an LOD chain; set screen-size thresholds per LOD; Nanite generally does not help low-poly stylized assets (and can defeat the faceted look).
- **Collision:** generate a convex or box collision in the Static Mesh editor; keep it to a handful of hulls.

---

## Godot

- **Import:** `.glb`/`.gltf` is the first-class path (better than FBX). Godot is Y-up, right-handed, meters.
- **Materials:** `StandardMaterial3D` or `ORMMaterial3D`. Set `Shading Mode`, disable rim/specular gimmicks for a clean flat look; vertex colors are supported natively.
- **Flat shading:** glTF with split normals is respected; in Godot you can also force flat via the surface's material or by ensuring the mesh has no smoothing groups.
- **Instancing:** `MultiMeshInstance3D` for large repeated sets (foliage, rocks), `GridMap` for modular kits.
- **LODs:** `GeometryInstance3D` LOD bias or manual `VisibleInstance3D`/`LOD` setup; `Mesh` LOD generation exists in the importer.
- **Collision:** `StaticBody3D` + `CollisionShape3D`; generate a trimesh convex or a primitive shape.

---

## Three.js

- **Format:** glTF/GLB (`GLTFLoader`) is the recommended path. `OBJLoader` and `FBXLoader` exist but are lossier.
- **Units:** arbitrary, but pick meters and be consistent. Y-up (matches glTF).
- **Building procedurally:** use `BufferGeometry` and build vertex/index arrays directly; this is the cleanest way to generate low-poly assets at runtime.

```js
// Minimal flat-shaded low-poly box, from a plan's dimensions
const geo = new THREE.BoxGeometry(w, h, d);          // w/h/d in base units
const mesh = new THREE.Mesh(
  geo,
  new THREE.MeshStandardMaterial({ color: 0x6b4a2f, roughness: 0.6, metalness: 0.0, flatShading: true })
);
mesh.position.set(x, y, z);
mesh.rotation.set(rx, ry, rz);   // radians
```

- **Flat shading:** `material.flatShading = true`, or `geometry.computeVertexNormals()` after `toNonIndexed()` for per-face normals.
- **Instancing:** `InstancedMesh` for repeated elements; `BatchedMesh` for varied-geometry sets; set per-instance color with `instanceColor`.
- **Performance:** merge static geometry (`BufferGeometryUtils.mergeGeometries`), share materials, keep draw calls low; use `geometry.computeBoundingSphere()` after edits.
- **LODs:** `THREE.LOD` with distance thresholds.

---

## OpenSCAD

Purely procedural/parametric — a plan maps almost directly to code. Express the plan's dimensions as variables at the top so the model stays parameterized.

```scad
// Base units from the plan
total_h = 10;
head_h  = 2.2;
body_h  = 4.0;

module handle(len = 8, r = 0.5, sides = 6) {
  // tapered shaft: cylinder + scale on the top ring
  cylinder(h = len, r1 = r, r2 = r * 0.75, $fn = sides);
}

module body() {
  cube([2.4, body_h, 1.6], center = true);
}

translate([0, 0, 0]) handle();
translate([0, body_h / 2, 0]) body();
```

Notes: `cylinder()` with `r1`/`r2` gives tapers for free; `hull()` unions two primitives into a smooth connecting mass (excellent for organic low-poly blobs); `minkowski()` rounds shapes but explodes geometry — use sparingly; `$fn` sets facet count (6–12 for low poly); prefer `mirror([1,0,0])` over duplicating symmetric parts. Export `.stl` (3D print) or `.off`/`.3mf`; note that STL has no units, materials, or color — set the target unit in the slicer.

---

## Unknown / custom / other tools

If the user names a tool not listed here (or a proprietary in-house tool), generate the mapping yourself using the same pattern:

1. Table mapping each universal operation to that tool's equivalent.
2. Its axis convention and unit scale vs the plan's coordinate system.
3. Its normal/smoothing model (this is where flat shading usually breaks).
4. Its instancing/array mechanism.
5. Its export path and what gets lost.
6. Any gotcha that would silently ruin a low-poly asset there.
