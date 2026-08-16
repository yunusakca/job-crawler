from pathlib import Path

import scrapy
import yaml

from job_scraper.items import JobItem

PROVIDERS_DIR = Path(__file__).parent
PROVIDERS_LIST_PATH = PROVIDERS_DIR / "providers-list.yaml"


class BaseCrawler(scrapy.Spider):
    """Shared helpers for job-board spiders. Subclasses set `name` and
    do their own fetching/parsing."""

    def load_config(self, provider_name):
        providers = yaml.safe_load(PROVIDERS_LIST_PATH.read_text())["providers"]
        path = PROVIDERS_DIR / providers[provider_name]["path_to_yaml"]
        return yaml.safe_load(path.read_text())

    def build_item(self, **fields):
        fields.setdefault("source", self.name)
        return JobItem(**fields)
