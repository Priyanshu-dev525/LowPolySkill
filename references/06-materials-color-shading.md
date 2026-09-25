# Materials, Color & Shading

## 1. Material table format

| Material | Color | Roughness | Metallic | Shading |
| -------- | ----- | --------- | -------- | ------- |
| `MAT_Body_Paint` | `#6B4A2F` | 0.55 | 0.0 | Flat |
| `MAT_Metal` | `#6E7378` | 0.35 | 1.0 | Flat, hard edges |
| `MAT_Glass` | `#4A6B73` | 0.10 | 0.0 | Smooth, transparent 0.7 |

Add columns or footnotes for: transparency/opacity, emission, texture vs flat color, double-sided.

---

## 2. PBR starting values (low-poly / stylized)

| Material class | Base color | Roughness | Metallic | Notes |
| -------------- | ---------- | --------- | -------- | ----- |
| Matte plastic / painted surface | as designed | 0.5–0.7 | 0.0 | The default for most low-poly assets |
| Glossy plastic / lacquered | as designed | 0.15–0.3 | 0.0 | Toy look |
| Painted metal | as designed | 0.35–0.5 | 0.8–1.0 | Car bodies, appliances |
| Bare steel | `#8A9099` | 0.25–0.4 | 1.0 | Tools, machinery |
| Weathered / rusty metal | `#6B5344` | 0.7–0.85 | 0.6–0.9 | Lower metallic with rust |
| Brass / gold | `#C9A227` | 0.3 | 1.0 | |
| Rough wood | `#6B4A2F` | 0.7–0.85 | 0.0 | |
| Polished wood | `#8B5A2B` | 0.3–0.4 | 0.0 | |
| Rubber / tire | `#1F2124` | 0.85–0.95 | 0.0 | Never pure black; use #1A1C1F–#2A2D31 |
| Cloth / fabric | as designed | 0.8–0.95 | 0.0 | |
| Glass | pale desaturated tint | 0.05–0.15 | 0.0 | Transparent 0.6–0.9; low roughness |
| Water | `#2E6C7E` | 0.1–0.25 | 0.0 | Transparent 0.5–0.8 |
| Foliage | mid-saturated green | 0.7–0.9 | 0.0 | Slight translucency if the engine supports it |
| Skin (stylized) | flat warm tone | 0.6–0.8 | 0.0 | |
| Emissive / glow | bright saturated | any | 0.0 | Emission strength 1.5–4.0 |
| Stone / concrete | `#8C8C86` | 0.85–0.95 | 0.0 | |

**Low-poly material rules:**
- Prefer **simple flat-colored materials**. Textures only when the user asks, or when a pattern is essential to identity.
- Keep material count low: **1–3 materials** for a prop, **2–5** for a hero asset, **1–2** for background/instanced assets.
- Avoid pure `#000000` and pure `#FFFFFF` — they crush shading. Use `#1A1C1F`–`#2A2D31` and `#EDEFF2`.
- Never rely on color alone to show form; the shading has to work in grayscale.

---

## 3. Palette construction

Use **3–6 colors** per asset. Structure:

| Slot | Share | Purpose |
| ---- | ----- | ------- |
| Dominant body color | 50–65% | The main read |
| Secondary color | 20–30% | Separates major components |
| Accent color | 5–15% | Draws the eye (identity features, lights, trim) |
| Neutral / dark | 5–15% | Tires, grips, recesses, grounding |

**Color separation principle:** adjacent components that must be told apart (blade vs handle, glass vs paint, rubber vs metal) should differ in **value** (lightness) by at least ~20%, not just hue. Value separation survives bad lighting; hue separation alone does not.

**Palette example (hammer):**
```
Wood handle   #6B4A2F
Grip rubber   #26282B
Steel head    #6E7378
Face highlight #9AA1A8
Accent stripe #C8452F
```

**Saturation guidance:**
- Stylized / cartoon: saturation 60–85%, value contrast high
- Realistic-ish: saturation 30–55%
- Background assets: slightly desaturated and value-flattened so heroes pop
- Mobile / small screens: push saturation and contrast up ~15%

---

## 4. Shading decisions

| Mode | Use when | How |
| ---- | -------- | --- |
| **Flat faceted** | Default for classic low poly; hard-surface props, vehicles, buildings, stylized characters | Every face gets one normal; no smoothing across edges |
| **Smooth** | Organics, terrain, water, rounded blobs, skins | Average vertex normals; add hard edges where you want a crease |
| **Weighted / custom normals** | Low-poly cylinders that must look round, or stylized models that need soft shading without extra geometry | Manually align normals on the curved band, keep hard edges on caps |
| **Hard edges** | Creases, panel borders, anywhere two materials meet | Mark/split the edge so shading does not bleed across it |
| **Soft edges** | Curved surfaces, organic transitions | Let normals average |
| **Shade by angle** | Quick pass on mixed models | Auto-hard above ~40–60°; then fix by hand |

**Per-component shading is mandatory in the plan.** Example assignment:

| Component | Shading |
| --------- | ------- |
| Body panels | Flat |
| Wheels (cylinder band) | Smooth with hard edges on the cap rim |
| Glass | Smooth |
| Handle (cylinder) | Weighted normals or flat with 8+ sides |
| Canopy (icosphere) | Flat |

**Normal rules:**
- Every face must face outward. Run a normals check at the end.
- Mirrored geometry with negative scale flips normals — recompute after mirroring.
- Coplanar overlapping faces cause z-fighting — offset by ~0.5–1% of the object size, or delete the hidden face.
- Interior faces that are never seen (inside a closed box, under a base, the back of a wall) should be **deleted**, not just hidden.
