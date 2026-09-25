# LOW-POLY MODEL PLAN

> Blank template. Copy, fill, delete the italic guidance in parentheses.
> Keep the section numbering and headings verbatim so `scripts/validate_plan.py` can check it.

## 1. Model Overview

**Object:** <!-- name -->
**Intended use:** <!-- game prop / hero asset / icon / animation / print / environment -->
**Visual style:** <!-- stylized / realistic / chunky-toy / geometric -->
**Input type:** <!-- text only | one image | multiple images | text + images -->

<!-- If images were supplied, paste the Reference Read block here -->
**Reference Read**
- Images supplied:
- View angle:
- Confirmed (Observed):
- Reasoned (Inferred):
- Not visible (Recommended):
- Recognizability drivers:
- Detail deferred to material:

<!-- If the request was vague, or an assumption could change the model -->
**Assumptions**
1.
2.

## 2. Target Style

- **Polygon density:** <!-- category + range + reason -->
- **Silhouette:** <!-- philosophy + planned exaggerations -->
- **Shading:** <!-- flat / mostly-flat-with-selective-smoothing / smooth-with-hard-accents -->
- **Proportions:** <!-- realistic / stylized / chunky -->
- **Level of detail:** <!-- silhouette only / + functional parts / + surface detail -->
- **Estimated triangle budget:** <!-- e.g. 250–600 tris -->

## 3. Coordinate System

- **Up axis:**
- **Forward direction:**
- **Origin:**
- **Base unit:**
- **Overall dimensions:** <!-- W × H × D -->

## 4. Component Breakdown

| Part | Base Shape | Dimensions | Position | Rotation | Polygon Level |
| ---- | ---------- | ---------- | -------- | -------- | ------------- |
|      |            |            |          |          |               |

<!-- Position = coordinates of the part's pivot relative to the origin, in base units. -->
<!-- Polygon Level = Very Low / Low / Medium, plus a rough triangle estimate. -->

## 5. Step-by-Step Construction

### 5.1 <Part name> (<base primitive>, ~<n> tris)

1. Create a <primitive> with <parameters>.
2. Scale to <X> × <Y> × <Z> units.
3. Move to (<x>, <y>, <z>) — <what that location is>.
4. Rotate to (<rx>, <ry>, <rz>)° — <why>.
5. Select <which faces or edges>.
6. <Operation> by <amount>.
7. <Cleanup operation>.
8. Assign material <name>. Shading: <flat | smooth | weighted normals | hard/soft edges>.

### 5.2 <Next part>
<!-- repeat -->

## 6. Assembly

<!-- How parts meet: touching faces, welds, interpenetration, parenting, pivot placement, z-fighting avoidance. -->

## 7. Materials

| Material | Color | Roughness | Metallic | Shading |
| -------- | ----- | --------- | -------- | ------- |
|          |       |           |          |         |

**Palette**

| Slot | Hex | Used on |
| ---- | --- | ------- |
| Dominant | `#000000` | |
| Secondary | `#000000` | |
| Accent | `#000000` | |
| Neutral | `#000000` | |

**Detail deferred to material:** <!-- panel lines, bolts, decals, text -->

## 8. Low-Poly Optimization

- **Delete:** <!-- interior/hidden faces -->
- **Dissolve:** <!-- redundant loops, coplanar faces -->
- **Weld:** <!-- duplicate verts, mirror seams -->
- **Mirror:** <!-- which axis, which parts -->
- **Instance:** <!-- repeated elements -->
- **Reuse:** <!-- components shared with other assets -->
- **Triangle estimate:** before ___ → after ___

## 9. Final Validation

| # | Check | Pass condition | Status |
| - | ----- | -------------- | ------ |
| 1 | Silhouette recognizable | Identifiable as a solid-black silhouette | ☐ |
| 2 | Proportions correct | Parts sum to stated totals (±3%) | ☐ |
| 3 | No unnecessary geometry | Every face works | ☐ |
| 4 | Normals correct | No inverted normals | ☐ |
| 5 | Materials assigned | No default/gray faces | ☐ |
| 6 | No duplicate geometry | Weld test passes | ☐ |
| 7 | Polygon budget respected | Inside the recommended range | ☐ |
| 8 | Ready for export | Scale, up axis, applied transforms, pivot correct | ☐ |

## 10. Optional Software Implementation

<!-- Only if the user named software. Otherwise:
"No target software specified — universal plan only." -->

**Target:** <!-- Blender / Maya / 3ds Max / Houdini / Cinema 4D / Unity / Unreal / Godot / Three.js / OpenSCAD -->

- **Operation mapping:**
- **Axis / unit handling:**
- **Normal & shading settings:**
- **Instancing / array mechanism:**
- **Export settings:**
- **Gotchas:**
- **Script / node setup / code:**
