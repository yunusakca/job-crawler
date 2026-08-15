import scrapy


class JobItem(scrapy.Item):
    source = scrapy.Field()
    external_id = scrapy.Field()  # source's native job id, for dedup: (source, external_id)
    title = scrapy.Field()
    company = scrapy.Field()
    department = scrapy.Field()
    location = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    posted_at = scrapy.Field()
