def heal_response(answer, risk, quality, unsupported):
    """
    Improvers system reliability by preventing unsafe responses.
    """

    # HIGH hallucination risk → block answer
    if risk == "HIGH":
        return (
            "The available documents do not contain reliable "
            "information to answer this question."
        )

    # LOW quality → insufficient evidence
    if quality < 40:
        return (
            "The retrieved information is insufficient to provide "
            "a confident answer."
        )

    # If many unsupported sentences → soften response
    if len(unsupported) >= 2:
        return (
            answer +
            "\n\n⚠ Some parts of this response may not be fully supported "
            "by the document."
        )

    return answer
