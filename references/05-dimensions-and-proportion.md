# Dimensions, Base Units & Proportion

## 1. Base unit system

When no real-world scale is given, define one base unit and derive everything from it.

```
Base unit: treat the total character height as 10 units.
```

Then express every part relative to it, and **check that the parts sum to the whole**.

### Character template (total height = 10.0)

| Part | Realistic | Stylized | Notes |
| ---- | --------- | -------- | ----- |
| Head | 1.3–1.4 | 2.0–2.6 | Stylized heads run large |
| Neck | 0.3 | 0.2–0.3 | Often merged into torso |
| Torso | 3.0–3.2 | 3.0–3.4 | Shoulder to hip |
| Hips | 0.9 | 0.9 | |
| Legs | 3.8–4.0 | 3.2–3.6 | Stylized legs run short |
| Feet | 0.9–1.0 | 1.0–1.2 | Oversize slightly for grounding |
| Shoulder width | 2.0–2.4 | 2.2–2.8 | |
| Arm length | 3.0 | 2.6–3.0 | Including hand |

### Vehicle template (total length = 10.0)

| Part | Value |
| ---- | ----- |
| Body length | 10.0 |
| Body width | 4.0–4.4 |
| Body height (ground to roof) | 3.0–3.6 |
| Wheel diameter | 1.6–2.0 |
| Ground clearance | 0.5–0.8 |
| Cabin length (sedan) | 4.0–4.5 |
| Hood length | 2.5–3.0 |
| Track width | 3.4–3.8 |

### Prop template (height = 1.0 when scale is irrelevant)
Design at 1.0 unit tall and note the real-world scale to apply on export (e.g. "scale 100× for a 1 m barrel in a 1-unit = 1 m engine").

---

## 2. Proportion rules that read well

| Rule | Reason |
| ---- | ------ |
| Head = 1/7 of height realistic, 1/5–1/4 stylized | Stylization reads through head size |
| Contact points slightly oversized | Objects look grounded, not floating |
| Taper ends more than the reference | Subtle tapers vanish at low poly |
| Widen negative spaces (gaps between legs, arms, spokes) | Gaps close up visually at distance |
| Round-count symmetry: use 6, 8, 10, 12 sides, not 7 or 9 | Even counts mirror cleanly and look intentional |
| Keep wall/plate thickness consistent (e.g. always 0.08 units) | Inconsistent thickness reads as sloppy |
| Make the largest mass at least 3× the smallest major mass | Avoids visual noise |

---

## 3. Positioning convention

Give positions as coordinates relative to the stated origin, in this order:

| Object type | Origin | Axes |
| ----------- | ------ | ---- |
| Character / creature | Center of feet contact, on the ground plane | Y up, −Z or +Z forward |
| Vehicle | Center of the wheel contact plane, mid-wheelbase | Y up, +Z or +X forward (state which) |
| Prop that sits on a surface | Center of the base contact area, at Y = 0 | Y up |
| Handheld / weapon | The grip point where the hand wraps (so it snaps to a socket) | Y up, barrel along +Z |
| Building | Center of the footprint at ground level | Z up is common in architecture — state it |
| Floating object | Its visual center of mass | Y up |

**Always state the coordinate convention in Section 3.** The most common cause of a failed plan is an unstated up axis.

Example:
```
Coordinate System
- Up axis: Y
- Forward: −Z
- Origin: center of the base, at ground level (Y = 0)
- Overall dimensions: 3.2 W × 10.0 H × 2.4 D units
- Base unit: total height = 10.0 units
```

---

## 4. Consistency check (run this before delivering)

1. Do the parts that stack along an axis sum to the stated total? (head + neck + torso + hips + legs + feet ≈ total height)
2. Is any part larger than the object it belongs to?
3. Are symmetric parts at mirrored coordinates (±x or ±z, same y)?
4. Do mating surfaces actually touch? (a leg top at Y = 4.0 when the torso bottom is at Y = 4.0, not 4.3)
5. Are thickness values consistent across similar parts?
6. Does the bounding box match the "overall dimensions" line in Section 3?

Fix any failure before writing the final plan. A plan with drifting proportions is worse than no plan.
