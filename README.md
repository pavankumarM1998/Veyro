# Veyro - Power BI Enterprise Analytics Dashboard

This repository contains the semantic data model, report layout definitions, and visual assets for the **Veyro** enterprise analytics report.

## 🔗 Live Report Link
Explore the interactive Power BI dashboard here:
👉 **[Live Veyro Power BI Report](https://app.powerbi.com/view?r=eyJrIjoiYmY2MmVmNGEtNDY0NC00MWQxLWJkOTctYzY5MzhjNTJhNTBlIiwidCI6ImM2ZTU0OWIzLTVmNDUtNDAzMi1hYWU5LWQ0MjQ0ZGM1YjJjNCJ9)**

---

## 🛠️ Built with Claude Power BI Agent Skills
This report and its underlying semantic model were developed and styled programmatically using a set of agentic skills designed for Power BI Developer tools:

1. **`powerbi-connect` (Connection & Discovery)**:
   * Discovered the local Power BI Desktop SSAS tabular instance port and connected to the database model dynamically.
2. **`powerbi-datamodelling` (Semantic Modeling & DAX)**:
   * Built the semantic star-schema relationships.
   * Created custom business calculated columns (e.g., `Ride Status`, `Payment Method`, `Cancellation Reason`, and chronological `Month Name` sorting).
   * Programmed essential measures (Rides, Revenue, Average Fare, Ratings, Distance, Duration, and Tips).
3. **`powerbi-reporting` (Page & Visual Layout Generation)**:
   * Scaffolded a 4-tab detailed analytical interface targeting different user audiences:
     * **Executive Overview**
     * **Trips & Bookings**
     * **Driver & Vehicle Performance**
     * **Passenger & Financial Insights**
4. **`powerbi-beautify` (Advanced Styling & Dark Mode)**:
   * Configured a custom dark-mode theme directly in the base theme file (`CY26SU05.json`).
   * Applied slate card container styling with accent blue visual highlights and precise, high-readability typography defaults.
