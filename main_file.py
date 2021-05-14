#!/usr/bin/env python
# coding: utf-8

# In[3]:


'''Getting the input values from Google Spread API'''
import gspread
import pandas as pd

'''Scrapping value from CoWinAPI'''

import pandas as pd
import numpy as np
import requests as rq
from bs4 import BeautifulSoup as bs
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

'''Twitter Updatation'''
import tweepy
import webbrowser
import time
from tweepy import OAuthHandler

import tweepy
from tweepy import StreamListener
from tweepy import Stream
from datetime import datetime,timedelta
import time
now = datetime.now()
tweet_count=0
base = datetime.today()
print(base)

numdays = 7
date_list = [base + timedelta(days=x) for x in range(numdays)]
# print(date_list)
date_str = [x.strftime("%d-%m-%Y") for x in date_list]

print_flag = 'y'
print_flag = 'y'

##this above import is to minismise SSL Security warning in Macbook


def gspreadData():
    '''Getting the input values from Google Spread API'''
    
    sheet_id='1jYrsjlx4xD8MSkFGM3mItJT59ytoc5_LZJgE6wMSWK0'
    sheet_name='CovidData'
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    url  
    df=pd.read_csv(url,error_bad_lines=False)
    df.dropna(axis=1, how='all')
    print(df)
    return df



def vaccineSlotsByDist(age,district_id):
    headers={'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

    try:
        available_df=[]
        age=age
        
#         'Not Needed above function to use'
#         df_vacc_state=vaccine_state_data()
        try:
#             print(df_vacc_state)
            DIST_ID=district_id
            ##list(df_vacc_state[(df_vacc_state['State_name']== state) & (df_vacc_state['district_name']==district_name)]['district_id'])[0]

        except:
            print("No Combintaiont found")
            return None
            pass

        for inp_date in date_str:
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(DIST_ID, inp_date)
            response = rq.get(URL,headers=headers,verify=False)
            if response.ok:
                resp_json = response.json()
                # print(json.dumps(resp_json, indent = 1))
                if resp_json["centers"]:
#                     print("Available on: {}".format(inp_date))
                    if(print_flag=='y' or print_flag=='Y'):
                        for center in resp_json["centers"]:
                            for session in center["sessions"]:
                                if session["min_age_limit"] <= age :
                                    if(session["vaccine"] != ''):
                                        pass
                                        
                                    else:
                                        
                                        session["vaccine"]='No Information'
#                                     print("\n\n")
                                    available_df.append([center["name"],center["block_name"],center["fee_type"],session["vaccine"],                                                        center['district_name'],center['state_name'],                                                        
                                                        center['pincode'],inp_date, session["available_capacity"], session["min_age_limit"]
                                                        
                                                        ])
                                                        
                           
                                 

                        
                else:
                    pass
#                     print("No available slots on {}".format(inp_date))




        # Create the pandas DataFrame for re grouping whole data into one particlur data frames
        info_vaccination = pd.DataFrame(available_df, columns = ['Vaccination Center', 'Block_name','Fee_type','Vaccine Type',            'District','State Name','Pincode','Available Date','available capacity','Age Group'],index=None)
        
        indexNames = info_vaccination[ (info_vaccination['available capacity'] == 0) ].index
    
        info_vaccination.drop(indexNames , inplace=True)
       
        html=info_vaccination#.set_index(['Available Date', 'State Name','District','pincode'])
        print(html)
        return html

    except Exception as e:
        print("Exception ",e)

def tweet_data(msg):
    '''Twitter Updatation'''


    CONSUMER_KEY='JTZluB3daESewe2ToGofBEdFG'
    CONSUMER_SECRET='hg3BGax9d5TiHw4UmB117WQYKE6Gnhe1dOL0zYyb4DfFlkH5HJ'
    Access_Token='1389917390520033284-of3M07i7EFEtwaM3GtoYkd62vSvaaA'
    Access_Token_Secret='z3ECIPDP6Lh7vbe0k1v0nYxer6GsvCnumsQ3Xtlsr7MqH'


    # callback_uri='oob'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(Access_Token,Access_Token_Secret)
    api=tweepy.API(auth)
    
    print(dist)
    try:
        api.update_status("{}".format(msg))
        
        print("TWeet Successful******")
    except Exception as e:
        print("Exception in Tweeter API status Update: ",e)
    
    

    

    
'''Start of the scripts'''
if __name__=='__main__':
    print("hello Starting to schedule the Run!")
    gspread_data=gspreadData()

    for j,i in enumerate(gspread_data['DistId'].tolist()):
        
        
        print(i)
        print("for District Name: ",gspread_data[gspread_data['DistId']==i]['DistName'])
        val_18=vaccineSlotsByDist(40,i)
        time.sleep(2)
        val_45=vaccineSlotsByDist(55,i)
        print(val_45,val_18)
        time.sleep(2)
        try:
            value=pd.concat([val_18, val_45], axis=0)
        except:
            print("Exception in Value concatination")
        print("Value:",value)

        for inp_date in date_str:
            dist='_'.join(gspread_data[gspread_data['DistId']==i]['DistName'].tolist()[0].split(' '))
            
            msg="#{0}\U0001F4E2 \n Date: {1} \n\n\t \U0001F489 Slots Available: \n\t".format(dist,inp_date)
#             print("String dates inserting",dist)
            
            covs_45=len(value[(value['Available Date']==inp_date) & (value['Vaccine Type']=='COVISHIELD') & (value['Age Group']==45)])
           
            covx_45=len(value[(value['Available Date']==inp_date) & (value['Vaccine Type']=='COVAXIN') & (value['Age Group']==45)])
        
            covs_18=len(value[(value['Available Date']==inp_date) & (value['Vaccine Type']=='COVISHIELD') & (value['Age Group']==18)])
           
            covx_18=len(value[(value['Available Date']==inp_date) & (value['Vaccine Type']=='COVAXIN') & (value['Age Group']==18)])
           
                
#             print([covs_45,covx_45,covs_18,covx_18])
            if all(v == 0 for v in [covs_45,covx_45,covs_18,covx_18]):
                print("No data for: ",inp_date)
#                 continue

            else:

                if covs_45 !=0:
                    cov_45_flag='\t Covishield - 45+/{} Slots \n\t'.format(covs_45)
                    msg=msg+cov_45_flag
                if covx_45 !=0:
                    covx_45_flag='\t Covaxin - 45+/{} Slots \n\t'.format(covx_45)
                    msg=msg+covx_45_flag

                if covs_18 !=0:
                    covs_18_flag='\t Covishield (18-44)/{} Slots \n\t'.format(covs_18)
                    msg=msg + covs_18_flag

                if covx_18 !=0:
                    covx_18_flag='\t Covaxin (18-44)/{} Slots \n\t'.format(covx_18)
                    msg=msg+ covx_18_flag

                msg=msg+'#COVID19IndiaHelp #VaxTrack \n\n Last Tracked: {}'.format(now.strftime('%d-%m-%Y, %I:%M%p'))
                print(msg)
                tweet_data(msg)
                time.sleep(1.5)
                tweet_count+=1
        if j%2==0:
            print("Waiting time ^_^")
            time.sleep(150)
            print("Waiting time ENDS ^_^")
        else:
            pass
                

print("Total Tweet done in this Schdule: ",tweet_count)       
        
    


# In[ ]:




