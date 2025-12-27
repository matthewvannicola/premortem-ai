// premortem-ai/pipedream/components/themes/index.js

module.exports = {
  name: "themes",
  version: "1.0.0",
  description: "Clusters risks into thematic groups for the PreMortem AI pipeline.",

  props: {
    risks: {
      type: "object",
      label: "Scored Risks Array",
      description: "Array of scored risk objects from the scoring step.",
      required: true,
    },
  },

  async run(context) {
    //
    // -------------------------------------
    // INPUT VALIDATION
    // -------------------------------------
    //
    const risks = context.props.risks;

    if (!Array.isArray(risks) || risks.length === 0) {
      throw new Error("Input 'risks' must be a non-empty array.");
    }

    //
    // -------------------------------------
    // NORMALIZATION
    // -------------------------------------
    //
    const normalized = risks.map((r) => ({
      ...r,
      title: typeof r.title === "string" ? r.title.normalize("NFKC").trim() : r.title,
      description:
        typeof r.description === "string"
          ? r.description.normalize("NFKC").trim()
          : r.description,
    }));

    //
    // -------------------------------------
    // PROMPT CONSTRUCTION
    // -------------------------------------
    //
    const prompt = `
You are PreMortem AI. Cluster the following risks into high-level themes.
A theme represents a repeating pattern, root cause category, or strategic area of concern.

Each theme must include:
- theme_id (string, like "theme-001")
- name (short human-readable title)
- summary (2–3 sentences explaining the pattern)
- risk_ids (array of risk.id values belonging to that theme)

Rules:
- Every risk MUST belong to at least one theme.
- Themes MUST be non-overlapping in explanation.
- Return ONLY valid JSON.

Risks:
${JSON.stringify(normalized, null, 2)}
`;

    //
    // -------------------------------------
    // LLM EXECUTION (GPT-4.1)
    // -------------------------------------
    //
    const response = await context.$ai.run("gpt-4.1", {
      messages: [
        { role: "system", content: "You are an AI risk-clustering and theme-analysis engine." },
        { role: "user", content: prompt },
      ],
      response_format: {
        type: "json_schema",
        schema: {
          type: "object",
          properties: {
            themes: {
              type: "array",
              items: {
                type: "object",
                properties: {
                  theme_id: { type: "string" },
                  name: { type: "string" },
                  summary: { type: "string" },
                  risk_ids: {
                    type: "array",
                    items: { type: "string" },
                  },
                },
                required: ["theme_id", "name", "summary", "risk_ids"],
              },
            },
          },
          required: ["themes"],
        },
      },
    });

    //
    // -------------------------------------
    // RETURN OUTPUT
    // -------------------------------------
    //
    return {
      themes: response.themes,
    };
  },
};
