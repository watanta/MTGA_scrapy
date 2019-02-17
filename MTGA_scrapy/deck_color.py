from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.mtga
collection_cards = db['cards']
collection_decks = db['decks']

collection_deck_color = db['deck_color']

for deck in collection_decks.find():
    color_set = set()
    main_deck = deck['main']
    for card_name in main_deck:
        print(card_name)
        card = collection_cards.find_one({'name': card_name})
        for color in card['color_identity']:
            color_set.add(color)
    print(color_set)
    print('-----------------------------------------------------------')
    post = {}
    post['deck_url'] = deck['deck_url']
    post['deck_color'] = list(color_set)

    collection_deck_color.insert_one(post)

