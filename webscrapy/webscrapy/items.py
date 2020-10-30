# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class WebscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    rest_name = scrapy.Field()
    overall_rating = scrapy.Field()
    dollar_rating = scrapy.Field()
    num_reviews = scrapy.Field()
    location = scrapy.Field()
    reviewer_username = scrapy.Field()
    review_text = scrapy.Field()

