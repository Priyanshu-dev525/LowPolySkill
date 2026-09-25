---
name: universal-lowpoly-3d-modeling
description: Turn a text description, a reference image, several reference images, or a mix of text and images into a complete, software-independent low-poly 3D model construction plan. Use whenever the user asks to make, design, block out, plan, rebuild, or optimize a low-poly 3D asset (prop, character, vehicle, building, creature, plant, weapon, environment kit) for Blender, Maya, 3ds Max, Houdini, Cinema 4D, Unity, Unreal Engine, Godot, Three.js, OpenSCAD, or any other 3D tool. Produces silhouette analysis, component breakdown, primitive recipes, dimensions, placement, rotations, polygon budgets, topology, materials, colors, shading, symmetry, instancing, optimization and export guidance.
license: MIT
version: 1.0.0
---

# Universal Low-Poly 3D Modeling Skill

## Purpose

This skill converts **"make this object"** into **"here is exactly how to construct this object, part by part"**.

The output is a *model construction plan*: a complete, software-independent recipe that another AI, a human artist, a procedural system, or a technical artist can execute inside any 3D application.

The skill is deliberately **application-agnostic**. It thinks in universal modeling operations — create primitive, scale, rotate, translate, extrude, inset, bevel, loop cut, bridge, mirror, array, boolean, dissolve, weld, flip normals — not in the menus of one package.

---

## When To Use

Use this skill when the request is any of:

- "Make a low-poly X." (text only)
- "Make this into a low-poly model." + image
- "Turn these reference images into a game asset."
- "Model this character / vehicle / building / prop in low poly."
- "How would I build this?" (about an object, not about UI)
- "Give me a construction plan / blockout / asset spec for X."
- "Optimize / reduce / stylize this model for low poly."
- "I need a low-poly X for Unity / Unreal / Godot / Three.js / a game."
- Procedural or scripted low-poly generation requests (OpenSCAD, Three.js, Houdini, Blender Python).

Do **not** use it for: high-poly sculpting workflows, photoreal PBR hero assets, photogrammetry retopology, CAD-tolerance mechanical parts, or pure 2D art. (Its optimization and decomposition rules still help, but the low-poly stylization target will not fit.)

---

## The Five Roles This Skill Plays

Every plan is written as if reviewed by five people at once:

| Role | What it demands from the plan |
| ---- | ----------------------------- |
| Low-poly artist | Recognizable silhouette, readable large forms, intentional style |
| Technical modeler | Clean topology, correct normals, sensible pivots, no wasted geometry |
| Procedural designer | Repeated units, arrays, mirroring, instancing, parameterization |
| Game asset artist | Triangle budget, material count, LODs, collision, export format |
| Art director | Proportions, color separation, material hierarchy, consistency |

If a plan would fail any one of these reviewers, it is not finished.

---

## Input Triage

Read the request, classify the input, then follow that path.

| Input | Protocol | Extra requirements |
| ----- | -------- | ------------------ |
| **Text only** | Treat the description as the source of truth. Extract every stated attribute (size, use, style, era, material, color, target software, purpose). Fill gaps with assumptions and label them. | Add an **Assumptions** block near the top. |
| **One reference image** | Run the Reference Image Analysis protocol first (`references/01-reference-image-analysis.md`). | Add a **Reference Read** section: camera/view angle, observed vs inferred vs recommended. |
| **Multiple reference images** | Analyze each image separately, then merge into one consensus object. Note contradictions between images and pick a resolution. | Add a **Reference Read** section including a per-image index and a contradiction resolution note. |
| **Text + image(s)** | Image wins on form and proportion; text wins on intent, use, and constraints. Where they conflict, say so and choose. | Add both **Reference Read** and **Assumptions**. |
| **Existing model to optimize** | Treat the existing mesh as the reference. Identify what to delete, dissolve, weld, collapse, and rebuild. | Add a **Before/After** comparison inside Optimization. |

**Vague request rule:** never stop and ask when you can reasonably assume. Make the assumption, label it, and keep going. Only flag an assumption as *blocking* when a different answer would change the whole model (e.g. "is this a toy or a real car?").

---

## Non-Negotiable Rules

1. **Never assume Blender.** The universal plan is tool-free. Software-specific notes appear only in Section 10, and only for software the user named.
2. **Never say "create the handle."** Say: *"Create a 6-sided cylinder, scale Z to 8.0 units, taper the top ring to 0.8×, extrude the top face 0.4 units, bevel the rim once."* Every component gets actionable operations.
3. **One base unit, stated out loud.** If no real-world scale is given, define one: *"Treat total character height as 10 units."* Then express every dimension relative to it, and keep them internally consistent (check that parts sum to the whole).
4. **Evidence is labeled.** Mark every claim **Observed** (visible in reference), **Inferred** (logical from what is visible), or **Recommended** (your design choice). Never present hidden geometry as if it were seen.
5. **Low poly is a style, not an unfinished model.** Every remaining polygon must earn its place: silhouette, intersection, animation, or material separation.
6. **Prefer primitives.** Start from cube / plane / cylinder / cone / sphere / icosphere / capsule / torus / pyramid / custom polygon / extruded polygon, then deform. Reach for boolean or sculpting only when a primitive path is genuinely worse.
7. **Silhouette beats detail.** At the target polygon count, the model must be identifiable from its outline alone. Delete or reallocate polygons that do not serve the outline, an intersection line, or a material boundary.
8. **Budget is a range, not a command.** Recommend a triangle range based on object size and purpose. Do not invent a hard number the user never gave.
9. **Use symmetry and repetition aggressively.** Model once, mirror/array/instance. Say which axis and how many copies.
10. **Colors separate components.** Palette entries exist to make parts readable at a glance, not to decorate. Always give hex.
11. **Shading is specified per component.** Flat, smooth, weighted normals, hard edges, soft edges — stated, not implied. Default to flat shading for classic low poly.
12. **Game-ready questions get game-ready answers.** If it is for a game or real-time engine, cover triangle count, pivot, scale, naming, material count, UVs, collision, LOD, texture resolution, and export format.

---

## Workflow

### Step 0 — Interpret the request
Extract: object identity, intended use (game prop, hero asset, icon, print, animation, environment), stylization level, target software (if any), polygon or performance constraints, and anything the user explicitly cares about.

### Step 1 — Analyze the reference (if any)
Work through `references/01-reference-image-analysis.md`. Output: view angle, silhouette, primary/secondary/tertiary forms, proportions, symmetry, materials, colors, surface character, must-keep features, and the decision of what becomes **geometry** vs what becomes **material/texture**.

### Step 2 — Set the style target
Fix polygon density, silhouette philosophy, shading model, proportion type (realistic vs stylized), and detail level. See `references/02-style-and-polygon-budgets.md`.

### Step 3 — Define the coordinate system
State up axis, forward axis, origin location, and overall bounding dimensions. This removes 90% of downstream ambiguity. (Recommend: Y-up, −Z or +Z forward, origin at the object's natural resting/contact point or rotation pivot.)

### Step 4 — Decompose the object
Break it into logical parts, ordered: **structure → shell → functional parts → surface details → accents**. See `references/03-model-decomposition.md`.

### Step 5 — Build the component table
One row per part with base shape, dimensions, position, rotation, polygon level. No row may say just "cube"; dimensions and placement are mandatory.

### Step 6 — Write construction steps
Numbered, sequential, executable instructions per component. Each step names the operation and its parameters. See `references/04-primitives-and-recipes.md` for reusable primitive transformation recipes.

### Step 7 — Assembly
Explain how parts meet: which faces touch, what is welded, what is merely interpenetrating, what is parented to what, and where the pivots sit.

### Step 8 — Materials, colors, shading
Material table + palette + per-component shading assignment. See `references/06-materials-color-shading.md`.

### Step 9 — Optimization
What to delete, dissolve, weld, mirror, instance, reuse, and what to leave alone. See `references/08-optimization-topology.md`.

### Step 10 — Validation checklist
Run the checklist in `references/09-validation.md`. Every box must be honestly checkable, with a pass condition.

### Step 11 — Optional software implementation
Only for software the user named. Use `references/10-software-implementation.md` (Blender, Maya, 3ds Max, Houdini, Cinema 4D, Unity, Unreal, Godot, Three.js, OpenSCAD).

---

## Output Contract

Every response uses exactly this structure. Keep the headings verbatim so plans are machine-checkable (`python scripts/validate_plan.py plan.md`).

````markdown
# LOW-POLY MODEL PLAN

## 1. Model Overview
What the object is, what it is for, and the intended visual style. Include an Assumptions block and/or a Reference Read block when applicable.

## 2. Target Style
Polygon density | silhouette philosophy | shading model | proportions | level of detail. Recommended triangle range with the reason.

## 3. Coordinate System
Up axis | forward direction | origin | overall dimensions | base unit definition.

## 4. Component Breakdown
| Part | Base Shape | Dimensions | Position | Rotation | Polygon Level |

## 5. Step-by-Step Construction
Numbered instructions per major component. Each: primitive → dimensions → position → rotation → face/edge selections → operations → shading.

## 6. Assembly
How parts connect, touch, weld, parent, and pivot. Intersection and z-fighting notes.

## 7. Materials
| Material | Color | Roughness | Metallic | Shading |
Plus: transparency/emission notes, and which details are texture-only.

## 8. Low-Poly Optimization
Delete / dissolve / weld / mirror / instance / reuse list. Triangle estimate before and after.

## 9. Final Validation
Checklist with pass conditions.

## 10. Optional Software Implementation
Only if the user named software. Otherwise: "No target software specified — universal plan only."
````

Section numbering is fixed. If a section has no content for this object, keep the heading and write a one-line reason (e.g. "No reference images supplied — Reference Read omitted.").

---

## Evidence Labeling (mandatory when a reference is used)

| Label | Meaning | Example |
| ----- | ------- | ------- |
| **Observed** | Directly visible in the reference | "Observed: three windows per side." |
| **Inferred** | Reasoned from what is visible | "Inferred: the far side mirrors the near side." |
| **Recommended** | Your design decision, not in evidence | "Recommended: underside is a flat plate; no reference shows it." |

Never write "the back has two vents" without a label when the reference only shows the front.

---

## Modeling Vocabulary (software-neutral)

Use these concepts only. Do not reference tool-specific menu paths in Sections 1–9.

**Create:** cube, plane, cylinder, cone, sphere, icosphere, capsule, torus, pyramid, custom polygon, extruded polygon
**Transform:** translate, rotate, scale (uniform and per-axis), align, snap, set pivot
**Edit:** extrude, inset, bevel, loop cut, merge, bridge, fill, knife/cut, delete faces, dissolve edges, collapse, weld vertices, flip normals, recalculate normals
**Duplicate:** duplicate, mirror, array, radial array, instance, clone, snap-to-surface scatter, curve/path array
**Combine:** boolean (union/subtract/intersect), attach, separate, join
**Refine:** subdivide (use sparingly), decimate (use sparingly), retopologize
**Shade:** flat, smooth, weighted normals, hard edge, soft edge, split edge, shade by angle
**UV:** unwrap, seam, pack, island, trim sheet, atlas, mirror UVs, box/triplanar projection

---

## Reference Files

Load only what the current request needs.

| File | Read it when |
| ---- | ----------- |
| `references/01-reference-image-analysis.md` | Any image, screenshot, or photo is supplied |
| `references/02-style-and-polygon-budgets.md` | Setting detail level or a triangle budget |
| `references/03-model-decomposition.md` | Breaking an unfamiliar object into parts |
| `references/04-primitives-and-recipes.md` | Writing construction steps / choosing base shapes |
| `references/05-dimensions-and-proportion.md` | Sizing parts, relative units, proportion systems |
| `references/06-materials-color-shading.md` | Palette, PBR values, flat vs smooth decisions |
| `references/07-procedural-and-symmetry.md` | Repeated elements, arrays, mirroring, instancing |
| `references/08-optimization-topology.md` | Cleaning geometry, topology rules, triangle counts |
| `references/09-validation.md` | Final checklist and pass conditions |
| `references/10-software-implementation.md` | User named Blender / Maya / Max / Houdini / C4D / Unity / Unreal / Godot / Three.js / OpenSCAD |
| `references/11-uv-textures.md` | Textures are requested, or vertex-color vs texture decision |
| `references/12-game-ready-and-export.md` | Real-time engine, game, or export target |
| `assets/templates/model-plan-template.md` | Blank starter template |
| `assets/examples/*.md` | Worked examples (hammer, pickup truck, pine tree, stylized character) |

---

## Common Failure Modes (avoid these)

- **Description instead of construction.** "A handle with a metal head" is not a plan. Give primitives, sizes, and operations.
- **Blender leakage.** No "Tab into edit mode", no "Add > Mesh > Cube", no "Shift+D" unless Section 10 says Blender.
- **Floating parts.** Every component has explicit coordinates relative to the stated origin.
- **Proportion drift.** Parts that should stack to 10.0 units stack to 11.7 because nobody checked.
- **Detail tourism.** Modeling bolts, panel lines, and fabric folds as geometry when a material or a normal-map-free color break would do.
- **Hidden geometry presented as fact.** Label it Inferred or Recommended.
- **Shading left implicit.** Flat vs smooth is a decision, not a default.
- **Over-modeling symmetry.** Modeling both halves by hand when one half plus a mirror is the point.
- **No budget arithmetic.** If you list per-part polygon levels, they should add up near the stated target.

---


## Machine-Readable Model Blueprint

The Markdown plan is the human-readable contract. When a downstream tool, agent, or exporter needs structured geometry, also produce a **Model Blueprint** conforming to `schemas/model-blueprint.schema.json`.

Use three output modes:

- **human** — the standard 10-section Markdown plan.
- **blueprint** — strict JSON only, suitable for procedural generators and exporters.
- **both** — Markdown plan followed by the JSON blueprint.

The blueprint is software-independent. It describes coordinate systems, parts, primitives, transforms, topology, materials, polygon estimates, symmetry, repetition, and procedural variation without assuming a DCC or engine.

### Blueprint rules

1. Every part has a stable `id` and explicit dimensions/transform where applicable.
2. Measurements use the plan's declared unit and coordinate system.
3. Material definitions are referenced by ID rather than duplicated per part.
4. Unknown values are represented with an explicit status such as `observed`, `inferred`, or `recommended`; never silently invented.
5. Repeated parts should use symmetry/instances rather than duplicating equivalent definitions.
6. Procedural variation may specify a deterministic seed and bounded ranges.
7. Polygon estimates are estimates unless an actual mesh is available.

## Geometry Validation

Before delivering a plan or blueprint, perform these checks when enough numeric information exists:

- stacked dimensions agree with the stated overall bounding box;
- mirrored parts use equal dimensions and opposite coordinates on the mirror axis;
- mating parts touch or intentionally overlap;
- dimensions and material values are within valid ranges;
- estimated triangles are reasonably consistent with the stated budget;
- every referenced material and part ID exists;
- the coordinate convention is stated exactly once and used consistently.

Use `python scripts/validate_blueprint.py <file.json>` for structured blueprints and `python scripts/validate_plan.py <file.md>` for Markdown plans.

## Dimension Library

Use the dimension references as **starting ranges**, not universal truths. Prefer object-specific, reference-derived measurements when an image or real-world specification exists. For common asset families, consult:

- `references/dimensions/trees.md`
- `references/dimensions/rocks-and-mountains.md`
- `references/dimensions/buildings.md`
- `references/dimensions/props.md`
- `references/dimensions/vehicles.md`
- `references/dimensions/characters.md`

For procedural assets, preserve a base template and expose controlled variation instead of inventing unrelated dimensions for every instance.

## Reference Routing Update

When the request is primarily procedural, read `references/07-procedural-and-symmetry.md` and use a deterministic seed when reproducibility matters. When terrain is the subject, also read `references/dimensions/rocks-and-mountains.md`. When a machine-readable result is requested, read `schemas/model-blueprint.schema.json` before generating it.

## Quick Start (minimum viable plan)

If you must be brief, still deliver: coordinate system + base unit, component table with dimensions and positions, numbered construction steps, material table with hex colors, shading mode per component, triangle estimate, and the validation checklist. Never drop Sections 1, 4, 5, 7, 9.
