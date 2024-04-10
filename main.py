from whoosh.index import create_in , open_dir
from whoosh.fields import *
from whoosh.writing import BufferedWriter
from whoosh.qparser import QueryParser,AndGroup
from whoosh.query import *
from jieba.analyse import ChineseAnalyzer

# import os.path
# import sys
# import subprocess

from myspider.settings import INDEXDIR,DBDIR

analyzer = ChineseAnalyzer()
schema = Schema(
            id=ID(stored=True,unique=True),
            name=TEXT(stored=True,analyzer=analyzer), 
            image_url=STORED,
            region=KEYWORD(stored=True,analyzer=analyzer),
            content_type=KEYWORD(stored=True,analyzer=analyzer),
            language=KEYWORD(stored=True,analyzer=analyzer),
            release_date=KEYWORD(stored=True,analyzer=analyzer),
            rating=KEYWORD(stored=True,analyzer=analyzer),
            status=KEYWORD(stored=True,analyzer=analyzer)
)
ix = open_dir(INDEXDIR,schema=schema)




# # 创建一个查询解析器
qp1 = QueryParser("region", ix.schema)
qp2 = QueryParser("name", ix.schema)

query1 = qp1.parse("大陆")
query2 = qp2.parse("我的")

with ix.searcher() as searcher:
    results = searcher.search(Or([query1,query2]))
    for result in results:
        print(result)


from tinydb import TinyDB, Query

db = TinyDB(DBDIR)
query = Query()

print( db.search(query.id == "512168fde4ac3c38eedfc9a42eeef3e4") )

