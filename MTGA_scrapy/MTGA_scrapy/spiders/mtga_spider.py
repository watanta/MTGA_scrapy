# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request
from MTGA_scrapy.items import MtgaScrapyItem
from datetime import datetime
import re

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
            request.meta["theme"] = item['theme']

            yield request

    def decks_by_theme(self, response):
        print('decks_by_theme:', response.url)
        decks = response.xpath('//*[@id="content"]/div[3]/div[1]/div/div[1]/div/div/div/table//td[2]/a')
        dates_path = response.xpath('//*[@id="content"]/div[3]/div[1]/div/div[1]/div/div/div/table//td[5]/strong')
        for deck, date_path in zip(decks, dates_path):
            item = MtgaScrapyItem()
            item["theme"] = response.meta["theme"]
            item["deckname"] = deck.xpath('text()').get()
            item["deck_url"] = deck.xpath('@href').get()
            url = 'https://mtgdecks.net/' + deck.xpath('@href').get()
            month_day = date_path.xpath('text()[1]').get()
            year = date_path.xpath('span/text()').get()
            item['date'] = month_day + year
            request = Request(url, callback=self.deck_detail)

            request.meta["theme"] = item["theme"]
            request.meta["deckname"] = item["deckname"]
            request.meta["deck_url"] = item["deck_url"]
            request.meta["date"] = item["date"]

            yield request

        #次のページがあればリンクをたどる
        next_page = response.xpath('//li[not(contains(@class, "next disabled"))]/a[@class="next"]/@href').get()
        print("next_page", next_page)
        print(next_page is not None)
        if next_page is not None:
            item = MtgaScrapyItem()
            item['theme'] = response.meta["theme"]
            print("Next PAGE!")
            url = 'https://mtgdecks.net' + next_page
            request = Request(url, callback=self.decks_by_theme)
            request.meta["theme"] = item["theme"]

            yield request

        else:
            pass

    def deck_detail(self, response):
        item = MtgaScrapyItem()
        item["theme"] = response.meta["theme"]
        item["deckname"] = response.meta["deckname"]
        item["deck_url"] = response.meta["deck_url"]
        item["date"] = response.meta["date"]

        creatures = response.xpath('//th[@class="type Creature"]/parent::tr[1]//following-sibling::tr/td[1]')
        creature_dict = {}
        for creature in creatures:
            creature_name = creature.xpath('a/text()').get()
            creature_amount = re.findall(r'\d{1,2}', creature.xpath('text()[2]').get())[0]
            creature_dict[creature_name] = creature_amount

        artifacts = response.xpath('//th[@class="type Artifact"]/parent::tr[1]//following-sibling::tr/td[1]')
        artifact_dict = {}
        for artifact in artifacts:
            artifact_name = artifact.xpath('a/text()').get()
            artifact_amount = re.findall(r'\d{1,2}', artifact.xpath('text()[2]').get())[0]
            artifact_dict[artifact_name] = artifact_amount

        instants = response.xpath('//th[@class="type Instant"]/parent::tr[1]//following-sibling::tr/td[1]')
        instants_dict = {}
        for instant in instants:
            instant_name = instant.xpath('a/text()').get()
            instant_amount = re.findall(r'\d{1,2}', instant.xpath('text()[2]').get())[0]
            instants_dict[instant_name] = instant_amount

        scorcerys = response.xpath('//th[@class="type Sorcery"]/parent::tr[1]//following-sibling::tr/td[1]')
        scorcery_dict = {}
        for scorcery in scorcerys:
            scorcery_name = scorcery.xpath('a/text()').get()
            scorcery_amount = re.findall(r'\d{1,2}', scorcery.xpath('text()[2]').get())[0]
            scorcery_dict[scorcery_name] = scorcery_amount

        enchantments = response.xpath('//th[@class="type Enchantments"]/parent::tr[1]//following-sibling::tr/td[1]')
        enchantment_dict = {}
        for enchantment in enchantments:
            enchantment_name = enchantment.xpath('a/text()').get()
            enchantment_amount = re.findall(r'\d{1,2}', enchantment.xpath('text()[2]').get())[0]
            enchantment_dict[enchantment_name] = enchantment_amount

        planeswalkers = response.xpath('//th[@class="type Planeswalker"]/parent::tr[1]//following-sibling::tr/td[1]')
        planeswalker_dict = {}
        for planeswalker in planeswalkers:
            planeswalker_name = planeswalker.xpath('a/text()').get()
            planeswalker_amount = re.findall(r'\d{1,2}', planeswalker.xpath('text()[2]').get())[0]
            planeswalker_dict[planeswalker_name] = planeswalker_amount

        lands = response.xpath('//th[@class="type Land"]/parent::tr[1]//following-sibling::tr/td[1]')
        land_dict = {}
        for land in lands:
            land_name = land.xpath('a/text()').get()
            land_amount = re.findall(r'\d{1,2}', land.xpath('text()[2]').get())[0]
            land_dict[land_name] = land_amount

        sideboards = response.xpath('//th[@class="type Sideboard"]/parent::tr[1]//following-sibling::tr/td[1]')
        sideboard_dict = {}
        for sideboard in sideboards:
            sideboard_name = sideboard.xpath('a/text()').get()
            sideboard_amount = re.findall(r'\d{1,2}', sideboard.xpath('text()[2]').get())[0]
            sideboard_dict[sideboard_name] = sideboard_amount

        main_deck = {}
        main_deck.update(creature_dict)
        main_deck.update(artifact_dict)
        main_deck.update(instants_dict)
        main_deck.update(enchantment_dict)
        main_deck.update(planeswalker_dict)
        main_deck.update(land_dict)

        item["main"] = main_deck
        item["side"] = sideboard_dict

        main_cardlist = list(main_deck.keys())
        side_cardlist = list(sideboard_dict.keys())

        item["main_cardlist"] = main_cardlist
        item["side_cardlist"] = side_cardlist

        #print(item)

        yield item
