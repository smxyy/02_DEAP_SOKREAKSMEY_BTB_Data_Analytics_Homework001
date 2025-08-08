# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class ScrapeWithScrapyItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class ProductItem(scrapy.Item):
    code = scrapy.Field()
    title = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    review_count = scrapy.Field()
    image_link = scrapy.Field()
    category_type = scrapy.Field()
