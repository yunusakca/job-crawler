import json

import scrapy

from job_scraper.spiders.providers.base import BaseCrawler


class GreenhouseCrawler(BaseCrawler):
    """Every company listed in greenhouse.yaml: scrapy crawl greenhouse"""

    name = "greenhouse"

    async def start(self):
        config = self.load_config("greenhouse")
        for company in config["companies"]:
            url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
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
