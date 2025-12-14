# Sample Project Description  
*Example input for the PreMortem AI Discovery Prompt*

## Project Overview
We are building a new cross-platform **Customer Insight Dashboard** for internal analytics teams.  
The system will aggregate data from multiple sources (Salesforce, HubSpot, Stripe, Snowflake, and several legacy SQL databases) and expose unified customer profiles, scoring, and trend reports.  
The MVP must support real-time data refresh, user-defined filtering, and export to PDF/Excel.

The project is expected to be used by:
- Customer Success Managers  
- Sales Operations  
- Senior Leadership  
- Support and Account Specialists  

## Goals
1. Consolidate all customer-facing data into a single internal dashboard.  
2. Provide near-real-time insights for churn prediction and upsell opportunities.  
3. Reduce manual reporting overhead across teams.  
4. Improve decision-making with automated scoring and trend detection.

## Technical Requirements
- Frontend built with **React + TypeScript**  
- Backend using **FastAPI**  
- Data sync handled via scheduled ETL jobs plus event-driven updates  
- Integration with Salesforce and Snowflake is considered critical-path  
- Authentication via the existing Okta SSO flow  
- User activity must be logged for compliance  
- PDF generation must match corporate visual standards  

## Timeline & Constraints
- Target launch: **12 weeks**  
- Only 2 dedicated backend engineers assigned  
- Data engineering resources are shared with two other initiatives  
- Salesforce and Snowflake teams operate on their own ticket queues with unpredictable turnaround times  
- Security review historically adds 1–2 weeks depending on findings  
- The design team has not finished the final UI/UX yet

## Known Challenges
- Some legacy SQL databases have inconsistent schemas  
- The Sales team frequently changes field naming conventions  
- Leadership requests last-minute reporting changes  
- Real-time ETL expectations may exceed what the data sources can reliably provide  
- No clear owner for data quality issues across departments  

## Success Criteria
- Dashboard loads < 3 seconds for 95% of queries  
- Data accuracy >= 98% across integrated systems  
- PDF export visually matches brand requirements  
- At least 3 key teams adopt the dashboard within 30 days of launch  

---

This example file is intended for testing the **Discovery Prompt**, but can also be used to validate the entire end-to-end PreMortem AI pipeline.
