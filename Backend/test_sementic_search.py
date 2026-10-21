from services.retrieval_service import RetrievalService


def main():
    retrieval = RetrievalService()

    matches = retrieval.retrieve_vector(
        ques="Which technology names and skill descriptions are defined in the skills array?",
        project_id=12,
        n_result=5,
    )

    if not matches:
        print("No matching chunks found.")
        return

    for rank, match in enumerate(matches, start=1):
        metadata = match["metadata"]

        print(f"\n--- Result {rank} ---")
        print("File:", metadata["file_path"])
        print("Chunk:", metadata["chunk_index"])
        print("Distance:", match["distance"])
        print("Code:\n", match["content"])


if __name__ == "__main__":
    main()