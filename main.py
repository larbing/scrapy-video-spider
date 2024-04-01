from whoosh.index import create_in , open_dir
from whoosh.fields import *
from whoosh.writing import BufferedWriter
from whoosh.qparser import QueryParser
from jieba.analyse import ChineseAnalyzer

import os.path
import sys
import subprocess

# analyzer = ChineseAnalyzer()
# schema = Schema(
#         id=ID(stored=True),
#         title=TEXT(stored=True,analyzer=analyzer), 
#         content=TEXT(analyzer=analyzer),
#         url=STORED,
#         region=KEYWORD(analyzer=analyzer),
#         category=KEYWORD(analyzer=analyzer),
#         update_context=KEYWORD(analyzer=analyzer)
# )
# ix = open_dir("/home/rock/app/indexdir",schema=schema)




# # 创建一个查询解析器
# qp = QueryParser("content", ix.schema)

# # 执行查询
# with ix.searcher() as searcher:
#     query = qp.parse("五行世家")
#     results = searcher.search(query,limit=50)
#     for result in results:
#         print(result)

