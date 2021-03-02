

import matplotlib.pyplot as plt 
from change_rate import *
from vehicle_state import *  
from voltage_extreme_diff import *   


filename='/home/zhao/python/data_statistic/data/all_file.csv'   

filename='/home/zhao/data/车型CC7001CE02ABEV/LGWEEUA5XJE001208/LGWEEUA5XJE001208_20200701-20200801.csv'
vs=Vehicle_state()
#volt_columns=vs.filter_voltage(filename) 
#print(volt_columns) 
#print(len(volt_columns)) 
# outfile_static='static.csv'
# vs.static(filename,outfile_static) 
outfile_slow_charge='slow_charge.csv'
vs.slowcharge(filename,outfile_slow_charge)  
print("test state end")
         
         
         

# filename_static='/home/zhao/python/data_statistic/data/static.csv'
# filename_slow_charge='/home/zhao/python/data_statistic/data/slow_charge.csv'   

# filename=filename_slow_charge
# label=" slow_charge_change_rate " 
# k=0
# day_peroid='-10D' 
# change_rate=Change_rate(k) 
# use_days,value=change_rate.change_rate(filename,day_peroid,k)  
# change_rate.data_visual(use_days,value,label)

# print("test slow_charge_change_rate end")



 
# v=Voltage_extreme_diff() 
# label="static_volt_diff"
# voltage_diff,day_interval=v.voltage_difference(filename_static ) 
# v.data_visual(day_interval,voltage_diff,label) 
 

# print("test static volt_diff end")