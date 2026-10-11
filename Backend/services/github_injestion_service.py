from calendar import error

from services.github_service import GithubService
import asyncio

class GitHubInjestionService:
    supported_ext = [
        ".py", ".js", ".jsx", ".ts", ".tsx",
        ".json", ".md", ".html", ".css",
        ".sql", ".yaml", ".yml", ".toml",
        ".env.example", ".sh", ".java", ".go",
        ".rs", ".php", ".xml"
    ]

    EXCLUDED_DIRECTORIES = {
        "node_modules",
        ".git",
        "dist",
        "build",
        "coverage",
        "__pycache__",
        ".venv",
        "venv",
        "vendor"
    }

    EXCLUDED_FILES = {
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "poetry.lock",
        "uv.lock",
        "Cargo.lock"
    }

    max_file_size = 500_000  # 50kb
    max_file = 50
    max_concurrent_req = 5


    def __init__(self):
        self.github_ingest = GithubService()


    def is_supported(self, file_path: str) -> bool:
        parts = file_path.split('/')
        file_name = parts[-1]

        if any(directory in self.EXCLUDED_DIRECTORIES for directory in parts[:-1]):
            return False

        if file_name in self.EXCLUDED_FILES:
            return False

        return any(
            file_name.endswith(ext) for ext in self.supported_ext
        )

    async def injest_repo(self, repository_url:str) -> dict:
        #retieve repo file
        tree_data = await self.github_ingest.get_repo_tree(repository_url)

        # 2. Filter relevant files and skip oversized files
        supported_files = [
            file for file in tree_data['files']
            if self.is_supported(file['path'])
            and file.get('size') is not None
            and file['size'] <= self.max_file_size
        ]

        # 3. Limit the initial ingestion size
        supported_files = supported_files[:self.max_file]

        #4 Limit simultaneous github request
        semaphore = asyncio.Semaphore(self.max_concurrent_req)

        async def fetch_files(file_info: dict)-> dict:
            async with semaphore:
                try:
                    return await self.github_ingest.get_file_content(
                        repository_url,
                        file_info['path']
                    )
                except Exception as exc:
                    return{
                        "path" : file_info['path'],
                        "error" : str(exc)
                    }
        #5 Fetch selected files concurrently

        result = await asyncio.gather(
            *[
                fetch_files(file_info) for file_info in supported_files
            ]
        )

        files = [
            result for result in result if "content" in result
        ]
        error = [
            result for result in result if "error" in result
        ]

        return {
            "repository": tree_data["repository"],
            "branch": tree_data["branch"],
            "total_files_found": tree_data["total_files"],
            "supported_files": len(supported_files),
            "successfully_ingested": len(files),
            "failed_files": error,
            "files": files
        }











