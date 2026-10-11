
import asyncio

from core.dbconnect import Session
from models.project import Project
from models.code_chunk import CodeChunk
from services.github_injestion_service import GitHubInjestionService
from services.code_chunk_service import ChunkCodeService


async def main():
    db = Session()

    try:
        project_id = 12

        # 1. Verify that the project exists
        project = db.query(Project).filter(
            Project.id == project_id
        ).first()

        if not project:
            print(f"Project {project_id} not found")
            return

        print("Project:", project.name)
        print("Repository:", project.repository_url)

        # 2. Fetch real repository files
        ingestion_service = GitHubInjestionService()

        ingestion_result = await ingestion_service.injest_repo(
            project.repository_url
        )

        files = ingestion_result.get("files", [])

        print("\nIngestion result:")
        print("Supported files:", ingestion_result.get("supported_files"))
        print("Successfully ingested:", ingestion_result.get("successfully_ingested"))
        print("Failed files:", ingestion_result.get("failed_files"))

        if not files:
            print("No files were fetched. Check the ingestion result.")
            return

        # 3. Chunk and store the fetched files
        chunk_service = ChunkCodeService(db)

        storage_result = chunk_service.process_and_store(
            project_id=project.id,
            files=files
        )

        print("\nStorage result:", storage_result)

        # 4. Verify persisted chunks
        saved_chunks = chunk_service.get_project_chunks(project.id)

        print("\nSaved chunks:")
        for chunk in saved_chunks[:10]:
            print(
                f"ID: {chunk.id} | "
                f"File: {chunk.file_path} | "
                f"Chunk: {chunk.chunk_index}"
            )

        print(f"\nTotal chunks found for project: {len(saved_chunks)}")

    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
