# Target Style & Polygon Budgets

## 1. Choose the style target first

Before anything else, fix these five variables and state them in Section 2. Every later decision follows from them.

| Variable | Options | Default recommendation |
| -------- | ------- | ---------------------- |
| **Polygon density** | ultra-low (<300 tri), prop (300–1.5k), hero (1.5k–5k), hero-plus (5k–15k) | Match object size and camera distance |
| **Silhouette philosophy** | true-to-reference, stylized/exaggerated, chunky/toy, geometric/abstract | Exaggerate 10–20% on identity features |
| **Shading model** | fully flat, mostly flat with selective smoothing, smooth with hard accents | Flat by default |
| **Proportions** | realistic, stylized (big head / chunky limbs), toy/rounded | Stylized unless realism was requested |
| **Level of detail** | silhouette only, silhouette + functional parts, + major surface detail | Silhouette + functional parts |

---

## 2. Polygon budget table

Recommend a **range** with a reason. Never present an invented number as a requirement.

| Category | Triangles | Typical use | Notes |
| -------- | --------- | ----------- | ----- |
| Micro prop / icon asset | 20–300 | Cutlery, coins, keys, small debris, inventory icons | 1–2 primitives, often a single material |
| Small game prop | 100–1,000 | Chairs, barrels, crates, lamps, tools, small plants | The bread and butter range |
| Medium prop | 1,000–3,000 | Doors, furniture, weapons, machinery, small creatures | Detail starts to matter |
| Hero / large object | 1,000–5,000 | Vehicles, large creatures, centerpiece props | Budget distributed by visibility |
| Hero character | 3,000–10,000 | Playable characters, NPCs seen up close | Face and hands take disproportionate budget |
| Large environment piece | 2,000–8,000 | Buildings, ships, terrain features, large trees | Spend on silhouette, not surface |
| Background / crowd / foliage | 30–500 | Distant props, background characters, foliage clusters | Aggressive instancing; LODs mandatory |

**Camera-distance rule:** if the camera never gets closer than X, the smallest feature worth modeling is roughly X/40. Anything smaller becomes material.

**Budget allocation rule (hero assets):** spend triangles where the eye goes.
- Head / face / focal detail: 25–35%
- Hands and contact points: 10–15%
- Main body mass: 25–35%
- Everything else: the remainder

**Never:** spend budget evenly across the model. Even spending produces a model that is detailed everywhere and interesting nowhere.

---

## 3. Silhouette philosophy

A low-poly model is read as an outline first, as shading second, and as detail last.

**Exaggeration targets (stylized work):**
- Identity features (a shark's fin, a hammer's claw, a truck's cab) → push 15–25% larger or more angular than reference
- Contact points (feet, tires, base) → slightly oversized so the object looks grounded
- Tapering ends → sharpen the taper; low poly loses subtlety
- Negative space → widen gaps; thin gaps fill in visually at distance

**Silhouette self-test:** describe the outline in one sentence without naming the object. If a stranger could not guess it, add or strengthen an outline feature, and delete interior geometry to pay for it.

---

## 4. Detail level decision

| Use case | Detail level |
| -------- | ------------ |
| Inventory icon, top-down/RTS camera | Silhouette + one or two color breaks |
| First-person held object | Full functional detail; visible moving parts modeled separately with pivots |
| Third-person character | Readable face, hands, and equipment; skip interior |
| Open-world environment prop | Silhouette + material variation; heavy instancing |
| Cinematic / portfolio hero | Highest detail the budget allows; selective smoothing on organics |
| 3D print | Avoid razor-thin features, avoid non-manifold geometry, keep wall thickness ≥ 1 mm at print scale |

---

## 5. Stylized vs realistic proportions

| Choice | When | How |
| ------ | ---- | --- |
| Stylized | Characters, creatures, props for stylized games, icons, toys | Enlarge the head/face, shorten and thicken limbs, round hard corners, exaggerate asymmetries |
| Realistic | Vehicles, architecture, hard-surface replicas, product visualization | Keep measured proportions; simplification comes from removing detail, not distorting form |
| Chunky / toy | Casual/mobile games, cute assets | Thicken everything, reduce part count, unify materials, use saturated colors |
| Geometric / abstract | Backgrounds, UI-adjacent 3D, motion graphics | Reduce to pure primitives; let color and light do the work |

State the choice in Section 2 with one line of justification, e.g. *"Stylized: exaggerated head and shortened limbs, because the asset is a cartoon NPC read at 5–15 m."*
