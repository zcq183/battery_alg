
import matplotlib.pyplot as plt 
from datetime import datetime  
import pandas as pd 
import numpy as np  
 
"""
 车辆状态：静态和慢充电
 @zhaoCQ 2020.01.12
"""
class Vehicle_state:
    def __init__(self):
        self.voltage_columns=[]

        pass

    def filter_voltage(self,filename):
        df = pd.read_csv(filename,encoding='GB18030')
        prefix='BMS_SignleCellVolt'           #  BMS_SignleCellVolt length is 18 
        sublen=len(prefix)
        strsub_exclude='Valid'                #exclude Valid
        listVolt=[]
        for col in df.columns:
            res=col.find(strsub_exclude)       # substring include BMS_SignleCellVolt and exclude Valid 
            volt_column=col[0:sublen]==prefix 
            col_null=(df[col].isnull().sum()==df.shape[0]) 
        # print("null size is :  %d"%df[col].isnull().sum())
            condition2=df.loc[df.index[1],col]!=511
            if volt_column and res==-1 and not col_null and condition2:   # pd.notnull(df.at[0,col]) data is not null  
            #np.isnan(df.loc[0,col])
                df[col].value_counts()
                col_zero_count=(df[col]==0).astype(int).sum()
                if(col_zero_count<10):
                   listVolt.append(col)     # append columns
        self.voltage_columns=listVolt
        return listVolt



        

    #OBC_ConnectSts==1 && BMS_ChrgSts==1 && BMS_DCChrgConnect==0 &&BMS_BattCurr<8000
    def vehicle_static_slowcharge(self,filename):
        df1 = pd.read_csv(filename,encoding='utf_8_sig')
        df_origin = pd.read_csv(filename,encoding='utf_8_sig')
        col_filter=['报文时间','OBC_ConnectSts','VCU_Sts','BMS_ChrgSts','BMS_BattCurr']
        print(df_origin.columns)
        df_filter=df_origin[col_filter]
      # df_filter.to_csv('filter.csv')


        col2=['报文时间','OBC_ConnectSts','VCU_Sts','VCU_HvPowerCtrl','BMS_DCChrgConnect','BMS_BattCurr']
        df=df1[col2] 
        
        print(df.index)
        # print("\n") 
        continue_one_threshold=20 
        label_slow_charge=[] 
        continue_one=0  
        #########slow  charge  condition
        ''''
        判断条件:OBC_ConnectSts==1 && VCU_Sts==2 && BMS_DCChrgConnect==0 &&BMS_BattCurr<8000  连续次数>5   

        '''

        slow_charge_count=0

        #for index in range(df.shape[0]-1,-1,-1): 
        for index in df.index[::-1]:           # reverse cause rows is time reverse   2021.1.15
        #for index in df.index:
            con_curr= df.loc[index, 'BMS_BattCurr'] <8000  
            v_curr=df.loc[index, 'BMS_BattCurr']
            obc_conn=df.loc[index, 'OBC_ConnectSts']
            vcu_sts=df.loc[index, 'VCU_Sts'] 

            con_slow_charge=df.loc[index, 'OBC_ConnectSts'] ==1 and  df.loc[index, 'VCU_Sts'] ==2  

            if con_slow_charge and con_curr :
                continue_one=continue_one+1
                if(continue_one>continue_one_threshold):
                    slow_charge_count+=1
                # print("slow charge  ")
                    label_slow_charge.append(1)
                else:
                    label_slow_charge.append(0) 
                    
            else:
                continue_one=0
                label_slow_charge.append(0)  
 


        print("slow_charge_count  :  %d \n" %slow_charge_count) 





        df_slow_charge=df_origin 
        df_slow_charge['slow_charge']=label_slow_charge
        df_slow_charge = df_slow_charge.drop(df_slow_charge[df_slow_charge['slow_charge']==0].index) 
        df_slow_charge.to_csv('slow_charge.csv') 

        ########2.static state judge 
        """
        VCU_Sts,VCU_HvPowerCtrl , BMS_BattCurr
        判断条件:（0,0 or 3)  continue time  >5 and  'BMS_BattCurr'==8000 
        """
        
        VCU_Sts_state=0
        VCU_HvPowerCtrl_state=0
        continue_zero=0 
        continue_zero_count_threshold=3 
        label_static_state=[]  
        static_count=0 
        #range(len(lista)-1,-1,-1):
         
        #for index in range(df.shape[0]): 
        for index in range(df.shape[0]-1,-1,-1):   # time is inverse  
            #if index>1:
                #if df.iloc[index,2]==0 and df.iloc[index, 3]==0 and df.iloc[index-1,2]==0 and df.iloc[index-1, 3]==3 : 
                con_static=df.iloc[index,2]==0 and (df.iloc[index, 3]==0 or df.iloc[index, 3]==3) and df.iloc[index, 5]==8000 

                if con_static : 
                    continue_zero=continue_zero+1
                    if(continue_zero>continue_zero_count_threshold):
                           # print("label_static_state continue_zero  is satisfied   :  %d"%index )
                            label_static_state.append(1)
                            static_count=static_count+1
                    else:
                        label_static_state.append(0)
                else:
                    continue_zero=0
                    label_static_state.append(0)

              
                    
        print("static_count is : %d"%static_count)           
        print(len(label_slow_charge)) 
        
        df_static=df_origin
        df_static['static_state']=label_static_state  
        df_static = df_static.drop(df_static[df_static['static_state']==0].index) 

        df_static.to_csv('static.csv') 
        

        return df






filename='/home/zhao/data/车型CC7001CE02ABEV/LGWEEUA5XJE001208/LGWEEUA5XJE001208_20200701-20200801.csv' 

filename='/home/zhao/python/data_statistic/all_file.csv' 



vs=Vehicle_state()
volt_columns=vs.filter_voltage(filename) 
#print(volt_columns) 
print(len(volt_columns))
df=vs.vehicle_static_slowcharge(filename)
df.head(30) 
#df.to_csv('out1.csv')
print("test end")
         