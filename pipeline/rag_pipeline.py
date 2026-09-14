from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from retrieval.retriever import get_retriever

from self_rag.self_rag import (
    filter_relevant_documents
)

from self_rag.graders import (
    grade_answer_groundedness
)

from corrective_rag.corrective_rag import (
    corrective_retrieve
)

from config.settings import LLM_MODEL


class AgricultureRAGPipeline:

    def __init__(self):

        print("Initializing Agriculture RAG Pipeline...")

        # Load FAISS retriever
        self.retriever = get_retriever()

        # OpenAI LLM
        self.llm = ChatOpenAI(
            model=LLM_MODEL,
            temperature=0
        )

        print("Agriculture RAG Pipeline initialized.")


    def generate_answer(
        self,
        question,
        documents
    ):

        # Combine retrieved documents
        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        prompt = ChatPromptTemplate.from_template(
            """
You are an agriculture information assistant.

Answer the user's question using ONLY the
information provided in the context.

Important rules:

1. Do not invent information.
2. Do not invent government schemes.
3. Do not invent subsidy amounts.
4. Do not invent eligibility rules.
5. Do not invent dates.
6. If the information is not available,
   clearly say that it is not available in
   the current Agrisnet knowledge base.

Give the answer in simple language.

Question:
{question}

Context:
{context}

Answer:
"""
        )

        chain = prompt | self.llm

        result = chain.invoke(
            {
                "question": question,
                "context": context
            }
        )

        return result.content, context


    def ask(self, question):

        status = {
            "guardrails": "PASS",
            "retrieval": "STARTED",
            "self_rag": "STARTED",
            "corrective_rag": "NOT REQUIRED",
            "grounded": "CHECKING"
        }

        # --------------------------------
        # STEP 1: Initial Retrieval
        # --------------------------------

        print("\nRetrieving documents...")

        documents = self.retriever.invoke(
            question
        )

        status["retrieval"] = (
            f"{len(documents)} documents retrieved"
        )

        print(
            f"Retrieved {len(documents)} documents."
        )


        # --------------------------------
        # STEP 2: Self-RAG
        # --------------------------------

        print("Running Self-RAG relevance grading...")

        relevant_documents = (
            filter_relevant_documents(
                question,
                documents
            )
        )

        status["self_rag"] = (
            f"{len(relevant_documents)} relevant documents"
        )

        print(
            f"Self-RAG found "
            f"{len(relevant_documents)} relevant documents."
        )


        # --------------------------------
        # STEP 3: Corrective RAG
        # --------------------------------

        if not relevant_documents:

            print(
                "No relevant documents found."
            )

            print(
                "Running Corrective RAG..."
            )

            (
                corrected_documents,
                improved_question,
                was_corrected
            ) = corrective_retrieve(
                question,
                self.retriever
            )

            if was_corrected:

                status["corrective_rag"] = (
                    "QUESTION REWRITTEN + RETRIEVED AGAIN"
                )

                print(
                    "Question rewritten."
                )

                print(
                    f"Improved question: "
                    f"{improved_question}"
                )

            relevant_documents = (
                filter_relevant_documents(
                    improved_question,
                    corrected_documents
                )
            )


        # --------------------------------
        # STEP 4: No useful information
        # --------------------------------

        if not relevant_documents:

            status["grounded"] = "NOT CHECKED"

            return {
                "answer": (
                    "I could not find enough relevant "
                    "information in the Agrisnet knowledge "
                    "base to answer this question."
                ),
                "sources": [],
                "status": status
            }


        # --------------------------------
        # STEP 5: Generate Answer
        # --------------------------------

        print("Generating answer with GPT-4o-mini...")

        answer, context = self.generate_answer(
            question,
            relevant_documents
        )


        # --------------------------------
        # STEP 6: Self-RAG Grounding Check
        # --------------------------------

        print(
            "Checking answer groundedness..."
        )

        grounded = grade_answer_groundedness(
            question,
            context,
            answer
        )

        if grounded:

            status["grounded"] = "PASS"

        else:

            status["grounded"] = "FAILED"


        # --------------------------------
        # STEP 7: Sources
        # --------------------------------

        sources = []

        for document in relevant_documents:

            source = document.metadata.get(
                "source",
                "Agrisnet"
            )

            sources.append(source)


        sources = list(set(sources))


        # --------------------------------
        # STEP 8: Return result
        # --------------------------------

        return {
            "answer": answer,
            "sources": sources,
            "status": status
        }