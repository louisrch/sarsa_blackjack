import os
from typing import TypeVar, List, Generic
import torch
import enum
from actor import Actor
from multiset import *
from dealer import Dealer

T = TypeVar('T')

class Card():
    value : int
    # ace is 1, 2 - 10 is mapped to 2 - 10, jack, queen and king are mapped to 10 as well
    def __init__(self, value : int):
        value = min(value, 10)
        value = max(value, 1)
        self.value = value

class Action(enum):
    FOLD = 0
    HIT = 1



class Stack(Generic[T]):
    queue : list[T]
    index : int
    nleft : int

    def __init__(self, queue):
        self.queue = queue
        self.index = 0
        self.nleft = len(queue)
    
    def pop(self) -> T:
        elem = self.queue[self.index]
        self.index +=1
        self.nleft -= 1
        return elem


  

def cards_to_string(cards : list[Card]) -> str:
    dict ={index: value for index, value in enumerate(cards)}
    multiset = Multiset(dict)
    return str(multiset)
    
def get_cards_sums(cards : list[Card]) -> list[int]:
    sums = [0]
    for c in cards:
        if c.value == 1:
            old_s = add_to_list(sums, 1)
            new_s = add_to_list(sums, 10)
            sums = old_s + new_s
        else:
            sums = add_to_list(sums, c.value)
    return sums



def add_to_list(elem : int, list : list[int]):
    l = list.copy()
    for i in range(len(l)):
        l[i] + elem
    return l

def get_bounded_max(l : list, major : int):
    return max(l[l <= major])

def has_ace(l : list[Card]):
    for card in l:
        if card.value == 1:
            return True
    return False

class Environment():
    cards : Stack[Card]
    player : Actor
    dealer : Dealer
    def __init__(self, cards):
        self.cards = cards
        self.player = Actor(self)
        self.dealer = Dealer(self)
    
    def get_state(self):
        player_state = cards_to_string(self.player.get_cards())
        dealer_state = cards_to_string(self.dealer.get_cards())
        return player_state, dealer_state
    
    def main_loop(self):
        player_cards = [self.cards.pop(), self.cards.pop()]
        self.player.init_round(player_cards)
        dealer_cards = [self.cards.pop]
        self.dealer.init_round(dealer_cards)
        player_bust = False
        dealer_bust = False
        dealer_done = False
        while not (player_bust and dealer_bust and dealer_done):
            self.player.do_one_round()
            self.dealer.do_one_round()

            player_sums = get_cards_sums(self.player.get_cards())
            dealer_sums = get_cards_sums(self.dealer.get_cards())

            if all(dealer_sums>21):
                dealer_bust = True
            if not has_ace(self.dealer.get_cards()):
                if all(dealer_sums>=18):
                    dealer_done = True

            if all(player_sums > 21):
                player_bust = True
            
            if not (player_bust and dealer_bust and dealer_done):
                action = self.player.get_action

        

                


        
      



    

