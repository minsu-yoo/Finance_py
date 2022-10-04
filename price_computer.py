# price computer


def get_close(date):
    
    day = date_con(date)
    close_values = {}
    for key in keyList:

        close_values[key] = data[key].loc[day].Close
        
    return close_values


    

def get_a4p_price(prices):

    # price of portfolio 

    current_price  = (prices['spy']*.30 + prices['bond_ief']*.15 
                  + prices['long_bond_tlt']*.40
                 + prices['gold_gld']*.75 
                 +prices['material_dbc']*.75)

    return current_price



