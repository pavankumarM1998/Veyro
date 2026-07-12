---
name: powerbi-datamodelling
description: "Use when profiling a connected Power BI semantic model, creating DAX measures, planning and applying column transformations, and persisting all changes to TMDL source files. Requires an active connection. Run after powerbi-connect and before powerbi-reporting."
---

# Power BI Data Modelling

Profiles the live model, creates DAX measures, and persists everything to TMDL. Requires an active MCP connection.

---

## Step 1: Collect Business Context (Mandatory)

Before touching the model, ask:
- **Dashboard goal**: What business question does this report answer?
- **Audience**: Executive / Management / Analyst / Mixed?
- **Key KPIs**: What numbers must appear as headline metrics?
- **Dimensions needed**: What filters/slicers are required (date, region, category, etc.)?
- **Must-have columns**: Any specific fields the stakeholder explicitly requires?
- **Must-avoid columns**: Any sensitive, technical, or irrelevant columns to hide?

Do not proceed until goal and audience are clearly stated.

---

## Step 2: Profile the Connected Model

Run all of the following in parallel:

1. `mcp__powerbi-modeling-mcp__table_operations` → `operation: "List"` — get all tables with column counts
2. `mcp__powerbi-modeling-mcp__table_operations` → `operation: "GetSchema"` for each table — get column names, data types, summarizeBy
3. `mcp__powerbi-modeling-mcp__measure_operations` → `operation: "List"` — get existing measures and display folders
4. `mcp__powerbi-modeling-mcp__relationship_operations` → `operation: "List"` — identify fact/dimension relationships and active/inactive

From results, identify:
- **Fact table(s)**: largest row count, numeric columns, has foreign keys
- **Dimension tables**: categorical, used as slicer axes
- **Date table**: contains Year, Month, Day Name, Quarter columns
- **Measure table(s)**: contains only measures, no data columns

---

## Step 3: Data Profiling with DAX

Run DAX queries to understand actual data shape. Use `mcp__powerbi-modeling-mcp__dax_query_operations` with `operation: "Execute"`.

Always profile:
- Row count and date range: `EVALUATE ROW("Rows", COUNTROWS('<FactTable>'), "Min Date", MIN('<FactTable>'[<DateCol>]), "Max Date", MAX('<FactTable>'[<DateCol>]))`
- Key measure totals: `EVALUATE ROW("Total <KPI>", SUM('<Table>'[<Column>]), "Avg <KPI>", AVERAGE('<Table>'[<Column>]))`
- Top categorical breakdowns (top 5 by count): `EVALUATE TOPN(5, SUMMARIZECOLUMNS('<Table>'[<CategoryCol>], "Count", COUNTROWS('<Table>')), [Count], DESC)`

Use these results to:
- Confirm the most analytically valuable columns
- Identify any obviously missing measures
- Spot data quality issues (nulls, extreme outliers)

---

## Step 4: Build Column Prioritization Plan

Using business context (Step 1) and profile results (Steps 2–3), produce a plan by table:

**Keep (dashboard-ready):**
- Columns directly answering the KPIs or enabling required slicers
- Columns with clear business names and populated values

**Deprioritize / Hide:**
- System/technical columns (row numbers, internal IDs, sort helper columns)
- Columns with no analytical use for stated audience
- Duplicate or derived columns already covered by measures

Include a one-line rationale per group.

---

## Step 5: Plan DAX Measures

Based on business context and data profile, plan the measures to create. Group them into display folders:

| Folder | Measure types |
|--------|--------------|
| `KPIs` | Core count, sum, average, max measures |
| `Time Intelligence` | MoM change %, cumulative totals, YTD |
| `Outlier Analysis` | Percentiles (Q1, Median, Q3, P90), IQR, upper/lower fence |
| `Executive` | Composite scores, ratios, high-impact flags |

For each measure, specify:
- Name
- DAX expression (using real column references resolved in Step 2)
- Format string (`#,0`, `0.0%`, `#,0.0`, etc.)
- Display folder

---

## Step 6: Get Approval Before Applying

Present to user:
1. Column keep/hide plan with rationales
2. Measures to create with DAX expressions
3. Any rename or format changes

State clearly:
> "No model changes will be made until you approve this plan. Reply **approve** to proceed or provide changes."

Do not create measures or modify columns until approved.

---

## Step 7: Apply Approved Changes

### 7A — Create Measures
Use `mcp__powerbi-modeling-mcp__measure_operations` with `operation: "Create"`.
- Submit in batches by display folder
- Use `options: { continueOnError: true }` so one failure does not block the rest
- Always specify `formatString` and `displayFolder`

### 7B — Column Visibility / Formatting
Use `mcp__powerbi-modeling-mcp__column_operations` with `operation: "Update"` for:
- `isHidden: true` on deprioritized columns
- `formatString` corrections
- `dataCategory` assignments (Country, StateOrProvince, Place)
- `sortByColumn` for sort-order columns (e.g. Month Name sorted by Month number)

---

## Step 8: Validate All Measures

For every measure created, run `mcp__powerbi-modeling-mcp__dax_query_operations` with `operation: "Validate"`.

Batch into groups of 6–8 measures per `ROW()` call:
```
EVALUATE ROW("Measure1", [Measure1], "Measure2", [Measure2], ...)
```

If any measure fails validation:
- Show the exact error
- Fix the DAX expression
- Re-validate before continuing

Do not proceed to reporting with any invalid measure.

---

## Step 9: Persist to TMDL

Export the updated model to the PBIP SemanticModel folder:

`mcp__powerbi-modeling-mcp__database_operations` → `operation: "ExportToTmdlFolder"`, `tmdlFolderPath: "<Name>.SemanticModel/definition/"`

This persists all measures, column changes, and relationships so they survive project reopen.

Verify the export created/updated:
- `definition/tables/<TableName>.tmdl` — contains measure definitions
- `definition/expressions.tmdl` — contains shared Power Query named queries (critical for partition references)
- `definition/relationships.tmdl`

---

## Step 10: Return Summary

```
✅ Data Modelling Complete
  Tables profiled     : <N>
  Measures created    : <N> across <N> display folders
  Columns hidden      : <N>
  Format/sort fixes   : <N>
  Validation          : All measures valid ✅
  TMDL export         : ✅ <N> files written

Measure folders:
  KPIs               : <list>
  Time Intelligence  : <list>
  Outlier Analysis   : <list>
  Executive          : <list>
```

---

## Rules

- Never modify the model before user approves the plan in Step 6.
- Never skip DAX validation in Step 8 — invalid measures will silently break visuals.
- Always run `ExportToTmdlFolder` after applying changes — in-memory model changes are lost on Desktop reopen without this.
- Never reference column or measure names from memory — always resolve from live model in Step 2.
- If a measure's DAX references a column that does not exist, fix the column reference before creating the measure.
- Always include `displayFolder` and `formatString` on every measure — no naked measures.
