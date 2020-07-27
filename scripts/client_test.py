# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 11:52:58 2020

@author: 85379
"""


import time
import requests

def testGetIntention():
    print("zzy debug testGetIntention")
    str_player = "\"agent1\""
    str_handcards = "[\"3\", \"3\", \"4\", \"6\", \"6\", \"6\", \"7\", \"7\", \"8\", \"9\", \"9\", \"10\", \"10\", \"J\", \"J\", \"J\", \"Q\", \"Q\", \"K\", \"2\"]"
    # str_handcards = "[\"3\", \"3\", \"6\", \"6\", \"6\", \"7\", \"7\", \"9\", \"9\", \"10\", \"10\", \"J\", \"J\", \"J\", \"Q\", \"Q\", \"K\", \"2\",\"2\",\"2\"]"
    str_last_two_cards = "[[], []]"
    str_prob_state = "[0.0, 0.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, 0.5, 0.5,0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0,0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5, 0.0,0.5, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5,0.0, 0.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0,0.0, 0.5, 0.0, 0.0, 0.0]"
        
    #landlor,up_player,down_player
    payload = {'handcards':str_handcards, 'last_two_cards': str_last_two_cards,'prob_state':str_prob_state,'player':str_player}
    r = requests.get('http://127.0.0.1:8000/getIntention', params=payload)
    print (r.text)          #str

def testGetCardsValue():
    print("zzy debug testGetCardsValue")
    str_handcards = "[\"3\", \"3\", \"6\", \"6\", \"6\", \"7\", \"7\", \"9\", \"9\", \"10\", \"10\", \"J\", \"J\", \"J\", \"Q\", \"Q\", \"K\", \"2\",\"2\",\"2\"]"
    payload = {'handcards':str_handcards}
    r = requests.get('http://127.0.0.1:8000/getCardsValue', params=payload)
    print (r.text)          #str
    
if __name__ == '__main__':
    for i in range(100):
        time_start=time.time()
        testGetIntention()
        print('testGetIntention useTime ', str(time.time()-time_start))
        
        time_start=time.time()
        testGetCardsValue()
        print('testGetCardsValue useTime ',str(time.time()-time_start))