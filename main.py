from whoosh.index import create_in , open_dir
from whoosh.fields import *
from whoosh.writing import BufferedWriter
from whoosh.qparser import QueryParser,AndGroup
from whoosh.query import *
from jieba.analyse import ChineseAnalyzer
import pickledb

# import os.path
# import sys
# import subprocess

from myspider.settings import INDEXDIR,DBDIR,PICKLEDB

# analyzer = ChineseAnalyzer()
# schema = Schema(
#             id=ID(stored=True,unique=True),
#             vid=ID(stored=True),
#             name=TEXT(stored=True,analyzer=analyzer), 
#             title=KEYWORD(stored=True),
#             image_url=STORED,
#             region=KEYWORD(stored=True),
#             content_type=KEYWORD(stored=True,analyzer=analyzer),
#             language=KEYWORD(stored=True,analyzer=analyzer),
#             release_date=KEYWORD(stored=True,analyzer=analyzer),
#             rating=KEYWORD(stored=True,analyzer=analyzer),
#             updated=KEYWORD(stored=True,analyzer=analyzer),
#             status=KEYWORD(stored=True,analyzer=analyzer)
# )
# ix = open_dir(INDEXDIR)


# # 创建一个查询解析器
# qp1 = QueryParser("title", ix.schema)
# qp2 = QueryParser("title", ix.schema)

# query1 = qp1.parse("尼安德特人")
# query2 = qp1.parse("千谎百计")

# with ix.searcher() as searcher:
#     results = searcher.search(Or([query1,query2]))
#     for result in results:
#         print(result)


# from tinydb import TinyDB, Query

# db = TinyDB(DBDIR)
# query = Query()


# db.insert({"a":1})
# print( db.search( query.vid == "1715382541" ))


db = pickledb.load(PICKLEDB, False)
print(db.totalkeys())
# for i in range(10000):
#     db.set(f"{i}",i)