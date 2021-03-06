# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MtgaScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    theme = scrapy.Field()
    deckname = scrapy.Field()
    main = scrapy.Field()
    side = scrapy.Field()
    date = scrapy.Field()
    deck_url = scrapy.Field()
    main_cardlist = scrapy.Field()
    side_cardlist = scrapy.Field()


    pass
