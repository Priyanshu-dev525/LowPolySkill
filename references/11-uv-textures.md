# UV & Texture Guidance

## 1. Decide whether a texture is needed at all

| Situation | Recommendation |
| --------- | -------------- |
| Solid-color stylized asset | **No texture.** Flat materials only. |
| A few color regions (2–6) | **Vertex colors** or separate material slots / a tiny palette atlas |
| Pattern that follows the surface (stripes, panels, numbering) | Small **trim sheet** or a palette atlas |
| Unique detailed surface (a face, a poster, a logo) | Dedicated small **texture atlas** |
| Hero asset in a realistic style | Full PBR set at an appropriate resolution |
| Background / instanced asset | No unique texture; share an atlas across many assets |
| 3D print | No texture (or vertex colors for multi-material printing) |

**Default for low poly: no textures.** Every texture you add costs memory, an authoring step, and a place for things to go wrong. If the asset reads correctly with flat colors, ship flat colors.

---

## 2. UV strategy by asset type

| Asset | Strategy | Notes |
| ----- | -------- | ----- |
| Simple box prop | Box projection, or leave the default unwrap | With flat colors you may not even need UVs — but still export valid UVs, engines expect them |
| Cylinder (handle, pole, wheel) | Seam along one hidden side; unwrap the band as a rectangle; caps as circles | Keep the seam on the back |
| Symmetric character | Half UVs + mirrored UVs for the other side (doubles effective resolution) | Offset the mirrored half so it is not perfectly identical if you want asymmetry |
| Vehicle | One atlas for the body; separate small atlas or solid color for glass and wheels | Windows can share a glass material with no UV dependency |
| Repeated elements (windows, bricks) | All copies share the **same** UV region (trim sheet reuse) | This is why arrays are cheap |
| Environment kit | Shared trim/atlas sheet across all kit pieces | Keeps material count low and allows batching |
| Foliage | Single atlas for leaf cards | Alpha/clip, not blend, for foliage |

---

## 3. Texture resolution guidance

| Asset class | Resolution | Notes |
| ----------- | ---------- | ----- |
| Small prop, mobile | 256×256 or none | Often flat color is better |
| Standard prop (desktop/console) | 512×512 | The workhorse |
| Hero prop seen up close | 1024×1024 | |
| Hero character | 1024–2048 | Face may get its own region |
| Large environment piece | 1024–2048 with trim reuse | |
| Background / crowd | 256 or shared atlas | |
| Foliage atlas | 512–1024 | |

Rules: power-of-two resolutions; reuse one atlas across many assets; prefer **trim sheets** over unique textures for anything with repeated surface features; never ship a texture whose resolution the camera will never resolve.

---

## 4. Texture types

| Map | Needed for low poly stylized? | Notes |
| --- | ----------------------------- | ----- |
| Base color | Sometimes | Often replaced by flat material color or vertex color |
| Roughness/metallic | Rarely | A single scalar value per material is usually enough |
| Normal map | Rarely | Geometry should carry the form; normal maps fight flat shading |
| Ambient occlusion | Sometimes | Baked AO adds grounding cheaply |
| Emission | Sometimes | Screens, lamps, glowing trim |
| Alpha | For foliage/cards | Use alpha clip, not alpha blend, where possible |

**Anti-pattern:** baking normal maps that fake geometry you could have modeled in 20 triangles. In low poly, model it.

---

## 5. UV checklist

- [ ] No overlapping islands (unless intentional reuse/mirroring)
- [ ] No severe stretching (check with a checker map)
- [ ] Seams placed on hidden edges or hard angle changes
- [ ] Consistent texel density across the asset (or deliberately higher on focal areas)
- [ ] Islands packed with a small padding (2–4 px at 512, scaled with resolution)
- [ ] All copies of a repeated element share UV space (trim reuse)
- [ ] UVs exist and are valid even if the material is flat color (engines expect UV0)
- [ ] For mirrored meshes: UVs offset so the halves are not identical islands
