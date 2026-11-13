# Custom Wallpaper Scenes & Clock Depth Layering

YourNewTV supports multi-layer wallpaper scenes where the giant ambient clock sits dynamically *behind* natural landscape features (mountain ridges, forest tree lines, or ocean horizons) using transparent WebP foreground masks and blurred frosted-glass backings.

---

## 1. Anatomy of a Scene

A complete multi-layer scene consists of three assets:

1. **`scene-<name>.jpg` (1920x1080, optionally `@2x.jpg` for 4K)**: The primary background image.
2. **`scene-<name>-fg.webp`**: The foreground cutout with the sky made 100% transparent. This renders *above* the clock digits, creating the optical depth illusion that the clock is part of the physical environment.
3. **`scene-<name>-glass.jpg`**: A brightened, blurred version of the scene used to fill the frosted glass clock numbers.

---

## 2. Generating Your Own Scene

### Step 1: Choose Your Image
Select a high-resolution landscape photo with a distinct horizon or skyline (mountains, coastlines, city skylines, forests). Crop to **1920x1080** (16:9).

### Step 2: Create the Foreground Cutout (`-fg.webp`)
Using any photo editor or AI mask tool:
1. Remove the sky completely, leaving only the foreground elements (mountains, trees, structures).
2. Save as a lossless or high-quality WebP with alpha transparency (`cwebp -q 85 -alpha_q 100 -exact cutout.png -o scene-custom-fg.webp`).
3. Keep the cutout edges clean with a 1px anti-aliased feather to prevent white halo artifacts around clock digits.

### Step 3: Create the Glass Texture (`-glass.jpg`)
Generate a blurred, ambient fill using ImageMagick:
```bash
magick scene-custom.jpg -blur 0x16 -modulate 130,125 scene-custom-glass.jpg
```

---

## 3. Registering the Scene

Place your generated assets in `src/web/backgrounds/` and add the scene entry to `src/web/config.js` or `app.js`:

```javascript
SCENE_LIB.push({
  id: "custom_mountain",
  name: "Alpine Mist",
  credit: "Photo by YourName (CC BY-SA 4.0)",
  bg: "backgrounds/scene-custom.jpg",
  fg: "backgrounds/scene-custom-fg.webp",
  glass: "backgrounds/scene-custom-glass.jpg"
});
```

---

## 4. Hardware Optimization

All foreground layers use GPU rasterization (`transform: translateZ(0)` and `will-change: transform`) to maintain 60 FPS Leanback scrolling without consuming unnecessary EGL swapchain buffers on low-memory Android TV SOCs.
