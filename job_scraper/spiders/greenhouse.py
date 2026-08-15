import json

import scrapy

from .base import BaseCrawler


class GreenhouseCrawler(BaseCrawler):
    """Any company on Greenhouse's job board: scrapy crawl greenhouse -a company=gitlab"""

    name = "greenhouse"
    source = "greenhouse"

    def __init__(self, company=None, *args, **kwargs):
        if not company:
            raise ValueError("usage: scrapy crawl greenhouse -a company=<slug>")
        self.company = company
        super().__init__(*args, **kwargs)

    async def start(self):
        url = f"https://boards-api.greenhouse.io/v1/boards/{self.company}/jobs?content=true"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        for job in data.get("jobs", []):
            yield self.build_item(
                title=job.get("title"),
                company=job.get("company_name"),
                location=(job.get("location") or {}).get("name"),
                url=job.get("absolute_url"),
                description=job.get("content"),
                posted_at=job.get("first_published"),
            )
