---
name: powerbi-reporting
description: "Use when building Power BI report pages and visuals inside a .pbip file. Accepts a text brief, screenshot description, or image layout. Produces page.json and visual.json files in the correct PBIP folder structure. Handles single visuals, full pages, or complete multi-page dashboard sets."
---

# Power BI Reporting

Writes `page.json` and `visual.json` files directly into a `.pbip` report folder. Requires an active MCP connection and a valid PBIP structure from `powerbi-scaffold`.

---

## Step 1: Collect Required Inputs

Before any model discovery or file creation, confirm:

1. **Report pages** — how many pages, what is each page called, what is the purpose of each?
2. **Audience** — Executive / Management / Analyst? (drives visual density and chart types)
3. **Visuals per page** — for each page: what chart types, what business metric, what axis/category?
4. **PBIP folder path** — where is the `<Name>.Report/` folder on disk?
5. **Branding** — logo, brand colours, theme direction, or "use default"?
6. **Layout source** — text brief, image/wireframe, or "design from scratch"?

If any of these are missing, ask before proceeding.

---

## Step 2: Resolve All Fields from the Live Model

Never hardcode field or measure names. Always resolve from the connected model first.

1. `mcp__powerbi-modeling-mcp__table_operations` → `operation: "List"` — get all table names
2. `mcp__powerbi-modeling-mcp__measure_operations` → `operation: "List"` — get all measures with table names
3. `mcp__powerbi-modeling-mcp__column_operations` → `operation: "List"` — get all columns

Map user descriptions (e.g. "monthly trend", "customers impacted") to actual model field names and table names.

If a required measure does not exist:
- Create it using `mcp__powerbi-modeling-mcp__measure_operations` → `operation: "Create"` before writing any visual
- Validate it with `mcp__powerbi-modeling-mcp__dax_query_operations` → `operation: "Validate"`

---

## Step 3: Plan the Page Layout

Canvas is always **1280 × 720** (`FitToPage`) unless the user specifies otherwise.

Standard layout zones:

| Zone | x | y | width | height | Use for |
|------|---|---|-------|--------|---------|
| Full header strip | 0 | 0 | 1280 | 42 | Title / brand |
| Filter strip | 0 | 48 | 1280 | 38 | Slicers |
| KPI strip (6 cards) | 0 | 93 | 1280 | 100 | Headline numbers |
| Main chart left | 0 | 200 | 620 | 245 | Primary chart |
| Main chart right | 640 | 200 | 640 | 245 | Secondary chart |
| Bottom chart left | 0 | 455 | 630 | 255 | Trend / detail |
| Bottom chart right | 640 | 455 | 640 | 255 | Breakdown / table |
| Full-width bottom | 0 | 455 | 1280 | 255 | Wide table / matrix |

Audience density guidance:
- **Executive**: 4–8 visuals per page. Prioritise KPI cards, one trend chart, one comparison chart, one table.
- **Management**: 6–10 visuals. Add segment breakdown, funnel or heatmap.
- **Analyst**: 8–12 visuals. Add scatter, distribution charts, full detail tables.

Assign `tabOrder` in reading order: `0`, `1000`, `2000`, `3000`...

---

## Step 4: Visual Type Reference

Use **only** these built-in Power BI visual types. Never invent type names.

| User asks for | `visualType` value |
|---|---|
| Horizontal bar chart | `clusteredBarChart` |
| Vertical column chart | `clusteredColumnChart` |
| Stacked bar | `stackedBarChart` |
| Stacked column | `stackedColumnChart` |
| Line chart / trend | `lineChart` |
| Area chart | `areaChart` |
| Line and column combo | `lineClusteredColumnComboChart` |
| Pie chart | `pieChart` |
| Donut chart | `donutChart` |
| KPI / single number | `card` |
| Multi-row card | `multiRowCard` |
| Table | `tableEx` |
| Matrix / pivot | `matrix` |
| Scatter / bubble | `scatterChart` |
| Funnel | `funnel` |
| Waterfall | `waterfallChart` |
| Slicer / filter | `slicer` |
| Map | `map` |
| Filled map | `filledMap` |

> ⚠️ `barChart`, `pivotTable`, `columnChart` do NOT exist — using them will render a broken visual that prompts the user to install a custom visual.

---

## Step 5: Visual JSON Schema Rules (Critical)

### Correct visual.json structure

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
  "name": "<visualId>",
  "position": { "x": 0, "y": 0, "z": 0, "height": 245, "width": 620, "tabOrder": 0 },
  "visual": {
    "visualType": "<type>",
    "query": {
      "queryState": {
        "Category": {
          "projections": [{
            "field": { "Column": { "Expression": { "SourceRef": { "Entity": "<TableName>" } }, "Property": "<ColumnName>" } },
            "queryRef": "<TableName>.<ColumnName>"
          }]
        },
        "Y": {
          "projections": [{
            "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<TableName>" } }, "Property": "<MeasureName>" } },
            "queryRef": "<TableName>.<MeasureName>",
            "active": true
          }]
        }
      }
    },
    "visualContainerObjects": {
      "title": [{ "properties": {
        "show": { "expr": { "Literal": { "Value": "true" } } },
        "text": { "expr": { "Literal": { "Value": "'<Chart Title>'" } } }
      }}],
      "border": [{ "properties": {
        "show": { "expr": { "Literal": { "Value": "true" } } }
      }}]
    },
    "drillFilterOtherVisuals": true
  }
}
```

### Query role keys by visual type

| Visual type | Roles to use |
|---|---|
| `clusteredBarChart`, `clusteredColumnChart` | `Category` (axis), `Y` (values), optionally `Series` |
| `lineChart`, `areaChart` | `Category` (x-axis), `Y` (line values), optionally `Y2` (secondary axis), `Series` |
| `scatterChart` | `X`, `Y`, `Details`, optionally `Size` |
| `matrix` | `Rows`, `Columns`, `Values` |
| `tableEx` | `Values` (all columns as projections) |
| `card`, `multiRowCard` | `Values` |
| `slicer` | `Values` |
| `pieChart`, `donutChart` | `Category`, `Y` |

### Strictly forbidden in visual.json

| Property | Why forbidden |
|----------|--------------|
| `"filters": [...]` inside `visual` | Not defined in the schema — crashes Desktop on file open |
| Top-level `visualType`, `x`, `y`, `width`, `height` | Obsolete pre-2.7 format |
| `query.Version`, `query.From`, `query.Select` | Obsolete query format |
| Custom visual types not in Step 4 list | Requires manual install, will break report |

> ⚠️ TopN / Top N filtering cannot be expressed in visual.json. Set it manually in Power BI Desktop: Filters pane → drag field to "Filters on this visual" → Filter type: Top N.

### Table names with spaces

Wrap in single quotes in `Entity`:
```json
{ "Entity": "dim Outage" }
{ "Entity": "Outage Classifications" }
```

---

## Step 6: Create Directories and Write Files

For each page:

1. Create directory: `<Report>/definition/pages/<pageId>/`
2. Create visual directories: `<Report>/definition/pages/<pageId>/visuals/<visualId>/`
3. Write `page.json`:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
  "name": "<pageId>",
  "displayName": "<Page Display Name>",
  "displayOption": "FitToPage",
  "height": 720,
  "width": 1280
}
```

4. Write each `visual.json` using the template from Step 5.

5. Update `pages.json` — append all new page IDs to `pageOrder`, set `activePageName` to first new page.

### Page ID naming convention

Use short descriptive IDs, not random hex:
- `page001overview`
- `page002timeanalysis`
- `page003outliers`
- `page004executive`

Visual IDs follow page prefix: `p1v01`, `p1v02`, `p2v01`, etc.

---

## Step 7: Confirm and Report

After all files are written:

```
✅ Reporting Build Complete

Pages created: <N>
  📄 page001overview     → 12 visuals
  📄 page002timeanalysis → 8 visuals
  📄 page003outliers     → 9 visuals
  📄 page004executive    → 8 visuals

Total visual files: <N>
pages.json: updated ✅

ℹ️  Reload <Name>.pbip in Power BI Desktop to see the changes.
ℹ️  TopN filters on LGA/Category charts must be set manually via the Filters pane in Desktop.
```

---

## Rules

- Never hardcode field or measure names — always resolve from live model in Step 2.
- Never use `visualType` values not listed in Step 4.
- Never add `filters` or any other undocumented property inside `visual`.
- Never reuse a page ID or visual ID already present in `pages.json`.
- Always create directories before writing `visual.json` files.
- Always update `pages.json` after creating new pages.
- Always include `title` and `border` in `visualContainerObjects` on every visual.
- Always set `drillFilterOtherVisuals: true` on every visual.
- If a required measure is missing, create and validate it before building the visual.
- When a table name contains spaces, always wrap `Entity` value in quotes in the JSON.
