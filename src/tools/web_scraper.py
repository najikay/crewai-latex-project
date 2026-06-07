"""
src/tools/web_scraper.py
=========================
WebScraperTool.
"""

from __future__ import annotations

from typing import Any, Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from src.config import logger


class WebScraperInput(BaseModel):
    url: str = Field(..., description="URL to scrape.")


class WebScraperTool(BaseTool):
    name: str = "WebScraperTool"
    description: str = "Fetch the text content of a web page."
    args_schema: Type[BaseModel] = WebScraperInput

    def _run(self, url: str, **kwargs: Any) -> str:
        logger.debug(f"WebScraperTool: fetching {url}")
        try:
            from crewai_tools import ScrapeWebsiteTool
            return ScrapeWebsiteTool().run(url)
        except Exception as exc:
            return f"ERROR: Scraper failed: {exc}"
