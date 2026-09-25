# Game-Ready & Export Considerations

Include this block whenever the asset is for a game, a real-time engine, or anything that gets exported.

## 1. The game-ready checklist

| Item | Recommendation |
| ---- | -------------- |
| **Triangle count** | Within the Section 2 budget; state the final number |
| **Pivot / origin** | Where the plan says: ground contact center for props, grip point for handhelds, wheel-contact center for vehicles |
| **Scale** | Authored at real-world size in the engine's unit system (Unity/Godot: meters; Unreal: centimeters) |
| **Applied transforms** | All transforms applied/reset before export (scale = 1, rotation = 0) |
| **Naming** | `<CATEGORY>_<Object>_<Part>_<Side><Index>`, e.g. `PRP_Barrel_Body`, `VEH_Truck_Wheel_F_L` |
| **Material count** | 1–3 for props, 2–5 for hero assets; each material = potential extra draw call |
| **UV requirements** | Valid UV0 even for flat-color assets; optional UV1 only if lightmaps are needed |
| **Collision** | Convex primitives or a small hull decomposition; never the render mesh |
| **LODs** | LOD0/1/2 at ~100% / 50% / 25%; keep silhouettes consistent |
| **Texture resolution** | Per `references/11`; shared atlases where possible |
| **Export format** | `.glb`/`.gltf` (web, Godot, modern pipelines), `.fbx` (Unity, Unreal), `.obj` (universal fallback, no materials), `.stl`/`.3mf` (3D print) |

---

## 2. Format selection

| Format | Use for | Loses |
| ------ | ------- | ----- |
| **glTF / GLB** | Web, Three.js, Godot, modern pipelines, asset delivery | Very little; supports PBR, vertex colors, embedded textures |
| **FBX** | Unity, Unreal, most DCC interchange | Version mismatch issues; smoothing/normal interpretation varies |
| **OBJ** | Universal fallback, 3D print workflows, simple meshes | No materials beyond a basic MTL, no animations, no units |
| **USD / USDZ** | Large pipelines, AR (Apple) | Tooling varies |
| **STL / 3MF** | 3D printing | No color, no materials (3MF has some), no units in STL |
| **Blend / C4D / Max native** | Handing off within that DCC | Not usable elsewhere |

Always state the export format **and** the settings that matter: up axis, unit scale, whether to triangulate, whether to apply modifiers, and whether to embed textures.

---

## 3. Axis and unit conversion

| Target | Up axis | Units | Handedness |
| ------ | ------- | ----- | ---------- |
| Unity | Y | meters | Left |
| Unreal | Z | centimeters | Left |
| Godot | Y | meters | Right |
| Three.js / glTF | Y | arbitrary (meters conventional) | Right |
| Blender | Z (exports +Y) | meters | Right |
| Maya | Y | centimeters | Right |
| 3ds Max | Z | arbitrary | Right |
| Houdini | Y | meters | Right |
| Cinema 4D | Y | centimeters | Right |
| OpenSCAD / STL | Z | unitless | Right |

**Always state the conversion in the plan.** "Export FBX with +Y up, 1 unit = 1 m, triangulated, modifiers applied, textures embedded."

---

## 4. Draw-call and batching notes

- One material per mesh is cheapest; each additional material can add a draw call.
- Merge static, same-material meshes that are always visible together — but do **not** merge across a large area or you lose frustum culling.
- Use instancing (Unity Prefabs/GPU instancing, Unreal ISM/HISM, Godot MultiMesh, Three.js InstancedMesh) for anything repeated more than ~4 times.
- Share atlases and trim sheets across whole kits to allow material batching.
- Vertex colors let many assets share one material while still looking different — very effective for low-poly props.

---

## 5. Pre-export cleanup (final pass)

1. Apply / freeze all transforms.
2. Delete history and construction modifiers/generators (or apply them deliberately).
3. Triangulate, then spot-check the triangulation direction on quads that form visible creases.
4. Weld vertices; remove zero-area faces, lamina faces, and interior faces.
5. Recalculate/flip normals so all face outward; verify visually from all sides.
6. Clear unused materials, UV sets, vertex colors, and empty objects from the scene.
7. Rename everything to the naming convention; remove default names (`Cube.001`, `pCube1`).
8. Confirm the pivot is at the stated origin.
9. Confirm the object measures the intended real-world size.
10. Export with the stated settings, then **re-import the exported file** and verify: scale, orientation, normals, materials, triangle count.
