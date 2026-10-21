from services.rag_service import RAGService


def main():
    rag = RAGService()

    answer = rag.answer_question(
        question="who is owner of this portfolio?",
        project_id=12,
        n_result=5,
    )

    print("\nRAG Answer:\n")
    print(answer)


if __name__ == "__main__":
    main()