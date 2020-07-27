# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 11:30:07 2020

@author: 85379
"""


from bottle import route, request, run
import json
import os
import sys
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(FILE_PATH, '..'))
sys.path.append(ROOT_PATH)
sys.path.insert(0, os.path.join(ROOT_PATH, 'build/Release' if os.name == 'nt' else 'build'))
from tensorpack.utils.stats import StatCounter
from tensorpack.utils.utils import get_tqdm
from multiprocessing import *
from datetime import datetime
from envs import make_env
from agents import make_agent
from env import Env as CEnv
from card import Card



env = make_env('CDQN')
# str_handcards = "[\"3\", \"3\", \"4\", \"6\", \"6\", \"6\", \"7\", \"7\", \"8\", \"9\", \"9\", \"10\", \"10\", \"J\", \"J\", \"J\", \"Q\", \"Q\", \"K\", \"2\"]"

intention = ['2','2','2','3','3','3','8','9']
feedbackdata = {'feedback': str(intention)}
 

@route('/getIntention')
def start():
    print("zzy test getIntention")
    handcards = str(request.query.handcards)
    print("handcards",type(handcards)," len ",len(handcards),handcards)
    last_two_cards = str(request.query.last_two_cards)
    print("last_two_cards ",type(last_two_cards)," len ",len(last_two_cards),last_two_cards)
    prob_state = str(request.query.prob_state)
    print("prob_state ",type(prob_state)," len ",len(prob_state),prob_state)
    player = str(request.query.player)
    print("player ",player)
    
    intention = env.getIntention(player,handcards,last_two_cards,prob_state)
    # print('radar and station is:', radar, station)

    return json.dumps(intention)

@route('/getCardsValue')
def start():
    print("zzy test getCardsValue")
    str_handcards = str(request.query.handcards)
    print("handcards",type(str_handcards)," len ",len(str_handcards),str_handcards)
    handcards = json.loads(str_handcards)
    cards_value, _ = CEnv.get_cards_value(Card.char2color(handcards))
    return json.dumps(cards_value)

if __name__ == '__main__':
    
    # str_player = "\"agent1\""
    # str_handcards = "[\"3\", \"3\", \"4\", \"6\", \"6\", \"6\", \"7\", \"7\", \"8\", \"9\", \"9\", \"10\", \"10\", \"J\", \"J\", \"J\", \"Q\", \"Q\", \"K\", \"2\"]"
    # str_last_two_cards = "[[], []]"
    # str_prob_state = "[0.0, 0.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, 0.5, 0.5,0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0,0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5, 0.0,0.5, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5,0.0, 0.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0,0.0, 0.5, 0.0, 0.0, 0.0]"
    # env.getIntention(str_player,str_handcards,str_last_two_cards,str_prob_state)
    run(host='127.0.0.1', port=8000, debug=False)
    # handcards = json.loads(str_handcards)
    # cards_value, _ = CEnv.get_cards_value(Card.char2color(handcards))
    # print("cards_value ",str(cards_value))
    
