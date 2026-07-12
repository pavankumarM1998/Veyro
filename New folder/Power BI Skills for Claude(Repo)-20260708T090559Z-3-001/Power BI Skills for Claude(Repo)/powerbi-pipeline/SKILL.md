---
name: powerbi-pipeline
description: "Use when running a full end-to-end Power BI PBIP development pipeline: scaffold → connect → data modelling → reporting → validation → evaluation. All stages are gated. Never skip gates. Use this when the user gives a complete brief and wants the full pipeline run from start to finish."
---

# Power BI Pipeline (End-to-End)

Runs the full PBIP development pipeline in sequence with hard gates between stages. Every stage must pass its gate before the next begins.

---

## Stage Status Table

Maintain and display this table throughout the run:

| Stage | Status |
|-------|--------|
| 0. Scaffold | Not Started |
| 1. Connect | Not Started |
| 2. Data Modelling | Not Started |
| 3. Reporting | Not Started |
| 4. Validation | Not Started |
| 5. Evaluation | Not Started |

Update status to `In Progress → Complete / Blocked` in real time.

---

## Stage 0: Scaffold

**Skill**: `powerbi-scaffold`

Actions:
- Collect project name, target folder, overwrite policy from user
- Create full PBIP folder and file structure
- Copy `CY25SU12.json` base theme from an existing project
- Write `version.json`, `report.json`, `pages.json`, `definition.pbir`, `definition.pbism`
- Create TMDL stub files (real export happens in Stage 1)

**Gate 0→1**: All required files exist and pass schema checks:
- `<Name>.pbip` ✅
- `definition.pbir` pointing to `../<Name>.SemanticModel` ✅
- `definition/version.json` with `versionMetadata/1.0.0` ✅
- `definition/report.json` with `themeCollection` + `resourcePackages`, no `name`/`displayName` ✅
- `definition/pages/pages.json` with `pagesMetadata/1.0.0` ✅
- `definition.pbism` ✅

If any file fails → fix before proceeding. Do not move to Stage 1 with broken scaffold.

---

## Stage 1: Connect

**Skill**: `powerbi-connect`

Actions:
- Ask: Local or Fabric Workspace?
- List instances / workspaces with fuzzy resolution
- Confirm selection before connecting
- Verify connection with `GetLastUsed` + `database_operations List`
- Export live model TMDL to `<Name>.SemanticModel/definition/` via `ExportToTmdlFolder`

**Gate 1→2**:
- Active connection confirmed via `GetLastUsed` ✅
- `ExportToTmdlFolder` succeeded and `expressions.tmdl` exists ✅

If export fails or `expressions.tmdl` is missing → fix before proceeding. A missing `expressions.tmdl` will cause "The import X matches no exports" on Desktop open.

---

## Stage 2: Data Modelling

**Skill**: `powerbi-datamodelling`

Actions:
- Collect business context: goal, audience, KPIs, dimensions
- Profile all tables, columns, relationships via MCP
- Run DAX profiling queries for data shape and value ranges
- Build column keep/hide plan with rationales
- Plan all DAX measures with display folders and format strings
- **Present plan to user and await explicit approval**
- Apply approved measures and column changes
- Validate every measure with `dax_query_operations Validate`
- Re-export TMDL after changes

**Gate 2→3**:
- User has explicitly approved the transformation plan ✅
- All measures validate clean (zero failures) ✅
- `ExportToTmdlFolder` run after measure creation ✅

Never proceed to reporting with unvalidated or unapproved measures.

---

## Stage 3: Reporting

**Skill**: `powerbi-reporting`

Actions:
- Confirm page count, page names, audience per page
- Confirm visuals per page (chart types, measures, dimensions)
- Confirm branding direction
- Resolve all field and measure names from live model
- Create any missing measures before building visuals
- Plan layout per page using 1280×720 grid
- Write all `page.json` and `visual.json` files
- Update `pages.json` with all new page IDs

**Gate 3→4**:
- All `page.json` files exist ✅
- All `visual.json` files exist ✅
- Every visual references only fields that exist in the live model ✅
- `pages.json` updated with all new page IDs ✅
- No `filters` property used inside any `visual` block ✅
- No invalid `visualType` values used ✅

---

## Stage 4: Validation

Actions (inline — no separate skill):

### 4A — DAX measure re-validation
Run `mcp__powerbi-modeling-mcp__dax_query_operations` with `operation: "Validate"` for every measure used in visuals.

### 4B — Schema scan
Grep all `visual.json` files for forbidden properties:
- `"filters"` inside visual block → P0: remove immediately
- Invalid `visualType` values (e.g. `barChart`, `pivotTable`) → P0: replace with correct type
- Missing `$schema` property → P0: add correct schema URI

### 4C — Field binding check
For every visual, confirm `Entity` and `Property` values exist in the live model.

### 4D — File structure check
Confirm:
- All pages in `pageOrder` have a corresponding `page.json` ✅
- All visual directories have a `visual.json` ✅
- `CY25SU12.json` exists in `StaticResources/SharedResources/BaseThemes/` ✅

**Issue severity:**

| Severity | Description | Action |
|----------|-------------|--------|
| P0 | Schema violation, invalid visual type, missing required file | Block — fix before Stage 5 |
| P1 | Missing title/border, wrong format string, unsorted axis | Fix in place, note in report |
| P2 | Cosmetic, suboptimal layout | Note for beautify pass |

**Gate 4→5**: Zero P0 issues. All P1 issues fixed or acknowledged.

---

## Stage 5: Evaluation

Actions (inline):

Assess the completed report against the original brief:

| Dimension | Questions |
|-----------|-----------|
| Business coverage | Does every stated KPI have a visual? |
| Audience fit | Does visual density match stated audience? |
| Data accuracy | Do DAX results match profiling queries from Stage 2? |
| Completeness | Are all requested pages built? |
| Reliability | Will the report open cleanly in Desktop? |

Produce a readiness decision:

| Status | Condition |
|--------|-----------|
| ✅ Ready | All gates passed, all KPIs covered, no P0/P1 issues |
| ⚠️ Ready with Conditions | Minor gaps or P2 issues, acceptable for review |
| ❌ Not Ready | Any P0 issue open, KPI coverage incomplete |

**Gate 5 output**: Status must be `Ready` or `Ready with Conditions` before handoff.

---

## Output Contract

After all stages complete, return:

```
✅ Pipeline Complete

Project     : <Name>
Location    : <TargetFolder>/<Name>.pbip

Stage Summary:
  0. Scaffold        ✅  <N> files created
  1. Connect         ✅  <model name> @ localhost:<port>
  2. Data Modelling  ✅  <N> measures created, all validated
  3. Reporting       ✅  <N> pages, <N> visuals
  4. Validation      ✅  0 P0, <N> P1 resolved
  5. Evaluation      ✅  Status: Ready

Open <Name>.pbip in Power BI Desktop to review.
Notes:
  - TopN filters on [chart names] must be set manually via Filters pane
  - Data sources require files at: <paths from expressions.tmdl>
```

---

## Hard Rules — Never Break

| Rule | Detail |
|------|--------|
| No stage skipping | Every gate must be passed in order |
| No auto-approve | User must explicitly approve data modelling plan in Stage 2 |
| No fuzzy name connect | Always confirm workspace/model with user before connecting |
| No unvalidated measures in visuals | All measures must pass `Validate` before Stage 3 |
| No P0 to evaluation | Fix all P0 schema/type issues before Stage 5 |
| No hardcoded field names | Always resolve from live model |
| No `filters` in visual.json | Property is not in schema — causes Desktop crash |
| Always export TMDL | Run `ExportToTmdlFolder` after Stage 1 and after Stage 2 |
