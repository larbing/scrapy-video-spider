# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

import logging
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from whoosh.index import create_in,open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.writing import BufferedWriter
from jieba.analyse import ChineseAnalyzer
import os.path

from .settings import INDEXDIR

indexdir = INDEXDIR

class MergeItemPipeline:

    def __init__(self) -> None:
        self.items = {}

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        id = adapter.get("id")

        if id not in self.items.keys():
            self.items[id] = item
        
        else:
            adapter.update(self.items.get(id))
            return adapter.item

class MyspiderPipeline:

    def __init__(self) -> None:

        analyzer = ChineseAnalyzer()
        # 定义索引的模式
        schema = Schema(
            id=ID(stored=True),
            title=TEXT(stored=True,analyzer=analyzer), 
            content=TEXT(analyzer=analyzer),
            url=STORED,
            region=KEYWORD(analyzer=analyzer),
            category=KEYWORD(analyzer=analyzer),
            update_context=KEYWORD(analyzer=analyzer)
        )

        # 创建索引目录
        if not os.path.exists(indexdir):
            os.mkdir(indexdir)

        # 创建索引
        self.ix = create_in(indexdir, schema)
        self.writer = BufferedWriter(self.ix, period=10)

    def process_item(self, item, spider):
        logging.debug(item)
        adapter = ItemAdapter(item)
        self.writer.add_document(
            id=adapter.get("id"),
            title=adapter.get('name'),
            content=adapter.get('name'),
            url=adapter.get('url'),
            region=adapter.get('region'),
            category=adapter.get('category'),
            update_context=adapter.get('update_context')
        )
        self.writer.commit()
        return item
    
    def open_spider(self, spider):
        pass


    
    def close_spider(self, spider):
        self.writer.close()
        self.ix.close()