from mtgsdk import Card
from pymongo import MongoClient
import json

cards_list = Card.where(gameFormat='Standard').all()
client = MongoClient('localhost', 27017)
db = client.mtga
collection = db['cards']

for card in cards_list:
    post = {}
    post["name"] = card.name
    post["cmc"] = card.cmc
    post["color"] = card.colors
    post["color_identity"] = card.color_identity
    post["type"] = card.type
    post["rarity"] = card.rarity
    post["text"] = card.text
    post["flavor"] = card.flavor
    post["power"] = card.power
    post["toughness"] = card.toughness
    post["loyalty"] = card.loyalty
    post["image_url"] = card.image_url
    post['id'] = card.id
    print(post)

    collection.insert_one(post)




