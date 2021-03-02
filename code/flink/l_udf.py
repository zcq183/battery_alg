#https://developer.aliyun.com/article/769987
#https://www.cnblogs.com/xiexiandong/p/12878642.html

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, DataTypes
from pyflink.table.udf import udf
import pandas as pd

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)
t_env = StreamTableEnvironment.create(env)
t_env.get_config().get_configuration().set_boolean("python.fn-execution.memory.managed", True)

@udf(input_types=[DataTypes.STRING(), DataTypes.FLOAT()],
     result_type=DataTypes.FLOAT(), udf_type='pandas')
def interpolate(id, temperature):
    # takes id: pandas.Series and temperature: pandas.Series as input
    df = pd.DataFrame({'id': id, 'temperature': temperature})
    print(df.head(2))

    # use interpolate() to interpolate the missing temperature
    interpolated_df = df.groupby('id').apply(
        lambda group: group.interpolate(limit_direction='both'))

    # output temperature: pandas.Series
    return interpolated_df['temperature']

t_env.register_function("interpolate", interpolate)

my_source_ddl = """
    create table mySource (
        id INT,
        temperature FLOAT 
    ) with (
        'connector.type' = 'filesystem',
        'format.type' = 'csv',
        'connector.path' = '/tmp/input'
    )
"""

my_sink_ddl = """
    create table mySink (
        id INT,
        temperature FLOAT 
    ) with (
        'connector.type' = 'filesystem',
        'format.type' = 'csv',
        'connector.path' = '/tmp/output'
    )
"""

t_env.execute_sql(my_source_ddl)
t_env.execute_sql(my_sink_ddl)

t_env.from_path('mySource')\
    .select("id, interpolate(id, temperature) as temperature") \
    .insert_into('mySink')

t_env.execute("pandas_udf_demo")
print("end")