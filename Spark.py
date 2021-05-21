
# from pyspark import SparkContext
# from pyspark.sql import SQLContext, Row
#
#
#
# sc = SparkContext()
# print("CIAO")
# sqlContext = SQLContext(sc)
#
# #spark = SparkSession.builder.getOrCreate()
# print("CIAO")
# # Enable hive support means that it will be stored in the Hive metastore and not in - memory
# df = sqlContext.read.format("jdbc").option(url="jdbc:mysql://localhost:3306/project_bdt",
#                                            driver = "com.mysql.jdbc.Driver",
#                                            dbtable = "tasso_disoccupazione",
#                                            user="root",
#                                            password="Pr0tett0.98").load()
# print(df)


