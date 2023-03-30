#You will need to install the FFMpeg library : pip install ffmpeg

import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter

#All data courtesy of the Federeral Reserve Bank of St Louis. https://fred.stlouisfed.org/


#Read in data 
#Fed funds rate
fed_funds= pd.read_csv('fed_funds_rate.csv').rename(columns={'DATE': "Time",'FEDFUNDS': 'fed_funds_rate'}).set_index('Time')
fed_funds=fed_funds.loc['2000-08-01':'2022-12-01',:] 
fed_funds.index = pd.to_datetime(fed_funds.index)
fed=fed_funds[['fed_funds_rate']]
 
 
#2yr Treasury
two_yr=pd.read_csv('DGS2.csv').rename(columns={'DATE': "Time",'DGS2':'2yr'}).set_index('Time')
two_yr=two_yr.loc['2000-08-01':'2022-12-01',:] 
two_yr.index=pd.to_datetime(two_yr.index)
two_yr=two_yr[two_yr != "."]
two_yr=two_yr.dropna()
two_yr=two_yr.astype(float) 
two_yr=two_yr.asfreq('MS',method='bfill')
 


#Define the date range for x axis in chart
dates = pd.date_range(start='2000-08-01', end='2022-12-01', freq='MS')

 
# Define the figure and axis shape
fig, ax = plt.subplots(figsize=(15, 7))

# Define the function to animate the plot
def animate(i):
    ax.clear()
    
    #Background color
    ax.set_facecolor('#1075A0')
    
     
    #Plot Fed Funds Rate
    ax.plot(dates[:i+1], fed[:i+1],'#7792E3', label='Fed Funds Rate', linewidth=4, marker='.')
    
     
    #Plot two year 
    ax.plot(dates[:i+1], two_yr[["2yr"]][:i+1],'black', label='2yr', linewidth=2,marker='.')
    
     
    
    #Title
    ax.set_title(' 2yr Treasury versus Fed funds rate since 2000') 
    
    #Define x and y axis upfront so axis will not jump around as data is read in.
    ax.set_ylim([-5, 11])
    ax.set_xlim([dates[0], dates[-1]])
    
    
    ax.legend()
     

# Create the animation and produce an mp4 file in the local directory called "fomc_gfc.mp4"
writer = FFMpegWriter(fps=5,codec='mpeg4')
with writer.saving(fig, "two_yr_vs_fed_funds.mp4",100):
    for i in range(len(dates)):
        animate(i)
      
        writer.grab_frame()




 