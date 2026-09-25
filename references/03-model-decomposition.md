# Model Decomposition

## 1. The decomposition order

Break every object into parts in this order. Working in this order prevents "detail first" mistakes.

1. **Structure / core mass** — the single form that carries the silhouette (body, chassis, trunk, torso)
2. **Shell / surfaces** — panels, hull plating, roof, outer skin
3. **Functional parts** — things that do something: wheels, blades, handles, doors, screens, limbs
4. **Interface parts** — where functional parts meet the core: joints, mounts, hubs, hinges, sockets
5. **Surface details** — bevels, insets, panel breaks, trim
6. **Accents** — badges, lights, tips, caps, tiny silhouette spikes

**Rule:** stop adding levels when the next level costs more than 5% of the budget and contributes nothing to the silhouette.

---

## 2. Part naming

Name parts so they are unambiguous in a hierarchy and in an outliner:

`<category>_<object>_<part>_<side><index>`

Examples: `PRP_Crate_Plank_L_01`, `CHR_Goblin_Arm_Upper_R`, `VEH_Truck_Wheel_F_L`.

Sides: `_L` / `_R`, `_F` / `_B`, `_T` / `_B`. Indexes start at 01. Mirrored parts usually keep a positive scale and are flagged as mirror instances rather than negative-scaled duplicates (negative scale flips normals).

---

## 3. Decomposition by category

### Characters / creatures
`torso · hips · head · neck · upper arm L/R · lower arm L/R · hand L/R · upper leg L/R · lower leg L/R · foot L/R · hair/helmet · equipment · eyes`
- Head ≈ 1/7 to 1/5 of total height realistic; 1/4 to 1/3 stylized.
- Model one side, mirror it, then break symmetry with equipment, hair, or pose.
- Joints: add one extra edge loop at each bend so deformation or posing does not collapse the form.

### Vehicles
`chassis/body · cabin · roof · windshield · side windows · hood · trunk · doors · fenders · bumpers · wheels ×n · hubs ×n · headlights · taillights · grille · mirrors · exhaust · roof rack · interior (only if visible)`
- Wheels: model one, instance the rest. Cylinder 8–14 sides; flat-shaded 10–12 sides reads as round.
- Glass: separate material on inset faces; do not model thickness unless it is seen edge-on.

### Buildings / architecture
`foundation · main mass · roof · floors/bands · window units · doors · cornice · chimney · balcony · stairs · trim · signage`
- One window unit → array along the facade and across floors.
- Roof: extruded polygon or prism; keep it to 1–3 pieces.
- Repetition is the whole budget story here: 1 window + arrays = 200 triangles; 40 modeled windows = 2,000.

### Weapons / tools
`grip · guard · blade/head · pommel · shaft/handle · binding · accent`
- Read at arm's length, so silhouette and a clean taper matter more than surface detail.
- Sharp edges: bevel once with a single segment, or leave hard and rely on flat shading.

### Props (furniture, containers, household)
`main volume · legs/supports ×n · top surface · hardware · wear accents`
- Legs: model one, array radially or place as instances.
- Chips and wear: color/material, not geometry.

### Plants / nature
`trunk · branch splits · canopy mass (1–5 faceted clusters) · ground contact · leaves (crossed planes or clusters)`
- Never model individual leaves at prop scale.
- Canopy: 1–3 icospheres (subdivision 0–1) flattened, or 3–5 intersecting cone/pyramid masses.

### Machines / hard surface
`frame · housing · moving assembly ×n · control panel · vents (single inset face) · pipes/cables (low-side cylinders or curves) · bolts (material only)`
- Pipes: 5–6 sided cylinders with curved segments only where the bend is visible.

---

## 4. Components that should be separate objects vs merged

| Keep separate when | Merge when |
| ------------------ | ---------- |
| It animates or moves | It is static and shares a material |
| It is instanced (wheels, bolts, pickets) | Merging saves draw calls and it never moves |
| It needs its own pivot | The joint between them is hidden |
| It needs a different material on a game mesh (draw-call tradeoff) | Materials can be combined into one atlas |
| It will get its own LOD | — |

---

## 5. Worked micro-example: hammer

| Part | Purpose | Base shape | Notes |
| ---- | ------- | ---------- | ----- |
| Handle | Grip, defines length | Cylinder 6 sides | Tapered, slight bend optional |
| Head | Striking mass | Cube | Crosses handle at 90° |
| Face | Contact surface | Cube (end of head) | Slightly larger, flat, chamfered |
| Claw | Identity feature | Extruded tapered polygon | Split/tapered horn shape |
| Grip | Material separation | Cylinder 6 sides, slightly larger | Rubber material |
| Bevels | Catch light | Edge bevel, 1 segment | Only on the most visible edges |

The claw and the face are what make it a hammer. Everything else can be a plain box.
