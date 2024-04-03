from whoosh.index import create_in , open_dir
from whoosh.fields import *
from whoosh.writing import BufferedWriter
from whoosh.qparser import QueryParser,AndGroup
from whoosh.query import *
from jieba.analyse import ChineseAnalyzer

# import os.path
# import sys
# import subprocess

from myspider.settings import INDEXDIR

analyzer = ChineseAnalyzer()
schema = Schema(
        id=ID(stored=True),
        title=TEXT(stored=True,analyzer=analyzer), 
        content=TEXT(analyzer=analyzer),
        url=STORED,
        region=KEYWORD(analyzer=analyzer),
        category=KEYWORD(analyzer=analyzer),
        update_context=KEYWORD(analyzer=analyzer)
)
ix = open_dir(INDEXDIR,schema=schema)




# # 创建一个查询解析器
qp1 = QueryParser("content", ix.schema)
qp2 = QueryParser("content", ix.schema)

query1 = qp1.parse("'2024安徽卫视春晚")
query2 = qp2.parse("情人节前7天")


# 执行查询
with ix.searcher() as searcher:
    results = searcher.search(Or([query1,query2]))
    for result in results:
        print(result)

