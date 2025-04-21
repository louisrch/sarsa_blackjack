import os
import typing
from environment import Card, Action, Environment
import torch


class Dealer():
    cards : list[Card]
    environment : Environment
    busted : bool
    epsilon : float
    q : dict
    discount : int
    previous_state : list[int]
    previous_action : Action
    previous_reward : int
    alpha : float

    
    def __init__(self, env : Environment):
        self.cards = []
        self.env = env
        self.state = []
        self.busted == False
        self.q = {}
        self.discount = 0

        self.previous_state = []
        self.previous_action = Action.HIT
        self.alpha = 0.05
    
    def init_round(self, cards):
        self.state = []
        self.cards = cards
        self.update_state(cards=cards)

    def hit(self):
        card = self.env.draw().value
        self.cards.append(card)
        self.update_state(card)
    
    

        

    def execute_policy(self, state):
        q_s_a = self.get_act_values(state)
        go_greedy = 1 - torch.bernoulli(self.epsilon)

        # Exploration mode
        if go_greedy == 0:
            hit = torch.bernoulli(0.5)
            if hit == 1:
                action = Action.HIT
            else:
                action = Action.FOLD
        # Greedy procedure
        else:
            # take argmax
            action = max(q_s_a, key=q_s_a.get)
        
        return action

    def get_act_values(self, state, dealer_state):
        state = str(set(state), set(dealer_state))
        if state not in self.policy.keys():
            self.policy[state] = {
                Action.HIT : 0,
                Action.FOLD : 0
            }
        return self.policy[state]


    def update_q_sarsa(self, previous_state, previous_action, reward, current_state, current_action):
        self.q[previous_state][previous_action] += self.alpha *(reward + self.discount * \
                                                                self.q[current_state][current_action] \
                                                                - self.q[previous_state][previous_action])
    
    def parse_reward(self, reward):
        # reward = 1 if win, -1 if lose
        self.reward = reward



    def do_one_round(self):
        # get the state, execute the policy, update q-value function, get reward from the environment
        state = self.env.get_state()
        action = self.execute_policy(state)
        self.update_q_sarsa(self.previous_state, self.previous_action, self.reward, state, action)
        self.update_previous_state(state)
        self.update_previous_action(action)

    def get_cards(self):
        return self.cards
    
    def update_previous_state(self, state):
        self.previous_state = state
    
    def update_previous_action(self, action):
        self.previous_action = action
    

def add_to_list(elem : int, list : list[int]):
    l = list.copy()
    for i in range(len(l)):
        l[i] + elem
    return l




    