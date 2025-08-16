
# Power BI Dashboard Guide

1) Get Data → Text/CSV → `outputs/predictions_for_dashboard.csv`
2) View → Themes → Browse → `PowerBI/theme.json`
3) Add visuals:
   - KPIs: Total Customers, Churned Customers, Churn Rate, High Risk Customers
   - Donut: risk_segment
   - Clustered Column: Geography_Spain, Geography_Germany (baseline = France)
   - Table: CustomerId, Age, CreditScore, Balance, churn_probability, risk_segment
4) Slicers: risk_segment, Gender_Male, Geography_*
