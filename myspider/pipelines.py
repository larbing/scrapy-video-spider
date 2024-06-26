# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

import os.path
import logging
import pickledb

from time import strftime,strptime
from whoosh.index import create_in,open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.writing import BufferedWriter
from jieba.analyse import ChineseAnalyzer
from itemadapter import ItemAdapter
from .settings import INDEXDIR,DBDIR

indexdir = INDEXDIR


class DBPipeline:

    def __init__(self) -> None:
        self.db = pickledb.load(DBDIR, False)

    def process_item(self, item, spider):
        if item:
            info = self.db.get(item['id'])
            if info:
                item['vid'] = info['vid']

            self.db.set(item['id'],ItemAdapter(item).asdict())
            self.db.set(item['vid'],item['id'])
            return item
      
    def close_spider(self, spider):
        self.db.dump()

class MergeItemPipeline:

    def __init__(self) -> None:
        self.items = {}

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        id = adapter.get("id")

        if id not in self.items.keys():
            self.items[id] = item
        
        else:
            adapter.update(self.items.pop(id))
            return adapter.item

class MyspiderPipeline:

    def __init__(self) -> None:

        analyzer = ChineseAnalyzer()
        # 定义索引的模式
        schema = Schema(
            id=ID(stored=True,unique=True),
            vid=ID(stored=True),
            name=TEXT(stored=True,analyzer=analyzer), 
            title=KEYWORD(stored=True),
            image_url=STORED,
            region=KEYWORD(stored=True,analyzer=analyzer),
            content_type=KEYWORD(stored=True,analyzer=analyzer),
            language=KEYWORD(stored=True,analyzer=analyzer),
            release_date=KEYWORD(stored=True,analyzer=analyzer),
            rating=KEYWORD(stored=True,analyzer=analyzer),
            updated=KEYWORD(stored=True,analyzer=analyzer),
            status=KEYWORD(stored=True,analyzer=analyzer)
        )

        # 创建索引目录
        if not os.path.exists(indexdir):
            os.mkdir(indexdir)
            self.ix = create_in(indexdir, schema)
        else:
            self.ix = open_dir(indexdir)
        
        self.writer = BufferedWriter(self.ix, period=10)

    def process_item(self, item, spider):
        # logging.debug(item)
        if item is None:
            return
        adapter = ItemAdapter(item)
        # updated = adapter.get('updated')
        # updated = strftime("%Y%m%d",strptime(updated,"%Y-%m-%d"))
        self.writer.update_document(
            id=adapter.get("id"),
            vid=adapter.get("vid"),
            name=adapter.get('name'),
            title=adapter.get('name'),
            image_url=adapter.get('image_url'),
            region=adapter.get('region'),
            content_type=adapter.get('category'),
            release_date=adapter.get('release_date'),
            language=adapter.get('language'),
            rating=adapter.get('rating'),
            updated=adapter.get('updated').replace("-",""),
            status=adapter.get('update_context')
        )
        self.writer.commit()
        return item
    
    def open_spider(self, spider):
        pass


    
    def close_spider(self, spider):
        self.writer.close()
        self.ix.close()