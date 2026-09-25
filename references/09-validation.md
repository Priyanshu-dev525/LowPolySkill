# Final Validation

Every plan ends with this checklist. Each item needs a **pass condition** — a way to check it, not a vibe.

```markdown
## 9. Final Validation

| # | Check | Pass condition | Status |
| - | ----- | -------------- | ------ |
| 1 | Silhouette recognizable | The object is identifiable from a solid-black silhouette at the target camera distance | ☐ |
| 2 | Proportions correct | All parts sum to the stated total dimensions (±3%) | ☐ |
| 3 | No unnecessary geometry | Every face is visible, structural, or material-separating | ☐ |
| 4 | Normals correct | No inverted normals; no black or inside-out faces from any angle | ☐ |
| 5 | Materials assigned | Every face has a material; no default/gray faces | ☐ |
| 6 | No duplicate geometry | Weld test passes; no overlapping coplanar faces | ☐ |
| 7 | Polygon budget respected | Final triangle count is inside the recommended range | ☐ |
| 8 | Model ready for export | Correct scale, up axis, applied transforms, pivot at the stated origin | ☐ |
```

## Extended checks (add when relevant)

| Check | Pass condition |
| ----- | -------------- |
| Symmetry | Mirrored parts are at exactly mirrored coordinates |
| Instances | Repeated parts are instances (or intentionally varied copies) |
| Pivots | Every animated/moving part has its pivot at its rotation point |
| Shading | Every component has an explicit flat/smooth/weighted assignment |
| UVs | If textured: no overlapping islands (unless intentional), no stretched faces |
| Naming | All objects follow the stated convention; no default names |
| Scale | Object measures correctly against the intended real-world size |
| Origin | Origin is where the plan said it would be (usually base center / ground contact) |
| Manifold | If required (printing, booleans, physics): the mesh is closed |
| LODs | If required: chain exists and silhouettes match |
| Collision | Collider type defined and fitted |
| Texture budget | Texture count and resolution match the stated platform target |

## Plan-quality checks (for the plan itself, not the model)

Before delivering, verify the plan:

- [ ] Every component in the table has dimensions **and** a position — no empty cells
- [ ] Every component in the table appears in the construction steps
- [ ] Construction steps name the primitive, the numbers, and the selected faces/edges
- [ ] Coordinates are all relative to the stated origin and up axis
- [ ] Parts that stack sum to the stated whole
- [ ] Per-part polygon estimates add up to the Section 2 budget range
- [ ] Every material has a hex color, roughness, metallic, and shading
- [ ] Software-specific instructions appear only in Section 10
- [ ] Observed / Inferred / Recommended labels are used wherever a reference was involved
- [ ] Assumption(s) that could change the model are stated up front

Run `python scripts/validate_plan.py <plan.md>` to machine-check the structural items.
