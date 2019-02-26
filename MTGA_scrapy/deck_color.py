from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.mtga
collection_cards = db['cards']
collection_decks = db['decks']

collection_deck_color = db['deck_color']

for deck in collection_decks.find():
    color_set = set()
    main_deck = deck['main']
    print(deck['deck_url'])
    for card_name in main_deck:
        print(card_name)
        card = collection_cards.find_one({'name': card_name})
        for color in card['color_identity']:
            color_set.add(color)
    print(color_set)
    print('-----------------------------------------------------------')
    post = {}
    post['deck_url'] = deck['deck_url']

    #すべての色をFalseにする
    collection_decks.update({'deck_url': deck['deck_url']}, {'$set': {'red': False}})
    collection_decks.update({'deck_url': deck['deck_url']}, {'$set': {'white': False}})
    collection_decks.update({'deck_url': deck['deck_url']}, {'$set': {'green': False}})
    collection_decks.update({'deck_url': deck['deck_url']}, {'$set': {'blue': False}})
    collection_decks.update({'deck_url': deck['deck_url']}, {'$set': {'black': False}})

    #それぞれの色に対応するfieldをTureにする
    if 'R' in color_set:
        collection_decks.update({'deck_url': deck['deck_url']}, {'$set': {'red': True}})
    if 'W' in color_set:
        collection_decks.update({'deck_url': deck['deck_url']}, {'$set': {'white': True}})
    if 'G' in color_set:
        collection_decks.update({'deck_url': deck['deck_url']}, {'$set': {'green': True}})
    if 'U' in color_set:
        collection_decks.update({'deck_url': deck['deck_url']}, {'$set': {'blue': True}})
    if 'B' in color_set:
        collection_decks.update({'deck_url': deck['deck_url']}, {'$set': {'black': True}})





