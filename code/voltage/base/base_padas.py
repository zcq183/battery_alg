
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from datetime import datetime  
import pandas as pd 
import numpy as np  
  
filename='/home/zhao/data/CATL_vehicle_warning/100/t.csv' 
df1 = pd.read_csv(filename,encoding='GB18030') 
df=df1[['VIN', '报文时间']] 
  
x = np.arange(0, 10, 0.1)
  
y = x * 2
  
plt.title("fun")
plt.plot(x, y)
plt.show()


pd.isnull(df)              # 判断df是否为空，返回布尔值
df = df[df[col].isnull()]  # 筛选出df中，列col为空的部分
np.isnan(df.iloc[0,2]) #对df的第0行第2列判断。此方法只对数值起作用，字符不行



 
 #按行统计，返回为一个series：
(df == 0).astype(int).sum(axis=1)
print(df.loc['05-05-11','R003'])
# 或者
print(df.iloc[4,0])

#print(df.iloc[0:2,0:2])  #访问的是第一行第二列的内容  

tt=pd.Period('2017-8-1 18:20:20', freq='D')   # obtain date
line_nums=df.shape[0]     #rows 

print(tt)


 
df = pd.read_csv(filename,encoding='GB18030')
print("colums is :%s"%df.columns)
t=df.columns
print(t[1]) 
print(".........")
print(df.index)

print(type(df.loc[1,'BMS_SignleCellVolt90']))
print(df.loc[1,'BMS_SignleCellVolt90'])


#####draw node and date 

from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
# 生成横纵坐标信息
dates = ['2017-08-5', '2017-09-26','2017-09-29'] 
ys = range(len(dates))
#print(xs) 
plt.plot(dates, ys,marker='o',mec='r',mfc='w') 
#ax1.plot(x,y,ls='--',lw=3,color='b',marker='o',ms=6, mec='r',mew=2, mfc='w',label='业绩趋势走向')


plt.gcf().autofmt_xdate()  # 自动旋转日期标记
plt.show()
