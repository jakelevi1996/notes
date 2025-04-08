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
  - [Copy edited image](#copy-edited-image)

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

Action                    | Shortcut
---                       | ---
Tools/rectangle select    | `shift+r`
Select/stroke selection   | `shift+s`
Layers/anchor layer       | `shift+a`
Image/crop to selection   | `shift+c`
Edit/fill with FG colour  | `shift+f`

### Default shortcuts

Action                    | Shortcut
---                       | ---
Tools/bucket fill         | `shift+b`
Open keyboard shortcuts   | `alt+e`, `k`

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
- Set "Opacity" to 50.0 (25.0 might look better on dark backgrounds)
- Set "Fill Type" to "FG colour fill"
- Set "Affected Area" to "Fill whole selection"
- Set "Bucket Fill" to "Darken only" (light background) or "Lighten only" (dark background)

## Highlight an area

- Change foreground colour to yellow (HTML `ffff00`)
- Press `r` to select "Rectangle Select Tool"
- Select an area (drag left mouse button)
- Press `shift+b` to select "Bucket Fill Tool"
- Set "Bucket Fill" to "Darken only" (light background) or "Lighten only" (dark background)
- Click inside the selected area (click multiple times to effictively increase opacity)

## Outline an area

- Change foreground colour to red (HTML `ff0000`)
- Press `r` to select "Rectangle Select Tool"
- Select an area (drag left mouse button)
- Press `shift+s` to apply "Stroke Selection" (assuming custom shortcut has been set, see above)

## Highlight/outline multiple areas simultaneously

- Select an area (drag left mouse button)
- Hold `shift` and select multiple additional areas
- To highlight:
  - Press `shift+b` and click inside one of the selected areas
- To outline:
  - Press `shift+s`

## Copy edited image

- Press `ctrl+a`, `ctrl+c` (do not close GIMP until the image has been pasted, otherwise the image will be lost from the clipboard)
