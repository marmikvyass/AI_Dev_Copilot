import asyncio
from services.github_injestion_service import (
    GitHubInjestionService
)


async def main():
    service = GitHubInjestionService()

    repository_url = (
        "https://github.com/marmikvyass/MarmikVyas_Portfolio"
    )

    result = await service.injest_repo(repository_url)

    print("Repository:", result["repository"])
    print("Supported files:", result["supported_files"])
    print("Successfully ingested:", result["successfully_ingested"])
    print("Failed files:", len(result["failed_files"]))

    for file in result["files"]:
        print("\nFile:", file["path"])
        print(file["content"][:1000])


if __name__ == "__main__":
    asyncio.run(main())
