# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# import scrapy
from scrapy import Item, Field


class Item(Item):
    title = Field()
    price = Field()
    imageUrl = Field()
    detailUrl = Field()
    platform = Field()
    # text = Field()
