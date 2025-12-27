// premortem-ai/pipedream/components/mitigation/index.js

module.exports = {
  name: "mitigation",
  version: "1.0.0",
  description: "Generates mitigation strategies for each scored risk in the PreMortem AI pipeline.",

  props: {
    risks: {
      type: "object",
      label: "Scored Risks Array",
      description: "Array of risks with severity scoring from the scoring step.",
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
          : r.description
    }));

    //
    // -------------------------------------
    // PROMPT CONSTRUCTION
    // -------------------------------------
    //
    const prompt = `
You are PreMortem AI. For each risk, generate a structured mitigation plan.

Each mitigation object MUST include:
- risk_id (string)
- short_term (concrete immediate actions)
- long_term (strategic mitigation solutions)
- owner (team, discipline, or role responsible for mitigating the risk)
- priority (low, medium, high) — based on severity_score

Rules:
- Priority MUST correlate with severity_score.
- Recommendations MUST be realistic and actionable.
- Output MUST be valid JSON only.
- Every risk MUST have exactly one mitigation object.

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
        { role: "system", content: "You are an AI mitigation strategy engine." },
        { role: "user", content: prompt },
      ],
      response_format: {
        type: "json_schema",
        schema: {
          type: "object",
          properties: {
            mitigations: {
              type: "array",
              items: {
                type: "object",
                properties: {
                  risk_id: { type: "string" },
                  short_term: { type: "string" },
                  long_term: { type: "string" },
                  owner: { type: "string" },
                  priority: { type: "string" }
                },
                required: ["risk_id", "short_term", "long_term", "owner", "priority"]
              }
            }
          },
          required: ["mitigations"]
        }
      }
    });

    //
    // -------------------------------------
    // RETURN OUTPUT
    // -------------------------------------
    //
    return {
      mitigations: response.mitigations
    };
  },
};
