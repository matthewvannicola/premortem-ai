// premortem-ai/pipedream/components/scoring/index.js

module.exports = {
  name: "scoring",
  version: "1.0.0",
  description: "Scores risk likelihood and impact to compute severity for the PreMortem AI pipeline.",

  props: {
    risks: {
      type: "object",
      label: "Risks Array",
      description: "Array of risk objects produced by the discovery step.",
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
      likelihood: typeof r.likelihood === "string" ? r.likelihood.trim().toLowerCase() : r.likelihood,
      impact: typeof r.impact === "string" ? r.impact.trim().toLowerCase() : r.impact,
    }));

    //
    // -------------------------------------
    // PROMPT CONSTRUCTION
    // -------------------------------------
    //
    const prompt = `
You are PreMortem AI. Given the following list of risks, assign numerical scoring fields
based on the following mapping:

Likelihood:
- low: 1
- medium: 2
- high: 3

Impact:
- low: 1
- medium: 2
- high: 3

Compute:
likelihood_score (number),
impact_score (number),
severity_score = likelihood_score * impact_score

Return ONLY valid JSON as an array of enriched risk objects.

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
        { role: "system", content: "You are an AI scoring engine." },
        { role: "user", content: prompt },
      ],
      response_format: {
        type: "json_schema",
        schema: {
          type: "array",
          items: {
            type: "object",
            properties: {
              id: { type: "string" },
              title: { type: "string" },
              description: { type: "string" },
              likelihood: { type: "string" },
              impact: { type: "string" },
              likelihood_score: { type: "number" },
              impact_score: { type: "number" },
              severity_score: { type: "number" }
            },
            required: [
              "id",
              "title",
              "description",
              "likelihood",
              "impact",
              "likelihood_score",
              "impact_score",
              "severity_score"
            ]
          }
        }
      }
    });

    //
    // -------------------------------------
    // RETURN OUTPUT
    // -------------------------------------
    //
    return {
      scores: response,
    };
  },
};
