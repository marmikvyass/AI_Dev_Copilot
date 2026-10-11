
import asyncio

from services.github_injestion_service import GitHubInjestionService
from rag.chunking_repo import ChunkingRepo


async def main():
    ingestion_service = GitHubInjestionService()
    chunking_service = ChunkingRepo()

    repository_url = (
        "https://github.com/marmikvyass/MarmikVyas_Portfolio"
    )

    result = await ingestion_service.injest_repo(repository_url)

    chunks = chunking_service.chunk_files(result["files"])

    print("Repository:", result["repository"])
    print("Files ingested:", result["successfully_ingested"])
    print("Total chunks:", len(chunks))

    for chunk in chunks[:5]:
        print("\nFile:", chunk["file_path"])
        print("Chunk index:", chunk["chunk_index"])
        print(chunk["content"][:200])


if __name__ == "__main__":
    asyncio.run(main())
