
import asyncio

from services.github_service import GithubService


async def main():
    service = GithubService()

    result = await service.get_file_content(
        "https://github.com/marmikvyass/MarmikVyas_Portfolio",
        "index.html"
    )

    print("Repository:", result["repository"])
    print("File:", result["path"])
    print("Size:", result["size"])
    print("\nContent:\n")
    print(result["content"])


if __name__ == "__main__":
    asyncio.run(main())
