from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, SQLContext
import os, re, sys, math
from django.shortcuts import render
from django.db import connection
# import mysql.connector

# spark = SparkSession.builder.master('local').appName('searchApp').getOrCreate()
# #sc = SparkContext.getOrCreate(SparkConf())
# sc = spark.sparkContext
# sql = SQLContext(sc)

# connection = mysql.connector.connect(host = "localhost",
#                                     user = 'root',
#                                     passwd = '12345678',
#                                     db = 'project')

# You can also submit the job to v a spark cluster, e.g.:
# spark = SparkSession.builder.master(‘spark://dpw2tcxu:7077’).appName(‘searchcall’).getOrCreate()
# sc = spark.sparkContext
# sql = SQLContext(sc)
# Be careful, in case of spark cluster, the tf-idf index should be in an HDFS, e.g.:
# sql.read.parquet(‘hdfs://ds-hdfs:9000/user/hduser/tf-idf3K1200M’)
#tfidf_RDD = sql.read.parquet("tfidf-index").rdd.map(lambda x: (x['_2'], (x['_1'], x['_3'])))
#('conditions', ('3.txt', 0.47712125471966244))

# here we use mysql statement to select the index.
def sql_search(query):
    # same as results in index function (views.py).
    # cursor = connection.cursor()
    # cursor.execute("SELECT filename, TFIDF, rowNum FROM booktfidf WHERE term = " + str(query) + " And TFIDF > " + str(0.25) + " ORDERBY TFIDF LIMIT " + str(topN))
    # rows = cursor.fetchall()
    # # total results of data in MySQL.
    # print(rows)
    # cursor.close()
    # connection.close()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM (SELECT filename, TFIDF FROM booktfidf WHERE term = '" + str(query) + "'" + ") AS a ORDER BY TFIDF DESC LIMIT 20;")
        row = cursor.fetchall()
        num = len(row)
    return num, row

# # read index from mysql, by using spark statement.
# tfidf_RDD = sql.read.parquet("/root/MyPyspark/Gutenberg/Django/dpwII_project/tfidf-index").rdd.map(lambda x: (x['_1'], (x['_2'], x['_3'])))
# print(tfidf_RDD.take(2))

# # User information
# user = 'root'
# pw = '12345678'
# ## Database information
# table_name = 'booktfidf'
# url = 'jdbc:mysql://localhost:3306/project?user='+user+'&password='+pw
# properties ={ 'password': pw,'user': user}
# df = spark.read.jdbc(url=url, table=table_name, properties=properties)
# df.show(10)
# df.printSchema()
# #convert it into rdd form.
# tfidf_RDD = df.rdd
# tfidf_RDD.take(3)

# def tokenize(s):
#     return re.split("\\W+", s.lower())

# def search(query, topN):
#     # create a RDD.
#     # collectAsMap just like collect, used to display the content.
#     tokens = sc.parallelize(tokenize(query)).map(lambda x: (x, 1)).collectAsMap()
#     #print(tokens)
#     # {'war': 1}

#     # make all data which key equals to query change to the form of token.
#     bcTokens = sc.broadcast(tokens)
#     #print(bcTokens)
#     # <pyspark.broadcast.Broadcast object at 0x000002AD7109F190>

#     joined_tfidf = tfidf_RDD.map(lambda x: (x[0], bcTokens.value.get(x[0], '-'), x[1])).filter(lambda x: x[1] != '-')
#     #print(joined_tfidf.take(10))
#     # [('war', 1, ('120-0.txt', 0.21226716587714003)), ('war', 1, ('1342-0.txt', 0.12493873660829993)),
#     # ('war', 1, ('1400-8.txt', 0.16254904394775976)), ('war', 1, ('2600-0.txt', 0.43388180332601806)),
#     # ('war', 1, ('36-0.txt', 0.27187809265078156)), ('war', 1, ('74-0.txt', 0.23052421803783169)),
#     # ('war', 1, ('76-0.txt', 0.16254904394775976)), ('war', 1, ('98-0.txt', 0.12493873660829993)),
#     # ('war', 1, ('frankenstein.txt', 0.16254904394775976)), ('war', 1, ('monte_cristo.txt', 0.29959559514598016))]

#     scount = joined_tfidf.map(lambda a: a[2]).aggregateByKey((0, 0), (lambda acc, value: (acc[0] + value, acc[1] + 1)),(lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1])))
#     #print(scount.take(10))
#     # [('120-0.txt', (0.21226716587714003, 1)), ('1342-0.txt', (0.12493873660829993, 1)),
#     # ('1400-8.txt', (0.16254904394775976, 1)), ('2600-0.txt', (0.43388180332601806, 1)),
#     # ('36-0.txt', (0.27187809265078156, 1)), ('74-0.txt', (0.23052421803783169, 1)),
#     # ('76-0.txt', (0.16254904394775976, 1)), ('98-0.txt', (0.12493873660829993, 1)),
#     # ('frankenstein.txt', (0.16254904394775976, 1)), ('monte_cristo.txt', (0.29959559514598016, 1))]

#     scores = scount.map(lambda x: (x[1][0] * x[1][1] / len(tokens), x[0])).top(topN)  ##sorted here by top
#     # (20, [(0.43388180332601806, '2600-0.txt'), (0.29959559514598016, 'ulysses.txt'),
#     # (0.29959559514598016, 'monte_cristo.txt'), (0.27187809265078156, '36-0.txt'),
#     # (0.23052421803783169, '74-0.txt'), (0.21226716587714003, '120-0.txt'),
#     # (0.2001593512872196, 'sherlock.txt'), (0.16254904394775976, 'frankenstein.txt'),
#     # (0.16254904394775976, '76-0.txt'), (0.16254904394775976, '1400-8.txt'),
#     # (0.12493873660829993, '98-0.txt'), (0.12493873660829993, '1342-0.txt')])

#     return topN, scores
