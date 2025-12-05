// premortem-ai/pipedream/components/summary/index.js

module.exports = {
  name: "summary",
  version: "1.0.0",
  description: "Generates an executive summary of the project risks, themes, and mitigations.",

  props: {
    risks: {
      type: "object",
      label: "Scored Risks Array",
      description: "The full set of scored risks.",
      required: true,
    },
    themes: {
      type: "object",
      label: "Themes Array",
      description: "High-level themes extracted from the themes component.",
      required: true,
    },
    mitigations: {
      type: "object",
      label: "Mitigations Array",
      description: "Mitigation recommendations for each risk.",
      required: true,
    },
  },

  async run(context) {
    //
    // -------------------------------------
    // INPUT VALIDATION
    // -------------------------------------
    //
    const { risks, themes, mitigations } = context.props;

    if (!Array.isArray(risks) || risks.length === 0) {
      throw new Error("Input 'risks' must be a non-empty array.");
    }

    if (!Array.isArray(themes) || themes.length === 0) {
      throw new Error("Input 'themes' must be a non-empty array.");
    }

    if (!Array.isArray(mitigations) || mitigations.length === 0) {
      throw new Error("Input 'mitigations' must be a non-empty array.");
    }

    //
    // -------------------------------------
    // NORMALIZATION
    // -------------------------------------
    //
    const normalizedRisks = risks.map((r) => ({
      ...r,
      title: typeof r.title === "string" ? r.title.normalize("NFKC").trim() : r.title,
      description:
        typeof r.description === "string"
          ? r.description.normalize("NFKC").trim()
          : r.description
    }));

    const normalized = {
      risks: normalizedRisks,
      themes,
      mitigations,
    };

    //
    // -------------------------------------
    // LLM PROMPT
    // -------------------------------------
    //
    const prompt = `
You are PreMortem AI. Generate a structured executive summary of the entire risk landscape.

Your summary MUST include:
- "overview": 3–5 sentences describing the overall risk posture and situation.
- "key_themes": Array of theme names representing the main areas of concern.
- "top_risks": The 3–5 highest severity risks, each containing id, title, severity_score.
- "recommended_focus": Strategic guidance for leadership on priorities and next steps.

Rules:
- Be concise but insightful.
- Refer to patterns and strategic implications.
- Do NOT produce freeform paragraphs outside the defined summary fields.
- Output MUST be valid JSON only.

Here is the full dataset:
${JSON.stringify(normalized, null, 2)}
`;

    //
    // -------------------------------------
    // LLM EXECUTION (GPT-4.1)
    // -------------------------------------
    //
    const response = await context.$ai.run("gpt-4.1", {
      messages: [
        { role: "system", content: "You are an AI executive summary generator." },
        { role: "user", content: prompt },
      ],
      response_format: {
        type: "json_schema",
        schema: {
          type: "object",
          properties: {
            summary: {
              type: "object",
              properties: {
                overview: { type: "string" },
                key_themes: {
                  type: "array",
                  items: { type: "string" }
                },
                top_risks: {
                  type: "array",
                  items: {
                    type: "object",
                    properties: {
                      id: { type: "string" },
                      title: { type: "string" },
                      severity_score: { type: "number" },
                    },
                    required: ["id", "title", "severity_score"]
                  }
                },
                recommended_focus: { type: "string" }
              },
              required: ["overview", "key_themes", "top_risks", "recommended_focus"]
            }
          },
          required: ["summary"]
        }
      }
    });

    //
    // -------------------------------------
    // RETURN OUTPUT
    // -------------------------------------
    //
    return {
      summary: response.summary,
    };
  },
};
