import os
import sys
import json
FILE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(FILE_PATH, '..'))
sys.path.append(ROOT_PATH)
sys.path.insert(0, os.path.join(ROOT_PATH, 'build/Release' if os.name == 'nt' else 'build'))

from datetime import datetime
import numpy as np
from card import Card, Category, CardGroup, action_space
from utils import to_char, to_value, get_mask_alter, give_cards_without_minor, \
    get_mask, action_space_single, action_space_pair, get_category_idx, normalize

from tensorpack import *
from env import Env as CEnv
from mct import mcsearch, CCard, CCardGroup, CCategory
from TensorPack.MA_Hierarchical_Q.env import Env
from TensorPack.MA_Hierarchical_Q.predictor import Predictor
from TensorPack.MA_Hierarchical_Q.DQNModel import Model


weight_path = os.path.join(ROOT_PATH, 'pretrained_model/model-302500')


class MCTEnv(Env):
    def step(self, intention):
        player, done = super().step(intention)
        if player != self.agent_names[0]:
            return 1, done
        else:
            return -1, done

    def step_auto(self):
        def char2ccardgroup(chars):
            cg = CardGroup.to_cardgroup(chars)
            ccg = CCardGroup([CCard(to_value(c) - 3) for c in cg.cards], CCategory(cg.type), cg.value, cg.len)
            return ccg

        def ccardgroup2char(cg):
            return [to_char(int(c) + 3) for c in cg.cards]

        handcards_char = self.get_curr_handcards()
        chandcards = [CCard(to_value(c) - 3) for c in handcards_char]
        player_idx = self.get_current_idx()
        unseen_cards = self.player_cards[self.agent_names[(player_idx + 1) % 3]] + self.player_cards[self.agent_names[(player_idx + 2) % 3]]
        cunseen_cards = [CCard(to_value(c) - 3) for c in unseen_cards]

        next_handcards_cnt = len(self.player_cards[self.agent_names[(player_idx + 1) % 3]])

        last_cg = char2ccardgroup(self.get_last_outcards())
        caction = mcsearch(chandcards, cunseen_cards, next_handcards_cnt, last_cg,
                           (self.agent_names.index(self.curr_player) - self.agent_names.index(self.lord)  + 3) % 3,
                           (self.agent_names.index(self.controller) - self.agent_names.index(self.lord) + 3) % 3, 10, 50, 500)
        intention = ccardgroup2char(caction)
        return self.step(intention)


class MCTEnv(Env):
    def step(self, intention):
        player, done = super().step(intention)
        if player != self.agent_names[0]:
            return 1, done
        else:
            return -1, done

    def step_auto(self):
        def char2ccardgroup(chars):
            cg = CardGroup.to_cardgroup(chars)
            ccg = CCardGroup([CCard(to_value(c) - 3) for c in cg.cards], CCategory(cg.type), cg.value, cg.len)
            return ccg

        def ccardgroup2char(cg):
            return [to_char(int(c) + 3) for c in cg.cards]

        handcards_char = self.get_curr_handcards()
        chandcards = [CCard(to_value(c) - 3) for c in handcards_char]
        player_idx = self.get_current_idx()
        unseen_cards = self.player_cards[self.agent_names[(player_idx + 1) % 3]] + self.player_cards[self.agent_names[(player_idx + 2) % 3]]
        cunseen_cards = [CCard(to_value(c) - 3) for c in unseen_cards]

        next_handcards_cnt = len(self.player_cards[self.agent_names[(player_idx + 1) % 3]])

        last_cg = char2ccardgroup(self.get_last_outcards())
        caction = mcsearch(chandcards, cunseen_cards, next_handcards_cnt, last_cg,
                           (self.agent_names.index(self.curr_player) - self.agent_names.index(self.lord)  + 3) % 3,
                           (self.agent_names.index(self.controller) - self.agent_names.index(self.lord) + 3) % 3, 10, 50, 500)
        intention = ccardgroup2char(caction)
        return self.step(intention)


class RandomEnv(Env):
    
    def __init__(self):
        super().__init__()
        father_Env = Env
        
    def get_state(self):
       return father_Env.get_state()
        
    def step(self, intention):
        # print(self.get_curr_handcards())
        # print(intention)
        player, done = super().step(intention)
        if player != self.agent_names[0]:
            return 1, done
        else:
            return -1, done

    def step_auto(self):
        mask = get_mask(self.get_curr_handcards(), action_space, self.get_last_outcards())
        intention = np.random.choice(action_space, 1, p=mask / mask.sum())[0]
        return self.step(intention)


class CDQNEnv(Env):
    def __init__(self, weight_path):
        super().__init__()
        agent_names = ['agent%d' % i for i in range(1, 4)]
        model = Model(agent_names, (1000, 21, 256 + 256 * 2 + 120), 'Double', (1000, 21), 0.99)
        self.predictors = {n: Predictor(OfflinePredictor(PredictConfig(
            model=model,
            session_init=SaverRestore(weight_path),
            input_names=[n + '/state', n + '_comb_mask', n + '/fine_mask'],
            output_names=[n + '/Qvalue'])), num_actions=(1000, 21)) for n in self.get_all_agent_names()}

    def step(self, intention):
        # print(intention)
        player, done = super().step(intention)
        if player != self.agent_names[0]:
            return 1, done
        else:
            return -1, done

    def step_auto(self):
        handcards = self.get_curr_handcards()
        last_two_cards = self.get_last_two_cards()
        prob_state = self.get_state_prob()
        # game_state = self.getState()
        # game_state_padded = self.get_state_padded()
        # game_state_state2 = self.get_state2()
        # #获取
        # game_cards_value = self.get_cards_value()
        str_handcards = json.dumps(handcards)
        str_last_two_cards = json.dumps(last_two_cards)
        str_prob_state = prob_state.tolist()
        # str_prob_state = str(str_prob_state)
        str_prob_state = json.dumps(str_prob_state)
        
        str_agent_name = json.dumps(self.get_curr_agent_name())
        
        intention = self.predictors[self.get_curr_agent_name()].predict(handcards, last_two_cards, prob_state)
        return self.step(intention)
    
    def getIntention(self,str_player,str_handcards,str_last_two_cards,str_prob_state):
        
        # if player == 'landlord':
        #     curr_agent_name = 'agent1'
        # elif player == 'up_player':
        #     curr_agent_name = 'agent3'
        # elif player == 'down_player':
        #     curr_agent_name = 'agent2'
            
        player = json.loads(str_player)
        prob_state = json.loads(str_prob_state)
        handcards = json.loads(str_handcards)
        last_two_cards = json.loads(str_last_two_cards)

        intention = self.predictors[player].predict(handcards, last_two_cards, prob_state)
        return intention
    


class RHCPEnv(CEnv):
    def __init__(self):
        super().__init__()
        self.agent_names = ['agent1', 'agent2', 'agent3']

    def prepare(self):
        super().prepare()
        self.lord = self.agent_names[self.get_current_idx()]
        self.controller = self.lord
        # print('lord is ', self.lord, self.get_role_ID())

    @property
    def curr_player(self):
        return self.agent_names[self.get_current_idx()]

    @property
    def player_cards(self):
        other_two = self.get_last_two_handcards()
        curr_idx = self.get_current_idx()
        return {
            self.agent_names[(curr_idx + 2) % 3]: to_char(other_two[1]),
            self.agent_names[(curr_idx + 1) % 3]: to_char(other_two[0]),
            self.agent_names[curr_idx]: self.get_curr_handcards()
        }

    def get_current_idx(self):
        return super().get_curr_ID()

    def get_last_outcards(self):
        return to_char(super().get_last_outcards())

    def get_last_two_cards(self):
        last_two_cards = super().get_last_two_cards()
        last_two_cards = [to_char(c) for c in last_two_cards]
        return last_two_cards

    def get_curr_handcards(self):
        return to_char(super().get_curr_handcards())

    def step(self, intention):
        # print(intention)
        idx = self.get_current_idx()
        r, done, category = self.step_manual(to_value(intention))
        if category > 0:
            self.controller = self.agent_names[idx]
        # print(self.agent_names[idx], 'gives', intention, self.controller)
        return r, done

    def step_auto(self):
        idx = self.get_current_idx()
        # print(idx)
        intention, r, _ = super().step_auto()
        intention = to_char(intention)
        if len(intention) > 0:
            self.controller = self.agent_names[idx]
        # print(self.agent_names[idx], 'gives', intention, self.controller)
        assert np.all(self.get_state_prob() >= 0) and np.all(self.get_state_prob() <= 1)
        # print(intention)
        return r, r != 0

class ManualEnv(CEnv):
    def step(self, intention):
        print(intention)
    def step_auto(self):
        print("step_auto")
def make_env(which):
    if which == 'RHCP':
        return RHCPEnv()
    elif which == 'RANDOM':
        return RandomEnv()
    elif which == 'CDQN':
        return CDQNEnv(weight_path)
    elif which == 'MCT':
        return MCTEnv()
    elif which == 'Manual':
        return ManualEnv()
    else:
        raise Exception('env type not supported')
