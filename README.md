# Universal Low-Poly 3D Modeling Skill

A reusable AI skill that turns a **text description**, a **reference image**, **multiple images**, or a **mix of both** into a complete, **software-independent** low-poly 3D model construction plan.

It is not a Blender tutorial. It is a construction specification that another AI, a human artist, a procedural system, or a technical artist can execute in **Blender, Maya, 3ds Max, Houdini, Cinema 4D, Unity, Unreal Engine, Godot, Three.js, OpenSCAD**, or any other modeling environment.

---

## What it produces

Every request is answered as a **model construction plan**, not a visual description.

The plan always covers:

1. Overall silhouette
2. Major components
3. Primitive shapes needed
4. Approximate dimensions and proportions
5. Placement of each component
6. Rotation of each component
7. Polygon / vertex density
8. Required topology
9. Which edges and faces to modify
10. Materials
11. Colors (with hex)
12. Flat vs smooth shading
13. Symmetry
14. Repetition / instancing
15. Detail level
16. Optimization
17. Final assembly
18. Export considerations

The output format is fixed (see `SKILL.md` and `assets/templates/model-plan-template.md`) so plans are machine-checkable with `python scripts/validate_plan.py`.

---

## Design principles

- Strong, recognizable silhouette
- Simple geometry, low polygon count, efficient topology
- Flat shading unless a component genuinely benefits from smoothing
- Large readable forms, no geometry added for complexity's sake
- Stylized proportions when appropriate
- Reusable components, symmetry, and instancing
- Intentionally low-poly, never unfinished

---

## Repository layout

```
SKILL.md                              Skill definition (read this first)
references/
  01-reference-image-analysis.md      How to read photos / concept art
  02-style-and-polygon-budgets.md     Style target and triangle ranges
  03-model-decomposition.md           Breaking objects into parts
  04-primitives-and-recipes.md        Primitive recipes and operations
  05-dimensions-and-proportion.md     Base units and proportion systems
  06-materials-color-shading.md       Palette, PBR, shading modes
  07-procedural-and-symmetry.md       Arrays, mirrors, instancing
  08-optimization-topology.md         Cleanup, topology, LODs
  09-validation.md                    Final checklist
  10-software-implementation.md       Optional per-DCC / engine notes
  11-uv-textures.md                   When (not) to texture
  12-game-ready-and-export.md         Real-time, pivots, formats
assets/
  templates/model-plan-template.md    Blank plan
  examples/
    hammer.md                         Text-only prop
    pickup-truck.md                   Multi-image + Unreal
    pine-tree-threejs.md              Procedural + Three.js
    stylized-character.md             Stylized character
scripts/validate_plan.py              Structural checker for plans
```

---

## How to use with an AI

1. Load `SKILL.md` as the skill.
2. Give the model a request: a description, one or more images, a target use, and optionally a target application.
3. The model writes a plan matching the 10-section contract.
4. Optionally run `python scripts/validate_plan.py path/to/plan.md`.
5. Build the model from the plan in any 3D tool. Section 10 appears only if you named software.

**Vague requests are filled with labeled assumptions.** Image evidence is labeled Observed / Inferred / Recommended. Hidden geometry is never presented as if it were visible.

---

## Example prompts

- "Make a low-poly claw hammer."
- "Turn this photo into a low-poly crate for Unity."
- "Low-poly pickup truck from these three references, Unreal, drivable hero vehicle."
- "Procedural pine trees for a Three.js forest, hundreds of instances."
- "Stylized low-poly goblin, game-ready, Godot."

Worked plans for the first four styles live in `assets/examples/`.

---

## Validating a plan

```bash
python scripts/validate_plan.py assets/examples/hammer.md
python scripts/validate_plan.py assets/templates/model-plan-template.md --lenient
```

The checker verifies the 10 required headings, the component and material tables, hex colors, a coordinate-system block, and (unless `--lenient`) that construction steps name primitives and operations.

---

## License

MIT. See `LICENSE`.
