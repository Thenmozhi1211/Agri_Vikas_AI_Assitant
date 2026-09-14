from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from config.settings import LLM_MODEL


llm = ChatOpenAI(
    model=LLM_MODEL,
    temperature=0
)


def rewrite_question(question):

    prompt = ChatPromptTemplate.from_template(
        """
Rewrite the user's question into a better search query
for an agriculture knowledge base.

Keep the meaning unchanged.

Original question:
{question}

Return only the improved search query.
"""
    )

    chain = prompt | llm

    result = chain.invoke({
        "question": question
    })

    return result.content.strip()