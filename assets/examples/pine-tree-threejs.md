# LOW-POLY MODEL PLAN — Example: Stylized Pine Tree (procedural, Three.js)

> Worked example. User request: *"I need low-poly pine trees for a Three.js scene — hundreds of them, procedurally generated."*
> Demonstrates: procedural generation, radial symmetry, instancing, vertex colors, a code implementation in Section 10.

## 1. Model Overview

**Object:** Stylized conifer (pine/spruce), 3 size classes
**Intended use:** Scattered background foliage in a real-time web scene — hundreds to thousands of instances
**Visual style:** Geometric low poly — stacked cones and a cylinder trunk, flat shaded, vertex-colored
**Input type:** Text only

**Assumptions**
1. **Temperate conifer** (stacked conical tiers), not a broadleaf or a palm.
2. Viewed from **5–60 m** — never inspected closely, so no needles are modeled individually.
3. **No wind animation** at LOD0 (mention only if a vertex shader is added later).
4. Web delivery, so **no textures** — vertex colors only.
5. The scene already has a ground plane; the tree does not include one.

## 2. Target Style

- **Polygon density:** background/instanced asset — **60–160 triangles each.** At hundreds of instances, per-tree cost is the whole budget.
- **Silhouette:** a tall triangle with stepped tiers. The stepped edge, not the surface detail, is what makes it a conifer rather than a cone.
- **Shading:** fully **flat**. Facets on the cone tiers catch light and separate the layers.
- **Proportions:** stylized — trunk short, tiers wide and chunky, slight irregularity so no two trees match.
- **Level of detail:** silhouette only. Zero surface detail.
- **Estimated triangle budget:** **~110 triangles** for a 3-tier tree at the default settings.

## 3. Coordinate System

- **Up axis:** Y (matches Three.js / glTF)
- **Forward direction:** not applicable (radially symmetric, but each instance gets a random Y rotation)
- **Origin:** center of the trunk base at ground level (Y = 0) — so instances drop straight onto terrain
- **Base unit:** total tree height = **10.0 units** (≈ 12 m real → export/`scale` as needed)
- **Overall dimensions:** **4.4 W (X) × 10.0 H (Y) × 4.4 D (Z)** at the default tier spread

## 4. Component Breakdown

| Part | Base Shape | Dimensions | Position | Rotation | Polygon Level |
| ---- | ---------- | ---------- | -------- | -------- | ------------- |
| Trunk | Cylinder, 6 sides, capped | d 0.55, H 2.60 | (0, 1.30, 0) | 0, 0°, 0 | Very low — 20 tris |
| Tier 1 (bottom) | Cone, 8 sides | d 4.40, H 3.60 | (0, 3.40, 0) | 0, 12°, 0 | Very low — 16 tris |
| Tier 2 (middle) | Cone, 8 sides | d 3.30, H 3.20 | (0, 5.60, 0) | 0, 26°, 0 | Very low — 16 tris |
| Tier 3 (top) | Cone, 8 sides | d 2.10, H 2.60 | (0, 7.60, 0) | 0, 41°, 0 | Very low — 16 tris |
| Tip spike | Cone, 4 sides | d 0.70, H 1.60 | (0, 9.20, 0) | 0, 0°, 0 | Very low — 8 tris |
| Root flare (optional) | Cone, 6 sides, inverted | d 1.10, H 0.45 | (0, 0.22, 0) | 0, 0°, 0 | Very low — 12 tris |

*Total ≈ 88 tris without the root flare, ~100 with it. A 4-tier variant is ~124.*

## 5. Step-by-Step Construction

### 5.1 Trunk (6-sided cylinder, ~20 tris)

1. Create a cylinder, **6 sides**, diameter 0.55, height 2.60, capped.
2. Move to **(0, 1.30, 0)** — spanning Y = 0.00 to 2.60.
3. Scale the **bottom** ring to 1.25× (diameter 0.69) so the trunk flares into the ground; this is what keeps the tree from looking like a pole stuck in the floor.
4. Delete the **top cap** — it is buried under tier 1. Keep the bottom cap if the tree can be seen from below; otherwise delete it too.
5. Add **no loop cuts**.
6. Assign `MAT_Bark`. Shading: **flat**.

### 5.2 Tiers (3 × 8-sided cone, ~16 tris each)

1. Create an **8-sided cone**, cap the base.
2. **Tier 1:** diameter 4.40, height 3.60; move to (0, 3.40, 0) so its base sits at Y = 1.60 — overlapping the trunk top by 1.0 so there is no visible gap.
3. **Tier 2:** diameter 3.30, height 3.20; move to (0, 5.60, 0) — base at Y = 4.00, overlapping tier 1's upper section by 0.60.
4. **Tier 3:** diameter 2.10, height 2.60; move to (0, 7.60, 0) — base at Y = 6.30.
5. Delete the **base cap** of every tier except tier 1 — they are hidden inside the tier below.
6. Rotate each tier about Y by a **different amount** (12°, 26°, 41°) so the facets do not line up vertically. Aligned facets create a single continuous shading seam that reads as a hard manufactured edge.
7. Scale each tier non-uniformly by 0.96–1.04 on X and Z, and jitter a few base vertices by ±3% of the radius, so no two trees are identical.
8. Assign `MAT_Foliage_Dark` to tier 1, `MAT_Foliage` to tiers 2 and 3 (darker at the bottom reads as self-shadowing and costs nothing).
9. Shading: **flat** on every tier.

### 5.3 Tip spike (4-sided cone, ~8 tris)

1. Create a **4-sided cone**, diameter 0.70, height 1.60.
2. Move to (0, 9.20, 0) — base at Y = 8.40, buried in tier 3's apex region; apex at Y = 10.00, the top of the tree.
3. Delete the base cap.
4. Assign `MAT_Foliage_Light`. Shading: **flat**.

### 5.4 Root flare (optional, 6-sided cone, ~12 tris)

1. Create a 6-sided cone, diameter 1.10, height 0.45.
2. **Flip it** (rotate 180° about X or Z) so the apex points down into the ground.
3. Move to (0, 0.22, 0).
4. Assign `MAT_Bark`. Shading: **flat**. Skip this part entirely if the trees are scattered on uneven terrain (the flare will float).

## 6. Assembly

- **Order:** root flare → trunk → tier 1 → tier 2 → tier 3 → tip.
- **Overlaps, not joints:** tiers deliberately overlap the tier below by 0.6–1.0 units. Never butt cone bases together — a hairline gap at the tier boundary is the classic broken-pine look.
- **Merge** all parts into a single geometry at generation time (they never move independently and share 3 materials). One geometry per tree variant, then instance it.
- **Pivots:** the single merged geometry's origin is at (0, 0, 0), the trunk base — instances placed at terrain height need no offset.
- **Instance variation** comes from per-instance transform (uniform scale 0.7–1.4, Y rotation 0–360°, slight non-uniform XZ scale 0.92–1.08) and per-instance color (darken/lighten the foliage by ±8% in value, ±5% in hue).

## 7. Materials

| Material | Color | Roughness | Metallic | Shading |
| -------- | ----- | --------- | -------- | ------- |
| `MAT_Bark` | `#5A3B26` | 0.85 | 0.0 | Flat |
| `MAT_Foliage_Dark` | `#2C4A34` | 0.90 | 0.0 | Flat |
| `MAT_Foliage` | `#3A6142` | 0.90 | 0.0 | Flat |
| `MAT_Foliage_Light` | `#4C7A52` | 0.90 | 0.0 | Flat |

**Palette**

| Slot | Hex | Used on |
| ---- | --- | ------- |
| Dominant | `#3A6142` | Middle foliage |
| Secondary | `#2C4A34` | Lower foliage (reads as shadow) |
| Neutral | `#5A3B26` | Trunk |
| Accent | `#4C7A52` | Tip highlight |

**Detail deferred to material:** needles, branch structure, bark texture, snow, moss. **No textures at all** — everything is flat-shaded vertex color. A single 256×256 foliage atlas is only worth adding if the camera ever closes to under 5 m.

## 8. Low-Poly Optimization

- **Delete:** top cap of the trunk; base caps of tiers 2, 3, and the tip; the bottom cap of the trunk if the tree is never seen from below.
- **Dissolve / weld:** after merging, weld the tier overlaps are **not** welded (they are separate overlapping solids — keep them, they are invisible and merging would cost more than it saves). Weld only within each part.
- **Mirror:** not applicable — the tree is radially symmetric by construction (cones and cylinders), so no mirroring is needed.
- **Instance:** this is the entire point of the asset. Generate **3–5 geometry variants**, then place hundreds of `InstancedMesh` copies with per-instance transforms and colors. Unique geometry: ~5 × 100 = 500 triangles for an entire forest.
- **Reuse:** the trunk (6-sided cylinder) and the tier (8-sided cone) are the same two primitives used at different scales — one parameterized function each.
- **Do not reduce:** tiers to fewer than **6 sides** (they stop reading as cones and start reading as pyramids — acceptable for a crystal, wrong for a tree); the tier count below 3 (the silhouette flattens).
- **LODs:**
  | LOD | Tris | Changes |
  | --- | ---- | ------- |
  | LOD0 | ~100 | 3 tiers as planned |
  | LOD1 | ~52 | 2 tiers, cones at 6 sides, no trunk flare |
  | LOD2 | ~20 | A single 6-sided cone + a trunk box |
  | LOD3 | — | Culled, or replaced by a billboard impostor |
- **Triangle estimate:** 124 before cleanup → **~100 after** → ~500 unique triangles for the whole forest.

## 9. Final Validation

| # | Check | Pass condition | Status |
| - | ----- | -------------- | ------ |
| 1 | Silhouette recognizable | Stepped triangular outline = conifer, not a cone or a bush | ☐ |
| 2 | Proportions correct | Tip apex at Y = 10.00 (±3%); tiers overlap by ≥ 0.6 | ☐ |
| 3 | No unnecessary geometry | 4 buried caps deleted; no needles modeled | ☐ |
| 4 | Normals correct | No inverted cones; flat shading active on all parts | ☐ |
| 5 | Materials assigned | Exactly 4 materials; no default gray | ☐ |
| 6 | No duplicate geometry | Instances share geometry; variants are 3–5, not 300 | ☐ |
| 7 | Polygon budget respected | ~100 tris per tree, ~500 unique total | ☐ |
| 8 | Ready for export | Y-up, origin at trunk base, scale 1, glTF or generated in-engine | ☐ |

**Extended:** per-instance color varies ☐ · LOD chain present ☐ · no textures shipped ☐ · collision = a single 1.2-diameter cylinder per tree ☐ · instanced draw calls ≤ 5 for the whole forest ☐

## 10. Optional Software Implementation — Three.js

Procedural generation: build `BufferGeometry` per variant, merge, then instance. Every dimension in Section 4 is a parameter.

```js
import * as THREE from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

// ---- Plan parameters (Section 4) -------------------------------------------
const DEFAULTS = {
  height: 10.0,          // base unit: total tree height
  tierCount: 3,          // 3 -> LOD0, 2 -> LOD1, 1 -> LOD2
  tierSides: 8,          // never below 6
  trunkSides: 6,
  trunkDiam: 0.55,
  trunkHeight: 2.60,
  baseDiameter: 4.40,    // tier 1
  tierTaper: 0.75,       // each tier is 75% the diameter of the one below
  tierOverlap: 0.60,     // units of vertical overlap between tiers
  tipHeight: 1.60,
  flatten: 1.0,          // XZ scale on tiers
  seed: 1,
};

const COLOR = {
  bark:      0x5a3b26,
  darkLeaf:  0x2c4a34,
  leaf:      0x3a6142,
  lightLeaf: 0x4c7a52,
};

// Deterministic RNG so a seed reproduces a tree exactly
function rng(seed) {
  let s = seed >>> 0 || 1;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
}

function flatMaterial(color) {
  return new THREE.MeshStandardMaterial({
    color, roughness: 0.9, metalness: 0.0, flatShading: true,
  });
}

/** Build one tree geometry. Returns geometry with 3 material groups. */
export function makePineGeometry(userOpts = {}) {
  const o = { ...DEFAULTS, ...userOpts };
  const rand = rng(o.seed);
  const jitter = (a) => 1 + (rand() * 2 - 1) * a;

  const parts = [];   // { geometry, matIndex }
  const mats  = [flatMaterial(COLOR.bark), flatMaterial(COLOR.darkLeaf), flatMaterial(COLOR.leaf)];

  // 5.1 Trunk ---------------------------------------------------------------
  const trunk = new THREE.CylinderGeometry(
    o.trunkDiam * 0.5 * 1.25,   // bottom radius (flare)
    o.trunkDiam * 0.5,          // top radius
    o.trunkHeight,
    o.trunkSides,
    1,
    true                        // open ended: delete both caps
  );
  trunk.translate(0, o.trunkHeight * 0.5, 0);
  parts.push({ geo: trunk, mat: 0 });

  // 5.2 Tiers ---------------------------------------------------------------
  const tierH = (o.height - o.tipHeight - o.trunkHeight * 0.5) / o.tierCount;
  let diam = o.baseDiameter;
  let y = o.trunkHeight + tierH * 0.5 - o.tierOverlap * 0.5;

  for (let i = 0; i < o.tierCount; i++) {
    const h = tierH + o.tierOverlap;
    const cone = new THREE.ConeGeometry(diam * 0.5 * jitter(0.04), h, o.tierSides, 1, i > 0);
    cone.scale(1, 1, o.flatten);
    cone.rotateY((i * 0.24 + rand() * 0.3) * Math.PI);   // de-align the facets
    cone.translate(0, y, 0);
    parts.push({ geo: cone, mat: i === 0 ? 1 : 2 });      // bottom tier darker
    diam *= o.tierTaper;
    y += tierH;
  }

  // 5.3 Tip spike -----------------------------------------------------------
  const tip = new THREE.ConeGeometry(0.35, o.tipHeight, 4, 1, true);
  tip.translate(0, o.height - o.tipHeight * 0.5, 0);
  parts.push({ geo: tip, mat: 2 });

  // Merge with material groups (groups keep the 3 materials on one geometry)
  const geos = parts.map((p) => {
    const g = p.geo.toNonIndexed();
    g.clearGroups();
    g.addGroup(0, g.attributes.position.count, p.mat);
    return g;
  });
  const merged = mergeGeometries(geos, true);
  merged.computeVertexNormals();     // flatShading handles the faceting
  merged.computeBoundingSphere();
  return merged;
}

/** Scatter N trees as instances. */
export function makeForest(count = 300, opts = {}) {
  const variants = [1, 2, 3, 4, 5].map((seed) => makePineGeometry({ ...opts, seed }));
  const materials = [
    flatMaterial(COLOR.bark), flatMaterial(COLOR.darkLeaf), flatMaterial(COLOR.leaf),
  ];
  const meshes = variants.map((geo) =>
    new THREE.InstancedMesh(geo, materials, Math.ceil(count / variants.length))
  );

  const m = new THREE.Matrix4();
  const q = new THREE.Quaternion();
  const p = new THREE.Vector3();
  const s = new THREE.Vector3();
  const c = new THREE.Color();

  meshes.forEach((mesh, vi) => {
    let i = 0;
    for (let n = vi; n < count; n += variants.length) {
      const scale = 0.7 + Math.random() * 0.7;               // 0.7 - 1.4
      p.set((Math.random() - 0.5) * 200, 0, (Math.random() - 0.5) * 200);
      q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), Math.random() * Math.PI * 2);
      s.set(scale * (0.92 + Math.random() * 0.16), scale, scale * (0.92 + Math.random() * 0.16));
      mesh.setMatrixAt(i, m.compose(p, q, s));
      // per-instance foliage tint variation (+/- 8% value)
      c.set(COLOR.leaf).offsetHSL((Math.random() - 0.5) * 0.05, 0, (Math.random() - 0.5) * 0.16);
      mesh.setColorAt(i, c);
      i++;
    }
    mesh.count = i;
    mesh.instanceMatrix.needsUpdate = true;
    if (mesh.instanceColor) mesh.instanceColor.needsUpdate = true;
    mesh.castShadow = true;
    mesh.receiveShadow = true;
  });
  return meshes;
}
```

**Axis / unit handling:** Three.js is Y-up with arbitrary units — the plan's coordinates are used as-is. Set `scale = 0.012` on the parent group if the scene is authored in meters and the tree should be 12 m tall.

**Flat shading:** `flatShading: true` on every material plus `toNonIndexed()` before merging, so each face gets its own normal. Do **not** call `computeVertexNormals()` on an indexed geometry expecting facets — index-sharing averages the normals and the tree goes smooth.

**Instancing:** `InstancedMesh` per variant (5 draw calls for the whole forest). Per-instance color via `setColorAt` requires the material to have `vertexColors` handled by the instance color attribute — Three.js does this automatically when `instanceColor` exists.

**Performance:** 5 unique geometries × ~100 tris = 500 triangles of unique memory for 300+ trees. Keep shadows on one directional light only, and disable shadow casting past LOD1.

**LODs:** build LOD1 (`tierCount: 2, tierSides: 6`) and LOD2 (`tierCount: 1, tierSides: 6, trunkHeight: 1.4`) from the same function and swap with `THREE.LOD` at distances 60 m and 140 m. Because the generator is parameterized, the LOD chain costs three function calls.

**Export alternative:** if the trees should be a static asset rather than runtime-generated, generate once, export via `GLTFExporter`, and ship a single `.glb` containing 5 variants — then instance that.
