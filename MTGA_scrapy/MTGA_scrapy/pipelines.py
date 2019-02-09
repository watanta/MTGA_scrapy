# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient


class MtgaScrapyPipeline(object):
    def __init__(self, mongo_uri, mongo_db, mongodb_collection):
        # インスタンス生成時に渡された引数で、変数初期化。各変数に代入する値は下のfrom_crawlerメソッドにて。
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongodb_collection = mongodb_collection
        # ユーザー、PW認証を行うときは以下のコメントを外す。
        # self.mongolab_user = mongolab_user
        # self.mongolab_pass = mongolab_pass

    @classmethod
    def from_crawler(cls, crawler):
        # settings.pyで定義した変数にアクセスする
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
            mongodb_collection=crawler.settings.get('MONGODB_COLLECTION')
        )

        #userとpassを設定しているならばreturn内にこいつらも含める。外に出してるけど、使うときはreturn cls中に入れる。
            # mongolab_user=crawler.settings.get('MONGOLAB_USER'),
            # mongolab_pass=crawler.settings.get('MONGOLAB_PASS')

    # スパイダー開始時に実行される。データベース接続を行う。
    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # ユーザー、PW認証を行うときは以下のコメントを外す。
        # self.db.authenticate(self.mongolab_user, self.mongolab_pass)

    def close_spider(self, spider): # スパイダー終了時に実行される。データベース接続を閉じる。
        self.client.close()

    # XXspider.pyでitemが返されたときに実行される。
    def process_item(self, item, spider):
        self.db[self.mongodb_collection].insert_one(dict(item))
        # ちなみに既にデータがあるかどうか確認してあったら更新するってばあいはこんな感じ↓
        # self.db[self.mongodb_collection].update(
        #     {u'title': item['title']},
        #     {"$set": dict(item)},
        #     upsert = True
        # )
        return item
