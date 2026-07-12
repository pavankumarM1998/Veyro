---
name: powerbi-beautify
description: "Use when applying visual polish to an existing PBIP report — canvas resize, brand colour palette, consistent chart formatting, container styling, typography, and background treatment. Run after powerbi-reporting to elevate raw visuals to presentation-ready quality. Can target all pages or a selected set."
---

# Power BI Beautify

Applies consistent visual polish across all pages of an existing `.pbip` report. Upgrades raw visuals to presentation-ready quality without changing any data bindings or measures.

---

## Step 1: Collect Polish Inputs

Before modifying any file, confirm:

1. **Report folder path** — where is `<Name>.Report/definition/pages/`?
2. **Pages to beautify** — All pages, or a specific subset? (list page IDs)
3. **Canvas size** — keep `1280×720` (landscape / default) or resize to `1080×1920` (portrait / mobile)?
4. **Brand colour palette** — use the default palette below, or provide custom hex codes?
5. **Background style** — `Dark` (near-black canvas) | `Light` (white/off-white) | `Brand` (primary colour wash)?
6. **Logo/image** — path to a logo PNG to embed, or skip?

If inputs are not provided, use the defaults defined in Step 2.

---

## Step 2: Default Brand & Style Specifications

### 2A — Colour Palette (Default)

| Role | Hex | Use for |
|------|-----|---------|
| Primary | `#1A73E8` | Main bar/column charts, key line |
| Secondary | `#34A853` | Comparison series, positive indicators |
| Accent 1 | `#FBBC04` | Highlights, warning KPIs |
| Accent 2 | `#EA4335` | Negative indicators, outliers |
| Neutral Dark | `#202124` | Canvas background (dark mode) |
| Neutral Mid | `#3C4043` | Card backgrounds, header bar |
| Neutral Light | `#F8F9FA` | Canvas background (light mode) |
| Text Primary | `#FFFFFF` | Labels on dark backgrounds |
| Text Secondary | `#9AA0A6` | Axis labels, subtitles |
| Border | `#5F6368` | Visual borders |

### 2B — Canvas Sizes

| Mode | Width | Height | `displayOption` |
|------|-------|--------|-----------------|
| Landscape (default) | 1280 | 720 | `FitToPage` |
| Portrait (mobile) | 1080 | 1920 | `FitToPage` |
| Custom | user-defined | user-defined | `FitToPage` |

### 2C — Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Page title | Segoe UI | 18px | Bold |
| Section header | Segoe UI | 13px | Semibold |
| Visual title | Segoe UI | 11px | Semibold |
| Axis labels | Segoe UI | 9px | Regular |
| KPI value | DIN / Segoe UI | 28px | Bold |
| KPI label | Segoe UI | 10px | Regular |

### 2D — Visual Container Defaults

Every visual should have:
```json
"visualContainerObjects": {
  "title": [{ "properties": {
    "show":       { "expr": { "Literal": { "Value": "true" } } },
    "text":       { "expr": { "Literal": { "Value": "'<Chart Title>'" } } },
    "fontColor":  { "expr": { "Literal": { "Value": "'#FFFFFF'" } } },
    "fontSize":   { "expr": { "Literal": { "Value": "11" } } },
    "fontFamily": { "expr": { "Literal": { "Value": "'Segoe UI'" } } },
    "bold":       { "expr": { "Literal": { "Value": "true" } } }
  }}],
  "border": [{ "properties": {
    "show":  { "expr": { "Literal": { "Value": "true" } } },
    "color": { "expr": { "Literal": { "Value": "'#5F6368'" } } }
  }}],
  "background": [{ "properties": {
    "show":         { "expr": { "Literal": { "Value": "true" } } },
    "color":        { "expr": { "Literal": { "Value": "'#3C4043'" } } },
    "transparency": { "expr": { "Literal": { "Value": "0" } } }
  }}]
}
```

### 2E — KPI Card Style

```json
"visualContainerObjects": {
  "title": [{ "properties": {
    "show": { "expr": { "Literal": { "Value": "false" } } }
  }}],
  "background": [{ "properties": {
    "show":         { "expr": { "Literal": { "Value": "true" } } },
    "color":        { "expr": { "Literal": { "Value": "'#1A73E8'" } } },
    "transparency": { "expr": { "Literal": { "Value": "15" } } }
  }}],
  "border": [{ "properties": {
    "show":  { "expr": { "Literal": { "Value": "true" } } },
    "color": { "expr": { "Literal": { "Value": "'#1A73E8'" } } }
  }}]
}
```

### 2F — Header / Title Bar Shape (if using a title visual)

Use a `textbox` visual spanning full page width (y=0, height=42):
```json
"visual": {
  "visualType": "textbox",
  "objects": {
    "general": [{ "properties": {
      "paragraphs": [{ "textRuns": [{
        "value": "<Report Title>",
        "textRunStyle": {
          "fontFamily": "Segoe UI",
          "fontSize": "18",
          "bold": true,
          "color": { "solid": { "color": "#FFFFFF" } }
        }
      }],
      "horizontalTextAlignment": "Left"
      }]
    }}]
  },
  "visualContainerObjects": {
    "background": [{ "properties": {
      "show":  { "expr": { "Literal": { "Value": "true" } } },
      "color": { "expr": { "Literal": { "Value": "'#1A73E8'" } } }
    }}],
    "border": [{ "properties": {
      "show": { "expr": { "Literal": { "Value": "false" } } }
    }}]
  }
}
```

---

## Step 3: Resize Canvas (if requested)

For each target page, update `page.json`:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
  "name": "<pageId>",
  "displayName": "<Page Display Name>",
  "displayOption": "FitToPage",
  "height": 1920,
  "width": 1080
}
```

> ⚠️ If resizing from 1280×720 to 1080×1920, all existing visual positions will need recalculating. Reflow visuals to portrait zones — see Step 4.

### Portrait layout zones (1080×1920)

| Zone | x | y | width | height | Use for |
|------|---|---|-------|--------|---------|
| Header | 0 | 0 | 1080 | 60 | Title bar |
| KPI row 1 | 0 | 70 | 1080 | 130 | Top 3 KPI cards |
| KPI row 2 | 0 | 210 | 1080 | 130 | Next 3 KPI cards |
| Main chart | 0 | 355 | 1080 | 380 | Full-width primary |
| Chart 2 | 0 | 750 | 1080 | 380 | Full-width secondary |
| Chart 3 | 0 | 1145 | 1080 | 380 | Full-width tertiary |
| Table / detail | 0 | 1540 | 1080 | 360 | Detail table |

---

## Step 4: Apply Colour Theme to `report.json`

Update `<Name>.Report/definition/report.json` to embed a custom data colour sequence:

```json
"objects": {
  "dataColors": [{
    "properties": {
      "dataColor1":  { "expr": { "Literal": { "Value": "'#1A73E8'" } } },
      "dataColor2":  { "expr": { "Literal": { "Value": "'#34A853'" } } },
      "dataColor3":  { "expr": { "Literal": { "Value": "'#FBBC04'" } } },
      "dataColor4":  { "expr": { "Literal": { "Value": "'#EA4335'" } } },
      "dataColor5":  { "expr": { "Literal": { "Value": "'#4285F4'" } } },
      "dataColor6":  { "expr": { "Literal": { "Value": "'#0F9D58'" } } },
      "dataColor7":  { "expr": { "Literal": { "Value": "'#F4B400'" } } },
      "dataColor8":  { "expr": { "Literal": { "Value": "'#DB4437'" } } }
    }
  }],
  "page": [{
    "properties": {
      "background": { "expr": { "Literal": { "Value": "'#202124'" } } }
    }
  }]
}
```

---

## Step 5: Apply Visual-Level Styling

For each `visual.json` in the target pages:

1. **Detect visual type** from `visual.visualType`
2. **Apply matching container style**:
   - `card` / `multiRowCard` → KPI Card style (Step 2E)
   - `slicer` → minimal border, no background
   - `textbox` → header bar style if in header zone
   - All others → standard container style (Step 2D)
3. **Update title font colour** to `#FFFFFF`
4. **Ensure border is enabled** with colour `#5F6368`
5. **Ensure `drillFilterOtherVisuals: true`** is set

Do NOT modify:
- `visual.query` (data bindings)
- `visual.visualType`
- `position.x`, `position.y`, `position.width`, `position.height` (unless resizing canvas)

---

## Step 6: Slicer Styling

For each `slicer` visual:

```json
"visualContainerObjects": {
  "title": [{ "properties": {
    "show":       { "expr": { "Literal": { "Value": "true" } } },
    "fontColor":  { "expr": { "Literal": { "Value": "'#9AA0A6'" } } },
    "fontSize":   { "expr": { "Literal": { "Value": "10" } } }
  }}],
  "background": [{ "properties": {
    "show":         { "expr": { "Literal": { "Value": "true" } } },
    "color":        { "expr": { "Literal": { "Value": "'#3C4043'" } } },
    "transparency": { "expr": { "Literal": { "Value": "0" } } }
  }}],
  "border": [{ "properties": {
    "show":  { "expr": { "Literal": { "Value": "true" } } },
    "color": { "expr": { "Literal": { "Value": "'#5F6368'" } } }
  }}]
}
```

---

## Step 7: Verify and Report

After all files are updated:

```
✅ Beautify Complete

Pages updated : <N>
  📄 page001overview     → <N> visuals styled
  📄 page002timeanalysis → <N> visuals styled
  📄 page003outliers     → <N> visuals styled
  📄 page004executive    → <N> visuals styled

Canvas size   : <W>×<H> (landscape / portrait)
Colour palette: Default Google-inspired | Custom
report.json   : dataColors updated ✅

ℹ️  Reload <Name>.pbip in Power BI Desktop to see changes.
ℹ️  Some formatting (axis colours, data label colours) may need fine-tuning in Desktop Format pane.
```

---

## Rules

- Never modify data bindings (`query`, `queryState`, projections) — only modify `visualContainerObjects` and `position`.
- Never change `visualType`.
- Never remove existing `title` text — only update its style properties.
- Always preserve `drillFilterOtherVisuals: true`.
- If canvas is resized, recalculate ALL visual positions for the new canvas size.
- If custom hex codes are provided, replace default palette values but keep the same structural JSON.
- Always update `report.json` with the colour palette when running a full beautify pass.
- Do not add the `filters` property anywhere in `visual.json` — even during styling.
