
import matplotlib.pyplot as plt 
from datetime import datetime  
import pandas as pd 
import numpy as np  

import matplotlib.dates as mdates
 

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 
    @brief:day volt_diff change rate  by days  as peroid
    @author:zhaoCQ 
    @date 2020.01.08
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Change_rate:
    
    def __init__(self , k):
      self.k = k


    def get_voltage_colums(filename): 
        df = pd.read_csv(filename,encoding='utf_8_sig')
        prefix='BMS_SignleCellVolt'           #  BMS_SignleCellVolt length is 18 
        sublen=len(prefix)
        strsub_exclude='Valid'                #exclude Valid

        #pick up voltage cols
        listVolt=[]
        for col in df.columns:
            res=col.find(strsub_exclude)                           # substring include BMS_SignleCellVolt and exclude Valid
            #colums filter condition
            if col[0:sublen]==prefix and res==-1 and pd.notnull(df.at[0,col]):   # pd.notnull(df.at[0,col]) data is not null
            #print(col)
                listVolt.append(col)                        # colums 
        return listVolt
    


      
    """
    @brief:  get one day data  
    @param:  filename :input file ;date:filter date   
    @return :  one day  data by date filter
    """   
    def one_day_voltage_data(filename,date):
        df1 = pd.read_csv(filename,encoding='utf_8_sig')
        vol_cols=Change_rate.get_voltage_colums(filename) 
        vol_cols.append('报文时间')  
        df=df1[vol_cols]  

        df['报文时间'] = pd.to_datetime(df['报文时间']) #将数据类型转换为日期类型 
        df = df.set_index('报文时间') # 将'报文时间'设置为index 
        d=df[date]                  # 获取某天的数据
        return d
    



    """
    @brief: voltage diff  cal
    @param: df : input  data  by day ;k:exclude the max,min number of k 
    @return : choose days list
    """
            
    def __vol_diff(self,df,k):        # call by  filter data  ,need modify   
      

        prefix='BMS_SignleCellVolt'           #  BMS_SignleCellVolt length is 18  
        sublen=len(prefix) 
        strsub_exclude='Valid'                #exclude Valid 
        #pick up voltage cols
        #print("\ncolums is %s " ,df.columns)
        listVolt=[]

        #print(df.columns)
        #print(type(df.index))

        if(df.empty):
            print("df is empty") 
            print("the rows is %d" %(df.shape[0]))
            return 0
 
        for col in df.columns:
            res=col.find(strsub_exclude)             # substring include BMS_SignleCellVolt and exclude Valid 
            #print(df.iloc[0:1,0:101])               #访问的是第一行第二列的内容 
            #print(df.loc[df.index[1],'BMS_SignleCellVolt90']) 
            #print(df.loc[1,col])          # and df.loc[1,col]!=511  
           # print(col) 
            condition1=col[0:sublen]==prefix and res==-1 and df[col].notnull().size>10
            #print(df.loc[df.index[2],col])
            condition2=df.loc[df.index[2],col]!=511          #       exclude data colums is 511    2021.01.13

            if condition1 and condition2 :   # pd.notnull(df.at[0,col]) data is not null   df[0].notnull().size
                listVolt.append(col)                        # colums





        voltage_diff=[]              #   max -min  
        colums=len(listVolt)              #voltage colums length is 90 
        print("colums is %d" %colums)
        if colums==0:
            return voltage_diff

       # listVolt.sort()                  
        volts=df[listVolt]  
        rows=volts.shape[0]   #rows  
        print("the rows is %d" %(rows))

        view_rows=rows 
        abnormal_diff_big_value=100 
        statistic_rows=0
      
        abnormal_value_count=0              
        for index in range(view_rows):                        #do not need reverse 
            # row_data_sort=volts.iloc[index].sort_values()
            # d=row_data_sort[len(row_data_sort)-1-k]-row_data_sort[k]        # exclude min ,max k voltage differece 


            mi=volts.iloc[index].min()
            ma=volts.iloc[index].max()
            d=ma-mi 

            if d>abnormal_diff_big_value:
                abnormal_value_count=abnormal_value_count+1
                #print("too big row index is %d" %(index))
            
            else:
                statistic_rows=statistic_rows+1
                voltage_diff.append(d) 
    
        return voltage_diff

    



    """
    @brief: ond day voltage diff mean value 
    @param: filename : input file ;date: dates list ;k:exclude the max,min number of k 
    @return : choose days list
    """

    def one_day_vol_diff_mean(self,filename,date,k):
        df=Change_rate.one_day_voltage_data(filename,date)       #one day data 
        if not df.empty:
            voltage_diff=Change_rate.__vol_diff(self,df,k) 
            if len(voltage_diff)>0:
                mean=np.mean(voltage_diff)  
                return mean
            else :                 # colums is null
                return 0
        else :
            print("%s   day data is empty! "%date) 
            return 0


    """
    @brief: choose  days by interval peroid 
    @param: filename : input file ;dateOffset_d:  interval peroid by day 
    @return : choose days list
    """

    def day_filter(self,filename,dateOffset_d): 
        df1 = pd.read_csv(filename,encoding='utf_8_sig') 
        df=df1[['VIN', '报文时间']] 
        line_nums=df.shape[0]
        #print(df.head(2)) 
        first_day=df.at[0, '报文时间']              #value at row index ,colums index 
        first_day=pd.to_datetime(first_day)
        first_day=pd.Period(first_day, freq='D')   #

        print("first day is : %s" %first_day) 

        last_day=df.at[line_nums-1, '报文时间']
        last_day=pd.to_datetime(last_day)
        last_day=pd.Period(last_day, freq='D')   #
        print("last  day is : %s" %last_day)  

        
        start_day=first_day
        
        start_day=str(start_day)
       # start_day="2020-07-23"   #debug
        
        #print(type(d))
        end_day=str(last_day) 
        
        
        rr=pd.date_range(start=start_day,end=end_day,freq=dateOffset_d, closed='left') 
        date_list=[]
        for i in range(rr.size):
            t=pd.Period(rr[i], freq='D')
            if t>=last_day :
                date_list.append(str(t))
            
                
        return date_list




    """
    @brief:change rate  
    @param: filename : input file ;day_peroid: interval days ;k: Exclude the max,min number of k 
    @return :  days list ,change_value 
    @time:2020.01.12
    """

    def  change_rate(self,filename,day_peroid,k): 
         
        days=Change_rate.day_filter(self,filename,day_peroid)
        #print(days) 
        mean_day_volt_diff=[]
        use_days=[]
        for i in range(len(days)) :
            print("\nday is : %s"%days[i])
            mean=Change_rate.one_day_vol_diff_mean(self,filename,days[i],k) 
            
            print("mean is : %d" %mean)
            if mean!=0:
                mean_day_volt_diff.append(mean)
                use_days.append(days[i])
 

            
        
        change_value=[]
        
        # for i in range(len(mean_day_volt_diff)-1):
        #     d=mean_day_volt_diff[i+1]-mean_day_volt_diff[i]
        #     change_value.append(d)
        # return (use_days, change_value) 
        use_days_ascending=[]

        for i in range(len(mean_day_volt_diff)-1,1,-1):            # volt_diff mean diff cal 
            d=mean_day_volt_diff[i]-mean_day_volt_diff[i-1]
            change_value.append(d)
            use_days_ascending.append(days[i])
        return (use_days_ascending, change_value)




    def data_visual(self,use_days,value,label):
        title=use_days[0] + "__"+use_days[len(use_days)-1] +label
        plt.title(title)            
        plt.plot(use_days, value,marker='o',mec='r',mfc='w')
        plt.gcf().autofmt_xdate()  # 自动旋转日期标记 
        savename=label+".png"
        plt.savefig(savename)
        plt.show() 



 




 

if __name__ == '__main__':

    #filename='/home/zhao/data/车型CC7001CE02ABEV/LGWEEUA5XJE001208/LGWEEUA5XJE001208_20200701-20200801.csv'  

    filename_static='/home/zhao/python/data_statistic/data/static.csv'
    filename_slow_charge='/home/zhao/python/data_statistic/data/slow_charge.csv'   

    filename=filename_slow_charge
    label=" slow_charge_change_rate " 
    k=0
    day_peroid='-10D'

    change_rate=Change_rate(k) 
    use_days,value=change_rate.change_rate(filename,day_peroid,k)  
    change_rate.data_visual(use_days,value,label)


    # title=use_days[0] + "__"+use_days[len(use_days)-1] +" slow_charge change_rate " 
    # plt.title(title)            
    # plt.plot(use_days, value,marker='o',mec='r',mfc='w')
    # plt.gcf().autofmt_xdate()  # 自动旋转日期标记 
    # plt.savefig("slow_charge_change_rate.png")
    # plt.show() 

    print("end")

    
