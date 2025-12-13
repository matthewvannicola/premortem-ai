"""
output/markdown.py

Enterprise-grade Markdown renderer for PreMortem AI reports.

This renderer:
- Applies a fixed, governed report structure
- Expands the Detailed Risk Register deterministically
- Produces executive- and audit-ready Markdown
"""

from __future__ import annotations

from typing import List, Dict

from premortem_ai.models.pipeline_response import PipelineResponse
from premortem_ai.output.base import BaseRenderer, OutputFormat


class MarkdownRenderer(BaseRenderer):
    """
    Renders a PipelineResponse into an enterprise-grade Markdown report.
    """

    format = OutputFormat.MARKDOWN

    # ------------------------------------------------------------------
    # CANONICAL REPORT TEMPLATE (LOCKED)
    # ------------------------------------------------------------------

    REPORT_TEMPLATE = """# Project {project_name}
## {project_subtitle}

**Final Engagement Report**

Prepared For: {prepared_for}  
Prepared By: {prepared_by}  
Engagement Duration: {engagement_duration}  
Report Date: {report_date}

---

## 1. Executive Summary

{executive_summary}

---

## 2. Engagement Objectives

{engagement_objectives}

---

## 3. Scope of Work

### In-Scope
{scope_in}

### Out-of-Scope
{scope_out}

---

## 4. Delivery Approach

{delivery_approach}

---

## 5. Solution Overview

### 5.1 Architecture Summary

{architecture_summary}

---

## 6. Governance, Risk, and Compliance Controls

{governance_controls}

---

## 7. Stakeholder Engagement

{stakeholder_engagement}

---

## 8. Project Timeline & Milestones

{project_timeline}

---

## 9. Outcomes & Benefits Realized

{outcomes_and_benefits}

---

## 10. Detailed Risk Register
{risk_register}

---

## 11. Final Deliverables

{final_deliverables}

---

## 12. Recommendations & Next Steps

{recommendations}

---

## 13. Engagement Close

{engagement_close}
"""

    # ------------------------------------------------------------------
    # PUBLIC RENDER METHOD
    # ------------------------------------------------------------------

    def render(self, response: PipelineResponse) -> str:
        """
        Render the PipelineResponse into enterprise-grade Markdown.
        """

        risk_register_md = self._render_risk_register(response)

        return self.REPORT_TEMPLATE.format(
            project_name=response.project_name,
            project_subtitle=response.project_subtitle,
            prepared_for=response.prepared_for,
            prepared_by=response.prepared_by,
            engagement_duration=response.engagement_duration,
            report_date=response.report_date,
            executive_summary=response.summary.executive_summary,
            engagement_objectives=response.summary.engagement_objectives,
            scope_in=response.summary.scope_in,
            scope_out=response.summary.scope_out,
            delivery_approach=response.summary.delivery_approach,
            architecture_summary=response.summary.architecture_summary,
            governance_controls=response.summary.governance_controls,
            stakeholder_engagement=response.summary.stakeholder_engagement,
            project_timeline=response.summary.project_timeline,
            outcomes_and_benefits=response.summary.outcomes_and_benefits,
            final_deliverables=response.summary.final_deliverables,
            recommendations=response.summary.recommendations,
            engagement_close=response.summary.engagement_close,
            risk_register=risk_register_md,
        )

    # ------------------------------------------------------------------
    # RISK REGISTER RENDERING
    # ------------------------------------------------------------------

    def _render_risk_register(self, response: PipelineResponse) -> str:
        """
        Render Section 10: Detailed Risk Register.
        """

        risks = sorted(
            response.risks,
            key=lambda r: r.severity_score,
            reverse=True,
        )

        grouped: Dict[str, List] = {
            "Critical Risks (Ranks 1–10)": [],
            "High Risks (Ranks 11–50)": [],
            "Medium Risks (Ranks 51–120)": [],
            "Low Risks (Ranks 121–200)": [],
        }

        for idx, risk in enumerate(risks, start=1):
            if idx <= 10:
                grouped["Critical Risks (Ranks 1–10)"].append((idx, risk))
            elif idx <= 50:
                grouped["High Risks (Ranks 11–50)"].append((idx, risk))
            elif idx <= 120:
                grouped["Medium Risks (Ranks 51–120)"].append((idx, risk))
            else:
                grouped["Low Risks (Ranks 121–200)"].append((idx, risk))

        sections: List[str] = []

        group_index = 1
        for group_title, group_risks in grouped.items():
            if not group_risks:
                continue

            sections.append(f"\n### 10.{group_index} {group_title}\n")

            for rank, risk in group_risks:
                sections.append(self._render_single_risk(rank, risk))

            group_index += 1

        return "\n".join(sections)

    # ------------------------------------------------------------------
    # SINGLE RISK BLOCK
    # ------------------------------------------------------------------

    def _render_single_risk(self, rank: int, risk) -> str:
        """
        Render a single risk entry.
        """

        mitigations = (
            "\n".join(f"- {m.description}" for m in risk.mitigations)
            if risk.mitigations
            else "- No mitigations identified at this time."
        )

        return (
            f"#### {rank}. {risk.title}\n\n"
            f"**Description**  \n{risk.description}\n\n"
            f"**Risk Scoring**  \n"
            f"- Inherent Risk: {risk.inherent_risk}  \n"
            f"- Likelihood: {risk.likelihood}  \n"
            f"- Impact: {risk.impact}  \n"
            f"- Residual Risk: {risk.residual_risk}\n\n"
            f"**Mitigation Controls**\n"
            f"{mitigations}\n\n"
            f"**Residual Risk Commentary**  \n"
            f"{risk.residual_commentary}\n"
        )
