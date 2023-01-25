import requests
import json
import datetime
import time
import yaml
import pickle


with open('config.yaml', encoding='UTF-8') as f:
    _cfg = yaml.load(f, Loader=yaml.FullLoader)
APP_KEY = _cfg['APP_KEY']
APP_SECRET = _cfg['APP_SECRET']
ACCESS_TOKEN = ""
CANO = _cfg['CANO']
ACNT_PRDT_CD = _cfg['ACNT_PRDT_CD']
DISCORD_WEBHOOK_URL = _cfg['DISCORD_WEBHOOK_URL']
URL_BASE = _cfg['URL_BASE']

def send_message(msg):
    """디스코드 메세지 전송"""
    now = datetime.datetime.now()
    message = {"content": f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {str(msg)}"}
    requests.post(DISCORD_WEBHOOK_URL, data=message)
    print(message)

def get_access_token():
    """토큰 발급"""
    headers = {"content-type":"application/json"}
    body = {"grant_type":"client_credentials",
    "appkey":APP_KEY, 
    "appsecret":APP_SECRET}
    PATH = "oauth2/tokenP"
    URL = f"{URL_BASE}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    ACCESS_TOKEN = res.json()["access_token"]
    return ACCESS_TOKEN
    
def hashkey(datas):
    """암호화"""
    PATH = "uapi/hashkey"
    URL = f"{URL_BASE}/{PATH}"
    headers = {
    'content-Type' : 'application/json',
    'appKey' : APP_KEY,
    'appSecret' : APP_SECRET,
    }
    res = requests.post(URL, headers=headers, data=json.dumps(datas))
    hashkey = res.json()["HASH"]
    return hashkey

def get_current_price(code="005930"):
    """현재가 조회"""
    PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
            "authorization": f"Bearer {ACCESS_TOKEN}",
            "appKey":APP_KEY,
            "appSecret":APP_SECRET,
            "tr_id":"FHKST01010100"}
    params = {
    "fid_cond_mrkt_div_code":"J",
    "fid_input_iscd":code,
    }
    res = requests.get(URL, headers=headers, params=params)
    return int(res.json()['output']['stck_prpr'])

def get_target_price(code="005930"):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    PATH = "uapi/domestic-stock/v1/quotations/inquire-daily-price"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
        "authorization": f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"FHKST01010400"}
    params = {
    "fid_cond_mrkt_div_code":"J",
    "fid_input_iscd":code,
    "fid_org_adj_prc":"1",
    "fid_period_div_code":"D"
    }
    res = requests.get(URL, headers=headers, params=params)
    stck_oprc = int(res.json()['output'][0]['stck_oprc']) #오늘 시가
    stck_hgpr = int(res.json()['output'][1]['stck_hgpr']) #전일 고가
    stck_lwpr = int(res.json()['output'][1]['stck_lwpr']) #전일 저가
    target_price = stck_oprc + (stck_hgpr - stck_lwpr) * 0.01
    return target_price

def get_stock_balance():
    """주식 잔고조회"""
    PATH = "uapi/domestic-stock/v1/trading/inquire-balance"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC8434R",
        "custtype":"P",
    }
    params = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "AFHR_FLPR_YN": "N",
        "OFL_YN": "",
        "INQR_DVSN": "02",
        "UNPR_DVSN": "01",
        "FUND_STTL_ICLD_YN": "N",
        "FNCG_AMT_AUTO_RDPT_YN": "N",
        "PRCS_DVSN": "01",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": ""
    }
    res = requests.get(URL, headers=headers, params=params)
    stock_list = res.json()['output1']
    evaluation = res.json()['output2']
    stock_dict = {}
    
    send_message(f"====주식 보유잔고====")
    for stock in stock_list:
        if int(stock['hldg_qty']) > 0:
            stock_dict[stock['pdno']] = stock['hldg_qty']


            send_message(f"{stock['prdt_name']}({stock['pdno']}): {stock['hldg_qty']}주")
            time.sleep(0.1)
    send_message(f"주식 평가 금액: {evaluation[0]['scts_evlu_amt']}원")
    time.sleep(0.1)
    send_message(f"평가 손익 합계: {evaluation[0]['evlu_pfls_smtl_amt']}원")
    time.sleep(0.1)
    send_message(f"총 평가 금액: {evaluation[0]['tot_evlu_amt']}원")

    time.sleep(0.1)
    send_message(f"=================")
    return stock_dict






def get_stock_bought_balance():
    """주식 잔고조회"""
    PATH = "uapi/domestic-stock/v1/trading/inquire-balance"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC8434R",
        "custtype":"P",
    }
    params = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "AFHR_FLPR_YN": "N",
        "OFL_YN": "",
        "INQR_DVSN": "02",
        "UNPR_DVSN": "01",
        "FUND_STTL_ICLD_YN": "N",
        "FNCG_AMT_AUTO_RDPT_YN": "N",
        "PRCS_DVSN": "01",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": ""
    }
    res = requests.get(URL, headers=headers, params=params)
    stock_list = res.json()['output1']
    evaluation = res.json()['output2']
    stock_dict = {}
    
    send_message(f"====주식 보유잔고====")
    for stock in stock_list:
        if int(stock['hldg_qty']) > 0:
            stock_dict[stock['pdno']] = stock['pchs_amt']

            #stock_dict[stock['pdno']] = stock['hldg_qty']
        
            send_message(f"{stock['prdt_name']}({stock['pdno']}): {stock['hldg_qty']}주  {stock['pchs_amt']} 에 삼")
            time.sleep(0.1)
    send_message(f"주식 평가 금액: {evaluation[0]['scts_evlu_amt']}원")
    time.sleep(0.1)
    send_message(f"평가 손익 합계: {evaluation[0]['evlu_pfls_smtl_amt']}원")
    time.sleep(0.1)
    send_message(f"총 평가 금액: {evaluation[0]['tot_evlu_amt']}원")
    time.sleep(0.1)
    send_message(f"=================")
    return stock_dict


#print(stock['pchs_amt'])

def get_stock_num():  ## 메시지 없이 숫자만 보내기
    """주식 잔고조회"""
    PATH = "uapi/domestic-stock/v1/trading/inquire-balance"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC8434R",
        "custtype":"P",
    }
    params = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "AFHR_FLPR_YN": "N",
        "OFL_YN": "",
        "INQR_DVSN": "02",
        "UNPR_DVSN": "01",
        "FUND_STTL_ICLD_YN": "N",
        "FNCG_AMT_AUTO_RDPT_YN": "N",
        "PRCS_DVSN": "01",
        "CTX_AREA_FK100": "",
        "CTX_AREA_NK100": ""
    }
    res = requests.get(URL, headers=headers, params=params)
    stock_list = res.json()['output1']
    evaluation = res.json()['output2']
    stock_dict = {}
    
    #send_message(f"====주식 보유잔고====")
    for stock in stock_list:
        if int(stock['hldg_qty']) > 0:
            stock_dict[stock['pdno']] = stock['pchs_amt']

            #stock_dict[stock['pdno']] = stock['hldg_qty']
        
            #send_message(f"{stock['prdt_name']}({stock['pdno']}): {stock['hldg_qty']}주  {stock['pchs_amt']} 에 삼")
            #time.sleep(0.1)
    #send_message(f"주식 평가 금액: {evaluation[0]['scts_evlu_amt']}원")
    #time.sleep(0.1)
    #send_message(f"평가 손익 합계: {evaluation[0]['evlu_pfls_smtl_amt']}원")
    #time.sleep(0.1)
    #send_message(f"총 평가 금액: {evaluation[0]['tot_evlu_amt']}원")
    #time.sleep(0.1)
    #send_message(f"=================")
    return stock_dict


def get_balance():
    """현금 잔고조회"""
    PATH = "uapi/domestic-stock/v1/trading/inquire-psbl-order"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC8908R",
        "custtype":"P",
    }
    params = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "PDNO": "005930",
        "ORD_UNPR": "65500",
        "ORD_DVSN": "01",
        "CMA_EVLU_AMT_ICLD_YN": "Y",
        "OVRS_ICLD_YN": "Y"
    }
    res = requests.get(URL, headers=headers, params=params)
    cash = res.json()['output']['ord_psbl_cash']
    send_message(f"주문 가능 현금 잔고: {cash}원")
    return int(cash)



def buy(code="005930", qty="1"):
    """주식 시장가 매수"""  
    PATH = "uapi/domestic-stock/v1/trading/order-cash"
    URL = f"{URL_BASE}/{PATH}"
    data = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "PDNO": code,
        "ORD_DVSN": "01",
        "ORD_QTY": str(int(qty)),
        "ORD_UNPR": "0",
    }
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC0802U",
        "custtype":"P",
        "hashkey" : hashkey(data)
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))
    if res.json()['rt_cd'] == '0':
        send_message(f"[매수 성공]{str(res.json())}")
        return True
    else:
        send_message(f"[매수 실패]{str(res.json())}")
        return False



def sell(code="005930", qty="1"):
    """주식 시장가 매도"""
    PATH = "uapi/domestic-stock/v1/trading/order-cash"
    URL = f"{URL_BASE}/{PATH}"
    data = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "PDNO": code,
        "ORD_DVSN": "01",
        "ORD_QTY": qty,
        "ORD_UNPR": "0",
    }
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC0801U",
        "custtype":"P",
        "hashkey" : hashkey(data)
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))
    if res.json()['rt_cd'] == '0':
        send_message(f"[매도 성공]{str(res.json())}")
        return True
    else:
        send_message(f"[매도 실패]{str(res.json())}")
        return False



# 자동매매 시작
try:
    ACCESS_TOKEN = get_access_token()
    
    with open('20230110_good_code.pickle', 'rb') as f:
        good_code = pickle.load(f)
    
    symbol_list = good_code

    #symbol_list = ["032190","066980","004360","073640", "242040", "066980"] # 매수 희망 종목 리스트
    bought_list = [] # 매수 완료된 종목 리스트


    bought_price = {} ##
    bought_qty = {}  ##


    bought_price_list = [] # 매수 완료된 종목 리스트

    total_cash = get_balance() # 보유 현금 조회
    stock_dict = get_stock_balance() # 보유 주식 조회
    stock_bought_dict = get_stock_bought_balance() # 보유 매입가격 조회

    

    for sym in stock_bought_dict.keys():
        bought_price_list.append(stock_bought_dict[sym])

    for sym in stock_dict.keys():
        bought_list.append(sym)


    target_buy_count = 3 # 매수할 종목 수
    buy_percent = 0.33 # 종목당 매수 금액 비율
    buy_amount = total_cash * buy_percent  # 종목별 주문 금액 계산
    soldout = False

    send_message("===국내 주식 자동매매 프로그램을 시작합니다===")
    #send_message(bought_list[0])
    while True:


        t_now = datetime.datetime.now()
        t_9 = t_now.replace(hour=9, minute=0, second=0, microsecond=0)
        t_start = t_now.replace(hour=9, minute=5, second=0, microsecond=0)
        t_sell = t_now.replace(hour=15, minute=30, second=0, microsecond=0)
        t_exit = t_now.replace(hour=15, minute=30, second=0,microsecond=0)
        today = datetime.datetime.today().weekday()

        #send_message(f"현재 보유 회사의 수는 ({len(bought_list)} .")
        
        if today == 5 or today == 6:  # 토요일이나 일요일이면 자동 종료
            send_message("주말이므로 프로그램을 종료합니다.")
            break
        if t_9 < t_now < t_start and soldout == False: # 잔여 수량 매도
            for sym, qty in stock_dict.items():
                sell(sym, qty)
            soldout == True
            bought_list = []
            stock_dict = get_stock_balance()
            stock_num_dict = get_stock_num()


        if t_start < t_now < t_sell :  # AM 09:05 ~ PM 03:15 : 매수

            send_message("-2. Let's do it again.") 
            stock_dict = get_stock_balance()  # msy 현재 보유한 주식체크
            stock_bought_dict = get_stock_bought_balance() # 보유 매입가격 조회
            bought_list = stock_dict.keys()
            
            for sym in symbol_list:
                #bought_list = get_stock_num
                #stock_dict = get_stock_balance()  # msy 현재 보유한 주식체크
                #stock_bought_dict = get_stock_bought_balance() # 보유 매입가격 조회
                #bought_list = stock_dict.keys()

                if len(bought_list) < target_buy_count:
                    send_message("-1. 더 살 수 있어서 체크합니다.") 
                    if sym in bought_list:
                        continue
                    target_price = get_target_price(sym)
                    current_price = get_current_price(sym)
                    if target_price < current_price:
                        buy_qty = 0  # 매수할 수량 초기화
                        buy_qty = int(buy_amount // current_price)
                        if buy_qty > 0:
                            send_message(f"{sym} 목표가 달성({target_price} < {current_price}) 매수를 시도합니다.")
                            result = buy(sym, buy_qty)
    
                            if result:  ## 사는 것이 성공했을 때  
                                soldout = False
                                #bought_list.append(sym)
                                #bought_price[sym] = current_price  ### 구매했을 때의 가격
                                #bought_qty[sym] = buy_qty  ## 구매했을 때 몇 주를 샀는지 확인
                                get_stock_balance()

                    time.sleep(1)  # 찾아야 하는 종목이 많아지면 더
                    #for sym, qty in stock_dict.items():  # 매번 이곳에서 얼마의 boght_list 가 있는지를 체크한다. 

                    
                else:

                    send_message("13. 설정 종목 수 모두 다 샀습니다.")


            time.sleep(1)


            stock_dict = get_stock_balance()  # msy 현재 보유한 주식체크
            stock_bought_dict = get_stock_bought_balance() # 보유 매입가격 조회
            bought_list = stock_dict.keys()            

            for b_sym in bought_list:

                buy_price = float(stock_bought_dict[b_sym])
                buy_num = float(stock_dict[b_sym])
                sell_qty = stock_dict[b_sym]
                real_buy_price = buy_price/buy_num
            #b_target_price = bought_price[b_sym]*1.01
                #stock_bought_dict[b_sym] 

                b_sell_target_price = (real_buy_price)*.995
                b_current_price = get_current_price(b_sym)
                #send_message(f"종목은 {b_sym} 입니다.")
                #send_message(f"{real_buy_price} 에 샀습니다."  )
                #send_message(f" 지금은 {b_current_price} 입니다."  )
                

                if (b_current_price < b_sell_target_price):

                    send_message(f"14. 종목은 {b_sym} 입니다.")
                    send_message(f"15. {real_buy_price} 에 샀습니다."  )
                    send_message(f" 16. 지금은 {b_current_price} 입니다."  )
                    send_message("17. 샀던 가격보다 더 적어지고 있습니다.")
                    send_message(f"18. {stock_dict[b_sym]} 주를 팔아야 할 것 같습니다.")

                    sell_res = sell(b_sym, sell_qty)

                    if sell_res:

                        pass
                        
                        #bought_list.remove(b_sym)  #매도 실패했을 때는 지우지 말아야 한다.

                    else:
                        pass

                    time.sleep(1)
                    #stock_dict
                    
                else:
                    send_message(f"19. 종목은 {b_sym} 입니다.")
                    send_message(f"20. {real_buy_price} 에 샀습니다."  )
                    send_message(f" 21. 지금은 {b_current_price} 입니다."  )
                    send_message("22. Everything is good now. ")

                    #time.sleep(1)
            #   sell(b_sym, bought_qty[b_sym])
            #  bought_list.remove(b_sym)

            time.sleep(1)

            


            if t_now.minute == 30 and t_now.second <= 5: 
              get_stock_balance()
              time.sleep(5)

                        
        if t_sell < t_now < t_exit:  # PM 03:15 ~ PM 03:20 : 일괄 매도
            if soldout == False:
                stock_dict = get_stock_balance()
                for sym, qty in stock_dict.items():
                    sell(sym, qty)
                soldout = True
                bought_list = []
                time.sleep(1)
        if t_exit < t_now:  # PM 03:20 ~ :프로그램 종료
            send_message("프로그램을 종료합니다.")
            break

        
except Exception as e:
    send_message(f"[오류 발생]{e}")
    time.sleep(1)

