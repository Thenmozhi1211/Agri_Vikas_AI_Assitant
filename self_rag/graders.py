from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from config.settings import LLM_MODEL


llm = ChatOpenAI(
    model=LLM_MODEL,
    temperature=0
)


def grade_document_relevance(question, document):

    prompt = ChatPromptTemplate.from_template(
        """
You are a document relevance grader.

Determine whether the following document
contains information useful for answering
the user's question.

Question:
{question}

Document:
{document}

Return ONLY one of:

YES

or

NO
"""
    )

    chain = prompt | llm

    result = chain.invoke(
        {
            "question": question,
            "document": document
        }
    )

    response = result.content.strip().upper()

    return response.startswith("YES")


def grade_answer_groundedness(
    question,
    context,
    answer
):

    prompt = ChatPromptTemplate.from_template(
        """
You are an answer groundedness grader.

Determine whether the answer is supported
by the supplied context.

Question:
{question}

Context:
{context}

Answer:
{answer}

Return ONLY:

YES

or

NO
"""
    )

    chain = prompt | llm

    result = chain.invoke(
        {
            "question": question,
            "context": context,
            "answer": answer
        }
    )

    response = result.content.strip().upper()

    return response.startswith("YES")