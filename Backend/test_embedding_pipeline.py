
from core.dbconnect import Session
from services.embedding_pipeline import EmbeddingPipeline


def main():
    db = Session()

    try:
        pipeline = EmbeddingPipeline(db)

        result = pipeline.index_project(project_id=13)

        print("Embedding pipeline result:", result)

    finally:
        db.close()


if __name__ == "__main__":
    main()
