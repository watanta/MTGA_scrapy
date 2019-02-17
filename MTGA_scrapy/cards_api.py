from mtgsdk import Card
from pymongo import MongoClient
import json

#cards_list = Card.where(gameFormat='Standard').all()
client = MongoClient('localhost', 27017)
db = client.mtga
collection = db['cards']

standard_set = ['XLN','RIX','DOM','GRN','M19','RNA','G18','PGP1']
# PGP1:Gift Pack2018

for set in standard_set:
    cards_list = Card.where(set=set).all()

    for card in cards_list:
        post = {}
        post["name"] = card.name
        post["cmc"] = card.cmc
        post["color"] = card.colors
        post["color_identity"] = card.color_identity
        post["type"] = card.types[0]
        post["rarity"] = card.rarity
        post["text"] = card.text
        post["flavor"] = card.flavor
        post["power"] = card.power
        post["toughness"] = card.toughness
        post["loyalty"] = card.loyalty
        post["image_url"] = card.image_url
        post['id'] = card.id
        post['layout'] = card.layout
        print(post)

        if card.layout == 'split':
            post['name'] = '/'.join(card.names)

        collection.insert_one(post)




