

#https://zhuanlan.zhihu.com/p/166502285

#bin/kafka-topics.sh --zookeeper 10.53.174.43:2181/kafka --create --replication-factor 1 --partitions 1 --topic  test_flink
# bin/kafka-console-producer.sh --broker-list 10.53.174.43:9092  --topic test_flink    //{"id":2,"name":"查询kafka后存储到cvs文件中"}
# bin/kafka-topics.sh --describe --zookeeper 10.53.174.43:2181 --topic test_flink


#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
from pyflink.datastream import StreamExecutionEnvironment, CheckpointingMode
from pyflink.table import StreamTableEnvironment, TableConfig, DataTypes, CsvTableSink, WriteMode, SqlDialect
s_env = StreamExecutionEnvironment.get_execution_environment()
s_env.set_parallelism(1)
#必须开启checkpoint，时间间隔为毫秒，否则不能输出数据
s_env.enable_checkpointing(1000)

st_env = StreamTableEnvironment.create(s_env, TableConfig())
st_env.use_catalog("default_catalog")
st_env.use_database("default_database")
sourceKafkaDdl = """
    create table sourceKafka(
        id int comment '序号',
        name varchar comment '姓名'
    )comment '从kafka中源源不断获取数据' 
    with(
        'connector' = 'kafka',
        'topic' = 'test_flink',        
        'properties.bootstrap.servers' = '10.53.174.43:9092',
        'scan.startup.mode' = 'earliest-offset',
        'format' = 'json'
        
    )
    """
st_env.execute_sql(sourceKafkaDdl)
 
fieldNames = ["id", "name"]
fieldTypes = [DataTypes.INT(), DataTypes.STRING()]
csvSink = CsvTableSink(fieldNames, fieldTypes, "/tmp/result.csv", ",", 1, WriteMode.OVERWRITE)
st_env.register_table_sink("csvTableSink", csvSink)
 
resultQuery = st_env.sql_query("select * from sourceKafka")
resultQuery.insert_into("csvTableSink")
 
st_env.execute("pyflink-kafka-v2")
print("end")








