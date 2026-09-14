from self_rag.graders import grade_document_relevance


def filter_relevant_documents(question, documents):
    """
    Filter retrieved documents using the Self-RAG
    relevance grader.

    Parameters:
        question: User's question
        documents: Documents returned by the retriever

    Returns:
        List of relevant documents
    """

    relevant_documents = []

    for document in documents:

        try:
            is_relevant = grade_document_relevance(
                question,
                document.page_content
            )

            if is_relevant:
                relevant_documents.append(document)

        except Exception as e:

            print(
                f"Error grading document: {e}"
            )

    return relevant_documents