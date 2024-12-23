# GNU Image Manipulation System

## Editing screenshots in Ubuntu

- Take a screenshot (Ubuntu 22.04.1 LTS):
  - Press `prt sc`
  - Select an area:
    - Drag left mouse button to select new area outside current selection or move current selection
    - Drag right mouse button to select new area starting inside current selection
  - Press `enter` or `ctrl+c`
- Open in GNU Image Manipulation System:
  - Click the screenshot notification to open the image in "Image Viewer"
  - Click the "hamburger" (menu button with 3 horizontal lines)
  - Select "Open With...", "GNU Image Manipulation System"
- Set options for highlighting:
  - Change foreground colour to yellow (HTML `ffff00`)
  - Press `shift+b` to select "Bucket Fill Tool"
  - Set "Opacity" to 50.0 (25.0 might look better on dark backgrounds)
  - Set "Fill Type" to "FG colour fill"
  - Set "Affected Area" to "Fill whole selection"
  - Set "Bucket Fill" to "Darken only" (light background) or "Lighten only" (dark background)
- Highlight an area:
  - Press `r` to select "Rectangle Select Tool"
  - Select an area (drag left mouse button)
  - Press `shift+b` to select "Bucket Fill Tool"
  - Set "Bucket Fill" to "Darken only" (light background) or "Lighten only" (dark background)
  - Click inside the selected area (click multiple times to effictively increase opacity)
- Copy edited image:
  - Press `ctrl+a`, `ctrl+c`
