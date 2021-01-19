import matplotlib.pyplot as plt 
from datetime import datetime  
import pandas as pd 
import numpy as np


"""
@fun:电芯最高最低电压差；
 @zhaoCQ 2020.01.06
"""
class Voltage:
    def __init__(self , k):
      self.k = k
      self.mean=0
      self.std_deviation=0 

    def  separation(filename,k):
          pass

    def voltage_difference(self,df ,k): 
      #df = pd.read_csv(filename,encoding='GB18030')  
     # print(df.head(0)) 
     
      first_day=df.iat[0, 2]              #value at row index ,colums index  
      last_day=df.iat[df.shape[0]-1, 2] 
      day_interval=[first_day,last_day] 


      prefix='BMS_SignleCellVolt'           #  BMS_SignleCellVolt length is 18 
      sublen=len(prefix)
      strsub_exclude='Valid'                #exclude Valid
      origen_rows=df.shape[0]                #rows 
      column_zero_count_thres=origen_rows*0.01

      print("the origen_rows   is %d" %(origen_rows)) 
      print("column_zero_count_thres %d "%(column_zero_count_thres))

      

      #pick up voltage cols

      listVolt=[] 
      for col in df.columns:
         res=col.find(strsub_exclude)       # substring include BMS_SignleCellVolt and exclude Valid 
         
         #print("col is null %d" %df[col].isnull.sum())
         # if(col=='BMS_SignleCellVolt71Valid'):
         #    print(col)
         #    print(df[col])
         
         volt_column=col[0:sublen]==prefix
         # if volt_column and res==-1:       # voltage columns 
         #    print(col)
         #    print(df[col]) 
         #colums value  is  all null filter condition
         col_null=(df[col].isnull().sum()==origen_rows)  
        # print("null size is :  %d"%df[col].isnull().sum())
         condition_511=df.loc[df.index[1],col]!=511          # exclude data colums is 511    2021.01.13

         if volt_column and res==-1 and not col_null and condition_511:   # pd.notnull(df.at[0,col]) data is not null  
            #np.isnan(df.loc[0,col])
            df[col].value_counts()
            col_zero_count=(df[col]==0).astype(int).sum()
            print("col zero count is : %d"%col_zero_count)  
            if(col_zero_count<column_zero_count_thres):
               listVolt.append(col)     # append columns

                                 
         
      
      
      length=len(listVolt)              #voltage colums length is 90 
      print(" colums after filter is %d" %length) 
      
      volts=df[listVolt]  
      volts[volts == 0.0].count()

      #t=(volts == 0).astype(int).sum(axis=0) 
      #volts.to_csv("voltage.csv")  
      #print(volts) 
      #v_s=volts.iloc[1]
      #print(v_s) 

      rows=volts.shape[0]   #rows  
      print("the rows after filter  is %d" %(rows)) 

      abnormal_diff_big_value=100 
      view_rows=rows 
      statistic_rows=0
      voltage_diff=[]                  #   max -min  
      abnormal_value_count=0
      for index in range(view_rows):  
         # row_data_sort=volts.iloc[index].sort_values()  
         # d=row_data_sort[len(row_data_sort)-k-1]-row_data_sort[k]        # exclude top_k bottom_k voltage differece 

         mi=volts.iloc[index].min()
         ma=volts.iloc[index].max()
         d=ma-mi

         #t=row_data_sort[k:row_data_sort.size-k]        # exclude top_k bottom_k voltage differece 
         if d>abnormal_diff_big_value: 
            abnormal_value_count=abnormal_value_count+1 
             # print("diff  too big  row index is %d:"%index)       
            # print(volts.iloc[index])
            #print(row_data_sort)
         else:
            statistic_rows=statistic_rows+1
            voltage_diff.append(d) 
            
         #print(t)
         #print(type(volts.iloc[index])) #sort_values
         #print(volts.iloc[index])                                                 #visit by row 

      print("statistic_rows is %d" %statistic_rows)
      return(voltage_diff,day_interval)  
      
 
    

    def standard_deviation(self,filename,K): 
         """
         @param:   k : exclude the number of min and max value  
         @author: zhaoCQ 2021.01.11

         """

         df = pd.read_csv(filename,encoding='unicode_escape')
         prefix='BMS_SignleCellVolt'           #  BMS_SignleCellVolt length is 18 
         sublen=len(prefix)
         strsub_exclude='Valid'                #exclude Valid

         #pick up voltage cols
         listVolt=[]
         for col in df.columns:
            res=col.find(strsub_exclude)                           # substring include BMS_SignleCellVolt and exclude Valid
            #colums filter condition
            #print("col size is %d" %df[col].size)
            if col[0:sublen]==prefix and res==-1 and  pd.notnull(df.at[0,col]):   # pd.notnull(df.at[0,col])  df[col].notnull().size==df[col].size data is not null
              #print("col size is %d" %df[col].size)
               listVolt.append(col)                        # colums
            
         
         
         length=len(listVolt)              #voltage colums length is 90 
         print("colums number  is %d" %length)
         listVolt.sort()                   #
         volts=df[listVolt]  
        
         rows=volts.shape[0]   #rows 
         str = "the rows is %d" %(rows)
         print(str)


         abnormal_diff_big_value=100 
         view_rows=rows 
        # view_rows=10 
         statistic_rows=0
         voltage_diff=[]               
         zero_count=0
         mean_value_list=[]
         std_deviation_list=[]



         for index in range(view_rows): 
            row_data_sort=volts.iloc[index].sort_values()
            #print(row_data_sort) 
            part=row_data_sort[k:row_data_sort.size-k] 

            
            tt=np.count_nonzero(row_data_sort)
            if tt!=row_data_sort.size:
               zero_count+=1
               #print("no zero number is %d: " %tt)
               #print("  number size is %d: " %part.size)

            #print(part)  
            #m=np.mean(row_data_sort)
            else :
               mean_value=np.mean(part) 
               std_deviation=np.std(row_data_sort, ddof = 1) # 计算样本方差  
               mean_value_list.append(mean_value)
               std_deviation_list.append(std_deviation)
               print("mean is %d " %mean_value )
               # print("std_deviation is %d "  %std_deviation)
              

        # print(type(mean_value_list ))
         print("valid  lines  is  :  %d" %len(mean_value_list))
         return  mean_value_list,std_deviation_list     
 



  


#filename='/home/zhao/data/problem/LGWECMA42KE024156/LGWECMA42KE024156_20201129-20201229.csv'



filename_static='/home/zhao/python/data_statistic/data/static.csv'
filename_slow_charge='/home/zhao/python/data_statistic/data/slow_charge.csv' 
df = pd.read_csv(filename_static,encoding='GB18030') 

k=0
v=Voltage(k) 
# mean_list,deviation=v.standard_deviation(filename,k)  
# x1=range(0,len(deviation))
# plt.figure(1) 
# #plt.figure(figsize=(100,20))
# plt.title("voltage deviation")
# plt.plot(x1, deviation)
# plt.show()

# x2=range(0,len(mean_list)) 
# plt.figure(2)  
# #plt.figure(figsize=(100,20))
# plt.title("voltage mean")
# plt.plot(x2, mean_list)
# plt.show()



 
voltage_diff,day_interval=v.voltage_difference(df,k)  
x=range(0,len(voltage_diff))
plt.figure(1) # 创建图表1 
#plt.figure(figsize=(100,20))

title=day_interval[1][0:11]+"__"+day_interval[0][0:11]+"  static volt_diff"
plt.title(title)
plt.plot(x, voltage_diff)
plt.savefig("static.png")
plt.show()


print("end")