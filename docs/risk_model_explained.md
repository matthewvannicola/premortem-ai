# Risk Model Explained

PreMortem AI uses a deterministic scoring model to ensure consistent, repeatable risk evaluation.

---

## 1. Probability Levels

| Level   | Description |
|---------|-------------|
| Low     | Unlikely to occur based on current context |
| Medium  | Possible but dependent on external factors |
| High    | Likely to occur without intervention |

---

## 2. Impact Levels

| Level   | Description |
|---------|-------------|
| Low     | Minimal disruption |
| Medium  | Noticeable delay or disruption |
| High    | Significant impact on timelines, budgets, or outcomes |

---

## 3. Severity Calculation

Severity is computed using:

severity = base_mapping[probability] + base_mapping[impact] - 1

---

Where:

Low = 1
Medium = 2
High = 3

---


Severity range is **1 to 5**.

### Examples:

| Probability | Impact | Severity |
|-------------|---------|----------|
| Low         | Low     | 1 |
| Medium      | High    | 4 |
| High        | High    | 5 |

---

## 4. Recommendations Engine

Recommendations are generated using:

- Weighted LLM inference  
- Best-practice playbooks  
- Category-specific guidance  
- Past predictions (future expansion)  

---

## 5. Validation Logic

All outputs must:

- Be valid JSON  
- Use allowed enums only  
- Contain non-empty fields  
- Pass schema validation  

Invalid entries trigger:

- Auto-correction  
- Re-inference  
- Error reporting  

---

# End of Document
