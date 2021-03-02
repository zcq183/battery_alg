from battery import Battery
from kalman import ExtendedKalmanFilter as EKF
from protocol import launch_experiment_protocol
import numpy as np
import math as m 
import matplotlib.pyplot as plt 
from datetime import datetime  
import pandas as pd  


def plot_everything(time, true_voltage, mes_voltage, true_SoC, estim_SoC, current):
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)

    # title, labels
    ax1.set_title('')    
    ax1.set_xlabel('Time / s')
    ax1.set_ylabel('voltage / V')
    ax2.set_xlabel('Time / s')
    ax2.set_ylabel('Soc')
    ax3.set_xlabel('Time / s')
    ax3.set_ylabel('Current / A')


    ax1.plot(time, true_voltage, label="True voltage")
    ax1.plot(time, mes_voltage, label="Mesured voltage")
    ax2.plot(time, true_SoC, label="True SoC")
    ax2.plot(time, estim_SoC, label="Estimated SoC")
    ax3.plot(time, current, label="Current")
    
    ax1.legend()
    ax2.legend()
    ax3.legend()

    plt.show()




def get_EKF(R0, R1, C1, std_dev, time_step):
    # initial state (SoC is intentionally set to a wrong value)
    # x = [[SoC], [RC voltage]]
    x = np.matrix([[0.5],\
                   [0.0]])

    exp_coeff = m.exp(-time_step/(C1*R1))
    
    # state transition model
    F = np.matrix([[1, 0        ],\
                   [0, exp_coeff]])

    # control-input model
    B = np.matrix([[-time_step/(Q_tot * 3600)],\
                   [ R1*(1-exp_coeff)]])

    # variance from std_dev
    var = std_dev ** 2

    # measurement noise
    R = var

    # state covariance
    P = np.matrix([[var, 0],\
                   [0, var]])

    # process noise covariance matrix
    Q = np.matrix([[var/50, 0],\
                   [0, var/50]])

    def HJacobian(x):
        return np.matrix([[battery_simulation.OCV_model.deriv(x[0,0]), -1]])

    def Hx(x):
        return battery_simulation.OCV_model(x[0,0]) - x[1,0]

    return EKF(x, F, B, P, Q, R, Hx, HJacobian)









def launch_experiment_protocol_2(Q_tot, time_step,current,voltage_measure):

    charge_current_rate = 0.5 #C
    discharge_current_rate = 1 #C
    discharge_constants_stages_time = 20*60 #s
    pulse_time = 60 #s
    total_pulse_time = 40*60 #s

    high_cut_off_voltage = 4.2
    low_cut_off_voltage = 2.5

    #charge CC
   # current = -charge_current_rate * Q_tot
    voltage = 0
    # print("curr is:  %d"%current)
   # while voltage < high_cut_off_voltage:
    voltage = update_all(current,voltage_measure)
    # print("curr is:  %f"%current)
   # print("noise voltage is:  %f"%voltage)
    
 

 




def update_all(actual_current,voltage_mesure):
        battery_simulation.current = actual_current
        battery_simulation.update(time_step)

        time.append(time[-1]+time_step)
        current.append(actual_current)

        # true_voltage.append(battery_simulation.voltage)
        # mes_voltage.append(battery_simulation.voltage + np.random.normal(0, std_dev, 1)[0]) 
        true_voltage.append(voltage_mesure)
        mes_voltage.append(voltage_mesure + np.random.normal(0, std_dev, 1)[0])
        
        Kf.predict(u=actual_current)
        Kf.update(mes_voltage[-1] + R0 * actual_current)
        
        true_SoC.append(battery_simulation.state_of_charge)
        estim_SoC.append(Kf.x[0,0])
        
        return battery_simulation.voltage #mes_voltage[-1]



# total capacity

Q_tot = 3.2
Q_tot = 4

# Thevenin model values
R0 = 0.062
R1 = 0.01
C1 = 3000



battery_simulation = Battery(Q_tot, R0, R1, C1)

# discharged battery
battery_simulation.actual_capacity = 0

# measurement noise standard deviation
std_dev = 0.015

# time period
time_step = 25


#get configured EKF
Kf = get_EKF(R0, R1, C1, std_dev, time_step)

time         = [0]
true_SoC     = [battery_simulation.state_of_charge]
estim_SoC    = [Kf.x[0,0]]
true_voltage = [battery_simulation.voltage]
mes_voltage  = [battery_simulation.voltage + np.random.normal(0,0.1,1)[0]]
current      = [battery_simulation.current]

 

filename='/home/zhao/python/data_statistic/data/slow_charge.csv' 

df = pd.read_csv(filename,encoding='utf_8_sig') 
col=['报文时间','BMS_BattCurr','BMS_SignleCellVolt10','BMS_SOC']
df=df[col]  
 
vol_curr_=df[['BMS_BattCurr','BMS_SignleCellVolt10']]


size=3237  #3237/2 *60=97110
vol_curr=vol_curr_.head(size)


#print(curr.head(10))

print(vol_curr.shape[0])
  



for index in vol_curr.index[::-1]:
    c=vol_curr.iloc[index][0]
    v=vol_curr.iloc[index][1]
    # print(c)
    #  print(v)
   
    current_=(c-8000)/1000 

    voltage_=v/1000 
    # print(type(current_))
    # print(type(index))
    #print("index cur vol  is : %d  %f  %f"%(index,current,voltage_))
    # print("index cur  voltage_   is : %d  %f %f "%(index,current_,voltage_))

    launch_experiment_protocol_2(Q_tot, time_step, current_,voltage_)

plot_everything(time, true_voltage, mes_voltage, true_SoC, estim_SoC, current)
    
    
    
    




