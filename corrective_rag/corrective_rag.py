from corrective_rag.question_rewriter import (
    rewrite_question
)


def corrective_retrieve(
    question,
    retriever
):

    documents = retriever.invoke(question)

    if documents:
        return documents, question, False

    improved_question = rewrite_question(
        question
    )

    documents = retriever.invoke(
        improved_question
    )

    return (
        documents,
        improved_question,
        True
    )