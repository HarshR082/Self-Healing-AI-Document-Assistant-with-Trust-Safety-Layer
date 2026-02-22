def optimize_prompt(prompt, risk=None, quality=None):
    """
    Dynamicaly strengthens prompts based on trust signals.
    """

    safety_rules = """
IMPORTANT SAFETY RULES:
- Answer ONLY if supported by context.
- Do NOT infer or assume.
- If unsure, say:
  "This information is not available in the uploaded documents."
"""

    # If hallucination risk is high → enforce strict mode
    if risk == "HIGH":
        return prompt + safety_rules + "\nBe extremely strict."

    # If quality is low → enforce evidence grounding
    if quality is not None and quality < 50:
        return prompt + safety_rules + "\nEnsure answer is directly supported."

    return prompt
