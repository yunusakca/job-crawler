import json
from collections.abc import AsyncGenerator, Generator

import scrapy
from scrapy.http import Response

from job_scraper.items import JobItem
from job_scraper.spiders.providers.base import BaseCrawler


class GreenhouseCrawler(BaseCrawler):
    """Every company listed in greenhouse.yaml: scrapy crawl greenhouse
    Pass -a companies=foo,bar to crawl only those companies."""

    name = "greenhouse"

    def __init__(self, *args: object, companies: str | None = None, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        self.companies_filter = companies.split(",") if companies else None

    async def start(self) -> AsyncGenerator[scrapy.Request, None]:
        config = self.load_config("greenhouse")
        for company in self.companies_filter or config["companies"]:
            url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response: Response) -> Generator[JobItem, None, None]:
        data = json.loads(response.text)
        for job in data.get("jobs", []):
            departments = job.get("departments") or []
            yield self.build_item(
                external_id=job.get("id"),
                title=job.get("title"),
                company=job.get("company_name"),
                department=departments[0].get("name") if departments else None,
                location=(job.get("location") or {}).get("name"),
                url=job.get("absolute_url"),
                description=job.get("content"),
                posted_at=job.get("first_published"),
            )
