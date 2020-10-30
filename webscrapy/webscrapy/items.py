# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class WebscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    nameRest = scrapy.Field()
    rating = scrapy.Field()
    dollar_rating= scrapy.Field()
    nbr_reviews = scrapy.Field()
    city = scrapy.Field()
    #food_type = scrapy.Field()