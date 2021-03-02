import pyflink
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment
import pandas as pd
import numpy as np

print(pyflink)

env = StreamExecutionEnvironment.get_execution_environment()
t_env = StreamTableEnvironment.create(env)

# Create a PyFlink Table
pdf = pd.DataFrame(np.random.rand(10, 3))
table = t_env.from_pandas(pdf, ["a", "b","c"]).filter("a > 0.5")

# Convert the PyFlink Table to a Pandas DataFrame
pdf = table.to_pandas()
print(pdf)
