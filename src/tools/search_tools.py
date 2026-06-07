"""
src/tools/search_tools.py
==========================
External search tools for the NavigatorCrew.
"""

from __future__ import annotations

import os
import textwrap
from typing import Any, Optional, Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from src.config import logger

_SERPER_ENDPOINT = "https://google.serper.dev/search"
_SERPER_DEFAULT_N = 8


class SerperSearchInput(BaseModel):
    query: str = Field(
        ...,
        description=(
            "Search query. Be specific."
        ),
    )
    n_results: int = Field(
        default=_SERPER_DEFAULT_N, ge=1, le=20,
        description="Number of organic results to return (1–20, default 8).",
    )


class SerperDevSearchTool(BaseTool):
    name: str = "SerperDevSearchTool"
    description: str = (
        "Search Google for academic and technical sources using Serper.dev. "
    )
    args_schema: Type[BaseModel] = SerperSearchInput

    def _run(self, query: str, n_results: int = _SERPER_DEFAULT_N, **kwargs: Any) -> str:
        api_key = os.getenv("SERPER_API_KEY", "").strip()
        if not api_key:
            return "ERROR: SERPER_API_KEY is not set."

        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        payload = {"q": query, "num": n_results}

        try:
            resp = requests.post(_SERPER_ENDPOINT, headers=headers, json=payload, timeout=15)
            resp.raise_for_status()
        except Exception as exc:
            return f"ERROR: Serper.dev error: {exc}"

        organic = resp.json().get("organic", [])
        if not organic:
            return f"No results found for query: {query!r}"

        lines = [f"Search results for: {query!r}\n"]
        for i, item in enumerate(organic[:n_results], start=1):
            lines.append(f"[{i}] {item.get('title')}\n    URL: {item.get('link')}\n    Snippet: {item.get('snippet')}\n")

        return "\n".join(lines).rstrip()


class ArxivSearchInput(BaseModel):
    query: str = Field(..., description="arXiv search query.")
    n_results: int = Field(default=5, ge=1, le=15)


class ArxivSearchTool(BaseTool):
    name: str = "ArxivSearchTool"
    description: str = "Search arXiv for academic papers."
    args_schema: Type[BaseModel] = ArxivSearchInput

    def _run(self, query: str, n_results: int = 5, **kwargs: Any) -> str:
        try:
            import arxiv
        except ImportError:
            return "ERROR: 'arxiv' package not installed."

        try:
            client = arxiv.Client()
            search = arxiv.Search(query=query, max_results=n_results)
            results = list(client.results(search))
        except Exception as exc:
            return f"ERROR: arXiv query failed: {exc}"

        if not results:
            return f"No arXiv results for: {query!r}"

        lines = [f"arXiv results for: {query!r}\n"]
        for i, paper in enumerate(results, start=1):
            lines.append(f"[{i}] {paper.title}\n    Authors: {', '.join(a.name for a in paper.authors)}\n    URL: {paper.pdf_url}\n")

        return "\n".join(lines).rstrip()
