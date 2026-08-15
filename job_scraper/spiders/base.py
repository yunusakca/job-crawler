import scrapy

from job_scraper.items import JobItem


class BaseCrawler(scrapy.Spider):
    """Shared helpers for job-board spiders. Subclasses set `source` and
    do their own fetching/parsing."""

    source = None

    def build_item(self, **fields):
        fields.setdefault("source", self.source)
        return JobItem(**fields)
