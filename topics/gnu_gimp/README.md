# GNU Image Manipulation System

## Contents

- [GNU Image Manipulation System](#gnu-image-manipulation-system)
  - [Contents](#contents)
  - [Configure shortcuts](#configure-shortcuts)
    - [Custom shortcuts](#custom-shortcuts)
    - [Default shortcuts](#default-shortcuts)
  - [Open screenshot in GIMP (Ubuntu 22.04.1 LTS)](#open-screenshot-in-gimp-ubuntu-22041-lts)
  - [Set options for highlighting](#set-options-for-highlighting)
  - [Highlight an area](#highlight-an-area)
  - [Outline an area](#outline-an-area)
  - [Highlight/outline multiple areas simultaneously](#highlightoutline-multiple-areas-simultaneously)
  - [Move an area](#move-an-area)
  - [Expand canvas size](#expand-canvas-size)
  - [Copy edited image](#copy-edited-image)
  - [Make speech bubble](#make-speech-bubble)
  - [Export as PNG](#export-as-png)

## Configure shortcuts

- Click "Edit", "Keyboard Shortcuts"
- Search for action name (EG "Stroke Selection")
- Click the "Shortcut" field next to the action name
- Press desired shortcut (EG `shift+s`)
- If a "Conflicting Shortcuts" box appears, click "Reassign Shotcut"
- Click "Save", "Close"
- To reset all keyboard shortcuts to default:
  - Click "Edit", "Preferences", "Interface", "Reset Keyboard Shortcuts to Default Values", "OK", "OK"
  - Restart GIMP

### Custom shortcuts

Action                      | Shortcut
---                         | ---
Tools/rectangle select      | `shift+r`
Tools/free select           | `shift+l`
Layers/alpha to selection   | `shift+z`
Select/stroke selection     | `shift+s`
Layers/anchor layer         | `shift+a`
Image/crop to selection     | `shift+c`
Tools/crop                  | `shift+e`
Layers/layer to image size  | `shift+i`
Edit/fill with FG colour    | `shift+f`
Layers/new layer            | `shift+n`
Layers/merge down           | `shift+m`
Tools/text                  | `shift+t`

### Default shortcuts

Action                    | Shortcut
---                       | ---
Tools/bucket fill         | `shift+b`
Select all                | `ctrl+a`
Paste in new image        | `ctrl+shift+v`
Open keyboard shortcuts   | `alt+e`, `k`
Reset FG/BG colours       | `d`
Swap FG/BG colours        | `x`
Export image to PNG       | `ctrl+shift+e`

## Open screenshot in GIMP (Ubuntu 22.04.1 LTS)

- Take screenshot:
  - Press `prt sc`
  - Select an area:
    - Drag left mouse button to select new area outside current selection or move current selection
    - Drag right mouse button to select new area starting inside current selection
  - Press `enter` or `space` or `ctrl+c`
- Open in GIMP:
  - Option 1:
    - Click the screenshot notification to open the image in "Image Viewer"
    - Click the "hamburger" (menu button with 3 horizontal lines), "Open With...", "GNU Image Manipulation System"
  - Option 2:
    - Open GIMP
    - Press `ctrl+v`
  - Option 3:
    - Open GIMP
    - Press `ctrl+o`
    - Select "Screenshots" folder
    - Sort by "Modified" (click "Modified")
    - Select most recent screenshot

## Set options for highlighting

- Press `shift+b` to select "Bucket Fill Tool"
- Set "Opacity" to 50.0 (25.0 might look better on dark backgrounds, 75.0 might look better on light backgrounds)
- Set "Fill Type" to "FG colour fill"
- Set "Affected Area" to "Fill whole selection"
- Set "Bucket Fill" to:
  - "Darken only" for light backgrounds
  - "Lighten only" for dark backgrounds

## Highlight an area

- Change foreground colour to yellow (HTML `ffff00`)
- Press `shift+r` to select "Rectangle Select Tool"
- Select an area (drag left mouse button)
- Press `shift+b` to select "Bucket Fill Tool"
- Set "Bucket Fill" to "Darken only" (light background) or "Lighten only" (dark background)
- Click inside the selected area (click multiple times to effictively increase opacity)

## Outline an area

- Change foreground colour to red (HTML `ff0000`)
- Press `shift+r` to select "Rectangle Select Tool"
- Select an area (drag left mouse button)
- Press `shift+s` to apply "Stroke Selection"

## Highlight/outline multiple areas simultaneously

- Press `shift+r` to select "Rectangle Select Tool"
- Select an area (drag left mouse button)
- Hold `shift` and select multiple additional areas
- To highlight:
  - Press `shift+b` and click inside one of the selected areas
- To outline:
  - Press `shift+s`

## Move an area

- Press `shift+r` to select "Rectangle Select Tool"
- Select an area (drag left mouse button)
- Hold `ctrl+alt` and drag selected area while holding left mouse button
- Press `shift+a` to anchor layer

## Expand canvas size

- Press `shift+e` to select "Crop Tool"
- Select "Delete cropped pixels"
- Select "Allow growing" and set "Fill with" to "white"
- Select an area (drag left mouse button)
- Press `enter` or click selected area
- Press `shift+i` to expand layer size to canvas size

## Copy edited image

- Press `ctrl+a`, `ctrl+c` (do not close GIMP until the image has been pasted, otherwise the image will be lost from the clipboard)

## Make speech bubble

- Press `d` to reset foreground/background colour to black/white
- Press `shift+t` to select "Text Tool"
- Click on the image where the top-left of the text should be inserted
- Set font size (EG to 30)
- Press `tab` to focus the text box
- Enter text
- Press `esc` to unfocus the text box
- Press `shift+n` to create new layer
- Drag new layer below text layer
- Press `shift+r` to select "Rectangle Select Tool"
- Draw a rectangle around the text
- Press `x` to swap foreground colour to white
- Press `shift+f` to fill in the rectangle
- Increase layer opacity to 100
- Press `shift+l` to select "Free Select Tool"
- Click 3 points to make 3 corners of a triangle, then click the first corner to close the selection
- Press `shift+f` to fill in the triangle
- Press `shift+z` to select the transparent background
- Press `x` to swap foreground colour to black
- Press `shift+s` to add a black outline to the speech bubble
- Select the top layer (containing the text)
- Press `shift+m` twice to merge all layers down

## Export as PNG

- Press `ctrl+shift+e` to export image to PNG
- Select folder and enter filename
- Press `enter` or click "Export"
- Press `enter` or click "Export" again to save with default settings
