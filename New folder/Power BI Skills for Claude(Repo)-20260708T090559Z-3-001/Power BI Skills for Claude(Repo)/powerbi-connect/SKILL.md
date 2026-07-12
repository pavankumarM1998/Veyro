---
name: powerbi-connect
description: "Use when connecting to a Power BI semantic model — either a running local Power BI Desktop instance or a Fabric workspace model. Handles fuzzy name matching with mandatory user confirmation. Always run after powerbi-scaffold and before powerbi-datamodelling."
---

# Power BI Connect

Establishes and confirms an active connection to a semantic model. Run after scaffold, before data modelling.

---

## Step 1: Ask Connection Source

Present the user with:
```
Where is your semantic model?
  1. Local (Power BI Desktop running on this machine)
  2. Fabric Workspace (cloud)
```

Accept only `1` or `2`. Re-prompt on invalid input.

---

## Step 2A: Local Connection

1. Call `mcp__powerbi-modeling-mcp__connection_operations` with `operation: "ListLocalInstances"`.

2. **If zero instances found:**
   - State clearly: "No Power BI Desktop instances are currently running."
   - Ask user to open their `.pbix` or `.pbip` file in Power BI Desktop and retry.
   - Stop.

3. **If exactly one instance found:**
   - Show its details: port, window title, start time.
   - Auto-connect using `operation: "Connect"` with the returned `connectionString`.

4. **If multiple instances found:**
   - Display them as a numbered list (show window title and port for each).
   - Ask user to pick a number.
   - Connect to the selected instance.

5. Confirm the connection with `operation: "GetLastUsed"`.

6. Call `mcp__powerbi-modeling-mcp__database_operations` with `operation: "List"` to retrieve the active database name and ID.

7. Return: connection name, server, port, database name, database ID.

---

## Step 2B: Fabric Workspace Connection

1. Authenticate with Power BI / Fabric. If not signed in, prompt user to sign in before proceeding.

2. After authentication, fetch all accessible workspaces from the signed-in user's profile context.
   - Never derive workspace list from prior sessions or cached names.

3. Display workspaces as a numbered list.

4. Ask: "Enter a workspace number or name."

5. **Fuzzy workspace resolution:**
   - Number input → map directly from list.
   - Name input → search all workspace names using case-insensitive substring match, then edit-distance match for typos.
   - If one clear match: show it and ask for confirmation ("Did you mean **X**? y/n").
   - If multiple probable matches: show as numbered list, ask user to pick.
   - If no match: state clearly, ask user to re-enter.
   - Never auto-select when multiple candidates exist.

6. After workspace confirmed, fetch all semantic models in that workspace.

7. Display models as a numbered list.

8. Ask: "Enter a model number or name."

9. Apply the same fuzzy resolution as step 5 for model name.

10. Only after both workspace and model are confirmed, connect using:
    - `mcp__powerbi-modeling-mcp__connection_operations`
    - `operation: "ConnectFabric"`
    - `workspaceName`: exact resolved name
    - `semanticModelName`: exact resolved name

11. Confirm with `operation: "GetLastUsed"` and `database_operations List`.

---

## Step 3: Post-Connection Export (Recommended)

After a successful connection, if a PBIP SemanticModel folder exists for this project:

Ask: "Do you want to sync the live model into the PBIP SemanticModel folder now? This ensures all tables, measures, relationships, and Power Query expressions are persisted correctly."

If yes → call `mcp__powerbi-modeling-mcp__database_operations` with:
- `operation: "ExportToTmdlFolder"`
- `tmdlFolderPath`: `<ProjectName>.SemanticModel/definition/`

This is the most reliable way to prevent "The import X matches no exports" errors when opening the PBIP in Desktop.

---

## Output Format

Always return:
```
✅ Connected
  Source       : Local | Fabric
  Connection   : <connection name>
  Server       : <server:port>
  Database     : <database name> (<database id>)
  Workspace    : <name> (Fabric only)
  TMDL Export  : Done | Skipped
```

---

## Rules

- Never call `ConnectFabric` with a user-typed name directly — always resolve to confirmed exact name first.
- Never skip confirmation when multiple fuzzy candidates match.
- Never proceed to data modelling if connection has not been confirmed via `GetLastUsed`.
- If connection fails, show the error message clearly and suggest corrective actions.
- Always retrieve the database list after connecting — the database ID is needed for export and deployment steps.
