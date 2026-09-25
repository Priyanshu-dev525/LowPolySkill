# Primitives & Construction Recipes

## 1. Primitive selection guide

| Primitive | Best for | Low-poly settings | Watch out for |
| --------- | -------- | ----------------- | ------------- |
| **Cube** | Boxes, crates, bodies, buildings, machine housings | 1×1×1, 8 verts / 12 tris | Always scale it; never leave a unit cube in the plan |
| **Plane** | Ground, water, cloth quads, decals, cross-plane foliage | 1×1, 2 tris | Single-sided; state if it needs to be double-sided |
| **Cylinder** | Poles, handles, wheels, pipes, trunks, caps, barrels | 6–16 sides; 8–12 for wheels | Cap it: no-cap cylinders are open holes |
| **Cone** | Spikes, horns, tips, roofs, tree canopies, funnels | 4–10 sides | Sharp apex reads great in low poly; keep it |
| **Sphere** | Round organic masses, eyes, fruit, domes (use sparingly) | UV sphere 8×6 max | High tri cost for the shape; prefer icosphere |
| **Icosphere** | Rock, canopy, blobs, heads, organic masses | Subdivision 0 (20 tris) or 1 (80 tris) | Very efficient; the go-to low-poly "blob" |
| **Capsule** | Limbs, antennae, rounded handles, bolts | 6–8 radial, 1–2 height segments | Usually collapses to a low-side cylinder + caps |
| **Torus** | Rings, tires, donuts, hoops, handles | 8–16 major, 6–10 minor | Expensive; only when the hole is visible |
| **Pyramid / prism** | Roofs, spikes, crystals, teeth, arrowheads | 3–6 sides | Cheap silhouette wins |
| **Custom polygon** | Profile shapes, wings, claws, plate silhouettes | Drawn from a side view, then extruded | Best return on effort for non-box shapes |
| **Extruded polygon** | Any shape with a constant cross-section | Draw profile, extrude, taper | Combine with taper and twist for variety |

**Default choices:** boxes and low-side cylinders build ~80% of hard-surface low poly. Icospheres and cones build most of the organic rest. Reach for a torus or a sphere only when the form genuinely needs it.

---

## 2. Reusable recipes

Each recipe: start → transforms → edits → shading.

### Tapered shaft / handle
1. Create a 6-sided cylinder, height 1.0, radius 0.5 (with caps).
2. Scale to the target length along its long axis.
3. Select the end ring, scale to 0.75× to taper.
4. Optionally select the opposite ring and scale to 0.9× for a subtle belly.
5. Add one loop cut near each end if a grip band is needed.
6. Flat shading.
*Use for: handles, poles, bones, pipes, table legs, tree trunks.*

### Wheel / disc
1. Create a cylinder with 10–12 sides, caps enabled.
2. Orient so its axis is horizontal and points along the vehicle's left-right axis.
3. Scale to diameter × width (typical: diameter 1.0, width 0.28 of diameter).
4. Select both cap faces, inset once, then extrude slightly inward or outward to form the hub face.
5. Optionally bevel the outer rim with 1 segment.
6. Flat shading. Model once; instance for all other wheels.
*Use for: wheels, gears, discs, lids, coins.*

### Rounded box / chunky mass
1. Create a cube and scale to target dimensions.
2. Bevel all edges 1 segment, width ~4–6% of the shortest dimension.
3. Optionally delete the small corner triangles if the budget is tight.
4. Flat shading for a machined look, or smooth with hard edges for a soft-toy look.

### Faceted dome / rock / canopy
1. Create an icosphere, subdivision 0 or 1.
2. Scale non-uniformly to the target mass.
3. Delete or flatten the bottom faces (or leave them; they are hidden inside the trunk).
4. Move individual vertices by small amounts (5–10% of radius) to break perfect symmetry — this is what makes it read as natural.
5. Flat shading.

### Spike / horn / tooth
1. Create a 4–6 sided cone.
2. Scale along the long axis to the target length.
3. Rotate to the mounting angle.
4. Optionally bend: add 2–3 loop cuts along the axis and offset each ring progressively.
5. Flat shading. Instance with a radial array for crowns or teeth.

### Curved / bent pipe
1. Create a 5–6 sided cylinder.
2. Extrude the end ring segment by segment, rotating each new segment by the bend increment (e.g. 6 segments × 15° for a 90° elbow).
3. Weld the final ring to the receiving surface.
4. Keep segment count at the minimum where the bend still reads.

### Panel / plate with thickness
1. Create a cube or a drawn polygon.
2. Scale to width × height × thin depth.
3. Inset the front face once for a border if a frame is needed, then extrude the inset face outward by a hair.
4. Flat shading with hard edges.

### Organic limb
1. Create a 6–8 sided cylinder with 2–3 height segments (or a low capsule).
2. Scale the end rings to taper toward the joint.
3. Position the pivot at the joint end.
4. Add 1 extra ring near the joint so bending does not collapse the silhouette.
5. Smooth shading for organic, flat for stylized/toy.

### Window unit (arrayable)
1. Create a plane or very thin cube matching the opening.
2. Inset the face once to create a frame border; extrude the border outward slightly.
3. Assign the glass material to the inner face, frame material to the border.
4. Duplicate with an array along the facade; vary one or two instances slightly so the repetition does not look mechanical.

### Bevel-only light catcher
Instead of modeling a rim: bevel the most camera-facing edges with 1 segment, ~3–5% width. In flat shading this reads as a highlight line at zero meaningful triangle cost.

---

## 3. Operation discipline

| Operation | When to use | Low-poly caution |
| --------- | ----------- | ---------------- |
| Extrude | Adding volume from a face | The cheapest way to add form; use first |
| Inset | Creating borders, panels, recesses | Prefer over modeling a separate frame |
| Bevel | Catching light, softening edges | 1 segment, small width; bevels multiply triangles fast |
| Loop cut | Adding a bend or a proportion change | One loop per needed feature, no more |
| Bridge | Connecting two openings | Great for handles and tubes |
| Boolean | Complex cuts, holes, unions | Last resort — it generates messy topology. Plan a cleanup step (dissolve, weld, retriangulate) |
| Mirror | Symmetric halves | Model one side, mirror on the stated axis, weld the seam |
| Array / radial array | Repeated units | Use instances, not copies, when the target supports it |
| Subdivide | Adding needed density | Almost never — if you need density you needed a different primitive |
| Dissolve / weld | Cleanup | Run after booleans and mirrors |
| Flip / recalculate normals | Fixing inside-out faces | Always validate at the end |

---

## 4. Writing a construction step

Format:

```
### <Part name> (<base primitive>, ~<n> tris)

1. Create a <primitive> with <parameters>.
2. Scale to <X> × <Y> × <Z> units.
3. Move to (<x>, <y>, <z>) — <describe what that location is>.
4. Rotate to (<rx>, <ry>, <rz>)° — <why>.
5. Select <which faces/edges>.
6. <Operation> by <amount>.
7. <Cleanup operation>.
8. Assign material <name>. Shading: <flat | smooth | hard/soft edges>.
```

Rules:
- Always say which faces or edges are selected before an operation on them.
- Always give the numeric amount.
- Never write "adjust as needed." Give the number and, if it is genuinely a taste call, give the range.
