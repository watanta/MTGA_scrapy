# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request
from MTGA_scrapy.items import MtgaScrapyItem
from datetime import datetime

class MtgaSpiderSpider(scrapy.Spider):
    name = 'mtga_spider'
    #allowed_domains = ['mtgdecks.net/Standard']
    allowed_domains = []
    start_urls = ['https://mtgdecks.net/Standard/']

    def parse(self, response):
        #crawl
        themes = response.xpath('//*[@id="archetypesTable"]/tbody//td[2]/strong/a/@href').getall()
        for theme in themes:
            item = MtgaScrapyItem()
            item["theme"] = theme.split('/')[2]
            url = 'https://mtgdecks.net/Standard/' + item["theme"]
            request = Request(url, callback=self.decks_by_theme)
            request.meta["item"] = item

            yield request

    def decks_by_theme(self, response):
        decks = response.xpath('//*[@id="content"]/div[3]/div[1]/div/div[1]/div/div/div/table//td[2]/a')
        dates_path = response.xpath('//*[@id="content"]/div[3]/div[1]/div/div[1]/div/div/div/table//td[5]/strong')
        for deck, date_path in zip(decks, dates_path):
            item = response.meta["item"]
            item["deckname"] = deck.xpath('text()').get()
            item["deck_url"] = deck.xpath('@href').get()
            url = 'https://mtgdecks.net/' + deck.xpath('@href').get()
            month_day = date_path.xpath('text()[1]').get()
            year = date_path.xpath('span/text()').get()
            item['date'] = month_day + year
            request = Request(url, callback=self.deck_detail)
            request.meta["item"] = item


            yield request


        #次のページがあればリンクをたどる
        next_page = response.xpath('//*[@id="content"]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/ul/li[13]/a/@href').get()
        print("next_page", next_page)
        if next_page is not None:
            url = 'https://mtgdecks.net' + next_page
            item = response.meta["item"]
            request = Request(url, callback=self.decks_by_theme)
            request.meta['item'] = item

            print("Next PAGE!")

            yield request

        else:
            pass

    def deck_detail(self, response):
        item = response.meta["item"]

        creatures = response.xpath('//*[@id="compact"]/div/div/table[1]/tr[1]/following-sibling::tr/td[1]')
        creature_dict = {}
        for creature in creatures:
            creature_name = creature.xpath('a/text()').get()
            creature_amount = creature.xpath('text()[2]').get()[1]
            creature_dict[creature_name] = creature_amount

        instants = response.xpath('//*[@id="compact"]/div/div/table[2]/tr[1]/following-sibling::tr/td[1]')
        instants_dict = {}
        for instant in instants:
            instant_name = instant.xpath('a/text()').get()
            instant_amount = instant.xpath('text()[2]').get()[1]
            instants_dict[instant_name] = instant_amount

        scorcerys = response.xpath('//*[@id="compact"]/div/div/table[3]/tr[1]/following-sibling::tr/td[1]')
        scorcery_dict = {}
        for scorcery in scorcerys:
            scorcery_name = scorcery.xpath('a/text()').get()
            scorcery_amount = scorcery.xpath('text()[2]').get()[1]
            scorcery_dict[scorcery_name] = scorcery_amount

        enchantments = response.xpath('//*[@id="compact"]/div/div/table[4]/tr[1]/following-sibling::tr/td[1]')
        enchantment_dict = {}
        for enchantment in enchantments:
            enchantment_name = enchantment.xpath('a/text()').get()
            enchantment_amount = enchantment.xpath('text()[2]').get()[1]
            enchantment_dict[enchantment_name] = enchantment_amount

        planeswalkers = response.xpath('//*[@id="compact"]/div/div/table[5]/tr[1]/following-sibling::tr/td[1]')
        planeswalker_dict = {}
        for planeswalker in planeswalkers:
            planeswalker_name = planeswalker.xpath('a/text()').get()
            planeswalker_amount = planeswalker.xpath('text()[2]').get()[1]
            planeswalker_dict[planeswalker_name] = planeswalker_amount

        lands = response.xpath('//*[@id="compact"]/div/div/table[6]/tr[1]/following-sibling::tr/td[1]')
        land_dict = {}
        for land in lands:
            land_name = land.xpath('a/text()').get()
            land_amount = land.xpath('text()[2]').get()[1]
            land_dict[land_name] = land_amount

        sideboards = response.xpath('//*[@id="compact"]/div/div/table[7]/tr[1]/following-sibling::tr/td[1]')
        sideboard_dict = {}
        for sideboard in sideboards:
            sideboard_name = sideboard.xpath('a/text()').get()
            sideboard_amount = sideboard.xpath('text()[2]').get()[1]
            sideboard_dict[sideboard_name] = sideboard_amount

        main_deck = {}
        main_deck.update(creature_dict)
        main_deck.update(instants_dict)
        main_deck.update(enchantment_dict)
        main_deck.update(planeswalker_dict)
        main_deck.update(land_dict)

        item["main"] = main_deck
        item["side"] = sideboard_dict

        print(item)

        yield item
