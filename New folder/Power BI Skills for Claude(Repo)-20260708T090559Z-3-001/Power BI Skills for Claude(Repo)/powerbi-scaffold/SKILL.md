---
name: powerbi-scaffold
description: "Use when creating a new blank Power BI .pbip project with default settings and folder structure. Run this first for any new project before connect, data modelling, reporting, or pipeline."
---

# Power BI PBIP Scaffold

Creates the complete PBIP folder and file scaffold. Run this once per new project.

---

## Step 1: Collect Inputs

Ask for:
- **Project base name** (e.g. `Executive_Outage_Report`)
- **Target folder path** (absolute path where project should be created)
- **Overwrite policy**: `1. Stop if exists` | `2. Reuse existing if compatible`

If the target folder already exists and policy is `Stop if exists`, halt and ask for a new name.

---

## Step 2: Resolve All Project Paths

From `<Name>` and `<TargetFolder>` derive:

| Artifact | Path |
|----------|------|
| PBIP launcher | `<TargetFolder>/<Name>.pbip` |
| Report folder | `<TargetFolder>/<Name>.Report/` |
| Report definition | `<TargetFolder>/<Name>.Report/definition.pbir` |
| Semantic model folder | `<TargetFolder>/<Name>.SemanticModel/` |
| Semantic model definition | `<TargetFolder>/<Name>.SemanticModel/definition.pbism` |

---

## Step 3: Create `<Name>.pbip`

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
  "version": "1.0",
  "artifacts": [{ "report": { "path": "<Name>.Report" } }],
  "settings": { "enableAutoRecovery": true }
}
```

---

## Step 4: Create `<Name>.Report/definition.pbir`

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
  "version": "4.0",
  "datasetReference": {
    "byPath": { "path": "../<Name>.SemanticModel" }
  }
}
```

---

## Step 5: Create Report Metadata Files (ALL REQUIRED — missing any one will crash Desktop on open)

### 5A — `<Name>.Report/definition/version.json`
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
  "version": "2.0.0"
}
```

### 5B — `<Name>.Report/definition/report.json`
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.2.0/schema.json",
  "themeCollection": {
    "baseTheme": {
      "name": "CY25SU12",
      "reportVersionAtImport": { "visual": "2.5.0", "report": "3.1.0", "page": "2.3.0" },
      "type": "SharedResources"
    }
  },
  "objects": {
    "section": [{ "properties": { "verticalAlignment": { "expr": { "Literal": { "Value": "'Top'" } } } } }],
    "outspacePane": [{ "properties": { "expanded": { "expr": { "Literal": { "Value": "false" } } } } }]
  },
  "resourcePackages": [{
    "name": "SharedResources",
    "type": "SharedResources",
    "items": [{ "name": "CY25SU12", "path": "BaseThemes/CY25SU12.json", "type": "BaseTheme" }]
  }],
  "settings": {
    "useStylableVisualContainerHeader": true,
    "exportDataMode": "AllowSummarized",
    "defaultDrillFilterOtherVisuals": true,
    "allowChangeFilterTypes": true,
    "useEnhancedTooltips": true,
    "useDefaultAggregateDisplayName": true
  }
}
```

> ⚠️ NEVER add `name`, `displayName`, or `description` at the top level of `report.json` — the schema forbids them and Desktop will refuse to open.

### 5C — `<Name>.Report/definition/pages/pages.json`
```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
  "pageOrder": [],
  "activePageName": null
}
```

> ⚠️ NEVER add a top-level `pages` array here — it is not in the schema.

### 5D — `<Name>.Report/StaticResources/SharedResources/BaseThemes/CY25SU12.json`
Source from any existing local PBIP project. Search with:
```
Glob("**/BaseThemes/CY25SU12.json")
```
Copy the file verbatim. If no source exists, write a minimal placeholder:
```json
{ "name": "CY25SU12", "dataColors": [], "visualStyles": {} }
```

---

## Step 6: Create `<Name>.SemanticModel/definition.pbism`

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
  "version": "4.2",
  "settings": {}
}
```

---

## Step 7: Populate Semantic Model TMDL

**Preferred path — live connection already exists:**
Use `mcp__powerbi-modeling-mcp__database_operations` with `operation: "ExportToTmdlFolder"` and `tmdlFolderPath` pointing to `<Name>.SemanticModel/definition/`.

This exports the real model including all tables, measures, relationships, and — critically — the `expressions.tmdl` file containing all shared Power Query named queries. Without this file, any partition that calls `Table.Combine` or references named queries will fail with "The import X matches no exports".

**Fallback path — no live connection:**
Create minimal stub TMDL files:

`definition/database.tmdl`
```tmdl
database
  compatibilityLevel: 1600
```

`definition/model.tmdl`
```tmdl
model Model
  culture: en-US
  defaultPowerBIDataSourceVersion: powerBI_V3
```

`definition/relationships.tmdl`
```tmdl
```

`definition/cultures/en-US.tmdl`
```tmdl
cultureInfo en-US
```

Create empty `definition/tables/` directory.

> ⚠️ All `.tmdl` files must use valid TMDL syntax. Never write JSON objects or `{ }` placeholder blocks inside a `.tmdl` file — Power BI will fail to load the model.

---

## Step 8: Verification Checklist

Run through every item before marking scaffold complete:

| Check | Expected |
|-------|----------|
| `<Name>.pbip` exists | ✅ with `$schema` and correct report path |
| `definition.pbir` exists | ✅ points to `../<Name>.SemanticModel` |
| `definition/version.json` | ✅ schema `versionMetadata/1.0.0`, version `2.0.0` |
| `definition/report.json` | ✅ has `themeCollection` + `resourcePackages`, no `name`/`displayName` |
| `definition/pages/pages.json` | ✅ schema `pagesMetadata/1.0.0`, has `pageOrder`, no `pages` array |
| `StaticResources/.../CY25SU12.json` | ✅ exists and is valid JSON |
| `definition.pbism` | ✅ schema `semanticModel/definitionProperties/1.0.0` |
| TMDL files | ✅ valid TMDL syntax or full live export |

### Auto-remediation table

| Error seen in Desktop | Fix |
|---|---|
| `Property 'name' has not been defined` in `report.json` | Remove `name`/`displayName`/`description`, ensure `themeCollection` present |
| `Can't find '$schema' in pages/pages.json` | Rewrite with `pagesMetadata/1.0.0` schema, add `pageOrder`, remove `pages` array |
| `TMDL Format Error ... Line '{'` | Replace stub TMDL with valid syntax or run `ExportToTmdlFolder` |
| `The import X matches no exports` | Run `ExportToTmdlFolder` from live model — `expressions.tmdl` is missing |

---

## Step 9: Handoff

Return:
- All created file paths
- Scaffold status: ✅ Complete / ⚠️ Needs attention
- Next step: run `powerbi-connect`
