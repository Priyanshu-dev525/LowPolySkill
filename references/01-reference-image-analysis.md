# Reference Image Analysis

Read this file whenever the user supplies a photo, screenshot, sketch, render, or concept art.

**Goal:** extract construction-relevant information from the image, and decide which details become geometry and which become material.

**Key principle:** do not blindly reproduce every visible detail. Prioritize the features that make the object recognizable at the target polygon count.

---

## 1. Analysis Pass (do this in order)

### 1.1 View & camera
| Question | Why it matters |
| -------- | -------------- |
| What is the camera angle? (front / side / 3-4 / top-down / low hero angle) | Tells you which faces you can trust |
| Is it orthographic or perspective? | Perspective distorts relative sizes — do not trust pixel measurements between near and far parts |
| Roughly what focal length / how much distortion? | Wide-angle exaggerates near features; a big "nose" may be lens, not form |
| What is hidden? | Everything you cannot see is Inferred or Recommended, never Observed |

State the view angle in the Reference Read section: *"Observed: 3/4 front-left view, slightly above eye level, mild perspective."*

### 1.2 Silhouette
Trace the outline mentally and describe it as a stack of simple shapes. Ask:
- If I filled the silhouette solid black, would you still recognize the object? If not, the silhouette needs exaggeration.
- Where are the notches, spikes, overhangs, and negative spaces that carry identity?
- Which outline features must survive at low poly (the hook of a hammer claw, the two humps of a camel, the taper of a sword tip)?

### 1.3 Form hierarchy
| Level | What it is | Low-poly treatment |
| ----- | ---------- | ------------------ |
| **Primary** | The big masses that define the object (body, head, chassis) | Always geometry. Get these exactly right. |
| **Secondary** | Functional sub-forms attached to primaries (windows, wheels, limbs, buttons) | Usually geometry, heavily simplified |
| **Tertiary** | Surface detail: panel lines, bolts, stitching, grain, wear, logos, text | Almost never geometry — material, color break, decal, or omit |

Rule of thumb: at under ~1,000 triangles, tertiary detail has no polygons to spend. It becomes color or gets deleted.

### 1.4 Proportions & relative dimensions
- Pick the largest reliable measurement in the image as the reference span (usually overall height or length).
- Express everything else as a fraction of it: "head is ~0.22 of total height."
- **Correct for perspective:** parts closer to the camera measure larger. Flag any measurement taken across depth as approximate.
- **Correct for foreshortening:** a wheel seen at an angle is an ellipse; its true radius is the ellipse's major axis.

### 1.5 Symmetry
Check for bilateral symmetry (left/right), radial symmetry (wheels, flowers, domes), and translational repetition (fence pickets, windows, treads).
- If one side is visible and looks symmetric, the mirror is **Inferred**, not Observed.
- Symmetry is the biggest polygon saving available: model 1/n of the object.

### 1.6 Materials & surface character
For each visible surface note:
- Base color (sample it; give a hex)
- Roughness: matte (chalk, rubber, cloth, unpolished wood) vs glossy (glass, paint, polished metal, wet surfaces)
- Metal vs non-metal: does it show colored specular and strong reflection, or white/dim specular?
- Transparency / translucency: glass, water, leaves, lampshades, glowing parts
- Emission: screens, lamps, lasers, glowing trim
- Surface quality: hard-edged machined, soft/organic, faceted, rounded worn

### 1.7 Recognizability audit
List the 3–5 features without which the object stops being itself. These get geometry priority.
Example — a low-poly police car: light bar, two-tone body split, boxy sedan silhouette, wheels with hubs. Everything else (door handles, mirrors, trim) is optional.

---

## 2. Geometry vs Material Decision

For every detail, run this filter:

| Test | Verdict |
| ---- | ------- |
| Does it change the **silhouette** from any useful angle? | → Geometry |
| Does it create a hard **material boundary** (glass next to paint)? | → Separate geometry (or a separate material slot on a separated face set) |
| Does it create a strong **self-shadow** or cast shadow? | → Geometry, if budget allows |
| Is it a **surface pattern** that lies flat on the form? | → Material / vertex color / decal |
| Is it **smaller than ~2% of the object's largest dimension**? | → Material or omit |
| Does it need to **move or animate**? | → Geometry, with its own pivot |
| Does the camera ever get **close** to it? | → Consider geometry |

Standard low-poly answers:
- Panel lines, seams, rivets, bolts → material or omit
- Text, logos, decals, numbers → material / texture / decal
- Wood grain, fabric weave, rust, grime → material or omit
- Small vents and grilles → **a single inset dark face** or a dark material patch (not 20 boxes)
- Windows on vehicles/buildings → flat or slightly inset faces with a glass material; do not model window frames unless large
- Foliage → crossed planes or a few faceted leaf clusters, never individual modeled leaves at prop scale

---

## 3. Multi-Image Handling

1. Analyze each image independently (view angle, observed features).
2. Merge into one object model of the object.
3. **Resolve contradictions explicitly.** Note what conflicts and which source you trust, and why (e.g. "Image 1 shows 4 wheels, Image 2 shows 6; trusting Image 1 because Image 2 is a different trim variant — flagged as Inferred").
4. Build a coverage map: which regions are confirmed by ≥1 image, and which are entirely unseen.
5. For unseen regions, state a Recommended solution.

Output format:

```
Reference Read
- Image 1: 3/4 front-left, outdoor daylight. Confirms: body shape, 2 doors, wheel count.
- Image 2: rear view. Confirms: tail light layout, bumper depth.
- Unseen: underside, interior, roof detail → Recommended: flat underside plate, no interior.
```

---

## 4. What To Do With Bad References

| Situation | Response |
| --------- | -------- |
| Very low resolution | Lean on the text description; treat fine detail as unspecified |
| Heavy motion blur / dark / backlit | State that detail-level reads are unreliable; design from category knowledge and label as Recommended |
| Object occluded by other objects | Model only what is visible; Recommend plausible continuation |
| Reference is itself a 3D render | Great — note the shading model it uses and whether to match flat or smooth |
| Reference contradicts the text | Ask nothing. Follow the image for form, the text for intent, and note the conflict |
| Sketch/line art only | Colors are unspecified → propose a palette and label it Recommended |

---

## 5. Reference Read Block (paste into Section 1)

```markdown
**Reference Read**
- Images supplied: 2 (front 3/4, side)
- View angle: front 3/4, slightly high camera, mild perspective
- Confirmed (Observed): <list>
- Reasoned (Inferred): <list>
- Not visible (Recommended): <list>
- Recognizability drivers: <3-5 features>
- Detail deferred to material: <list>
- Silhouette risks: <what might read as generic, and the planned exaggeration>
```
