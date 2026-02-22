def quality_score(answer, context):

    length_score = min(len(answer) / 300, 1)

    keyword_overlap = sum(
        1 for word in answer.split()
        if word.lower() in context.lower()
    )

    relevance_score = min(keyword_overlap / 20, 1)

    final_score = (length_score * 0.4) + (relevance_score * 0.6)

    return round(final_score * 100, 2)
