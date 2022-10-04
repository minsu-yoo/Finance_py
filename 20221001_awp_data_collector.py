# All Weather data collector 

import yfinance as yf
import matplotlib.pyplot as plt
import pickle 

def date_con(date_input):
    
    date_input = str(date_input)
    
    # the date values will be changed from '20220922' to '2022-09-22'
    year = date_input[:4] 
    month = date_input[4:6] 
    day = date_input[6:] 
    day_input = year + '-' + month + '-' + day
    
    return day_input
    


def awp_data_collect(start_date, end_date):
    
    s_day = date_con(start_date)
    e_day = date_con(end_date)
    
    spy = yf.download('SPY', start= s_day, end = e_day,
               progress = False,
               auto_adjust = False, 
               actions = 'inline')


    ief = yf.download('IEF', start= s_day, end = e_day,
               progress = False,
               auto_adjust = False, 
               actions = 'inline')



    tlt = yf.download('TLT', start= s_day, end = e_day,
               progress = False,
               auto_adjust = False, 
               actions = 'inline')



    dbc = yf.download('DBC', start= s_day, end = e_day,
               progress = False,
               auto_adjust = False, 
               actions = 'inline')


    gld = yf.download('GLD', start= s_day, end = e_day,
               progress = False,
               auto_adjust = False, 
               actions = 'inline')

    a4s_data = {}

    #all four seasons data 

    a4s_data['spy'] = spy
    a4s_data['bond_ief'] = ief
    a4s_data['long_bond_tlt'] = tlt
    a4s_data['gold_gld'] = gld
    a4s_data['material_dbc'] = dbc

    plt.style.use('plotstyle.mplstyle')
    
    return a4s_data
