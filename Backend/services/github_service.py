import base64
import re
from http.client import responses

import httpx
from fastapi import HTTPException
from starlette import status
import base64


class GithubService:
    @staticmethod
    def parse_repo_url(repository_url: str)-> tuple[str, str]:
        pattern = (
            r"^(?:https?://)?"
            r"(?:www\.)?github\.com/"
            r"([^/]+)/([^/#?]+)"
            r"(?:\.git)?/?$"
        )

        match = re.match(pattern, repository_url.strip())

        if not match:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Invalid Github Repository URL'
            )

        owner, repo = match.groups()

        return owner, repo

    async def get_repo_info(self, repository_url: str) -> dict:
        owner, repo = self.parse_repo_url(repository_url)

        api_url = f"https://api.github.com/repos/{owner}/{repo}"

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    api_url,
                    headers={
                        "Accept" : 'application/vnd.github+json'
                    }
                )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail='Github API Request Timeout'
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=502,
                detail='Could not connect to Github'
            )
        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Repository not found or is not publicly accessible"
            )

        if response.status_code == 403:
            raise HTTPException(
                status_code=502,
                detail="GitHub API rate limit or access restriction"
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail="GitHub API request failed"
            )

        data = response.json()

        return {
            "name": data["name"],
            "full_name": data["full_name"],
            "description": data["description"],
            "html_url": data["html_url"],
            "default_branch": data["default_branch"],
            "language": data["language"],
            "stars": data["stargazers_count"],
        }

    async def get_repo_tree(self, repository_url : str)-> dict:
        owner, repo = self.parse_repo_url(repository_url)

        repo_info = await self.get_repo_info(repository_url)
        branch = repo_info["default_branch"]

        api_url = (
            f"https://api.github.com/repos/{owner}/{repo}"
            f"/git/trees/{branch}?recursive=1"
        )

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    api_url,
                    headers={
                        "Accept" : 'application/vnd.github+json'
                    }
                )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail='Github API Request Timeout'
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=502,
                detail="Could not connect to GitHub"
            )

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Repository tree not found"
            )

        if response.status_code == 403:
            raise HTTPException(
                status_code=502,
                detail="GitHub API rate limit or access restriction"
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail="GitHub tree request failed"
            )

        data = response.json()

        files = [
            {
                "path": item["path"],
                "type": item["type"],
                "sha": item["sha"],
                "size": item.get("size")
            }
            for item in data.get("tree", [])
            if item["type"] == "blob"
        ]

        return {
            "repository": repo_info["full_name"],
            "branch": branch,
            "truncated": data.get("truncated", False),
            "total_files": len(files),
            "files": files
        }

    async def get_file_content(self, repository_url : str,  file_path: str)-> dict:
        owner, repo = self.parse_repo_url(repository_url)

        repo_info = await self.get_repo_info(repository_url)
        branch = repo_info['default_branch']

        api_url = (
            f"https://api.github.com/repos/{owner}/{repo}"
            f"/contents/{file_path}"
        )

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    api_url,
                    params={'ref' : branch},
                    headers={
                        "Accept" : 'application/vnd.github+json'
                    }
                )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail="GitHub file request timed out"
            )

        except httpx.RequestError:
            raise HTTPException(
                status_code=502,
                detail="Could not connect to GitHub"
            )

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="File not found in repository"
            )

        if response.status_code == 403:
            raise HTTPException(
                status_code=502,
                detail="GitHub API rate limit or access restriction"
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail="GitHub file request failed"
            )

        data = response.json()

        if data.get('type') != 'file':
            raise HTTPException(
                status_code=502,
                detail='Requested file type not supported'
            )
        if data.get('encoding') != 'base64':
            raise HTTPException(
                status_code=502,
                detail='Encoding not supported'
            )
        content = base64.b64decode(data['content']).decode(
            'utf-8',
            errors='replace'
        )

        return {
            "repository": repo_info["full_name"],
            "path": data["path"],
            "size": data["size"],
            "content": content
        }