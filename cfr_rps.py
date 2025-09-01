#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

ROCK = 0
PAPER = 1
SCISSORS = 2
GAME_ACTIONS = [ROCK, PAPER, SCISSORS]
NUM_ACTIONS = 3
NUM_ROUNDS = 100000 #change to change accuracy

strategy = [1/3, 1/3, 1/3]
strategy_sum = [0, 0, 0]
opp_strategy = [0.9, 0.05, 0.05] #change to play around
regret = [0, 0, 0]

def get_opp_move(opp_strategy):
    return random.choices(GAME_ACTIONS, opp_strategy, k=1)[0]

def get_cfr_move(strategy):
    return random.choices(GAME_ACTIONS, strategy, k=1)[0]

def update_strategy(strategy, opp_move, cfr_move):    
    action_utility = [0, 0, 0]
    action_utility[opp_move] = 0
    action_utility[(opp_move + 1) % NUM_ACTIONS] = 1 #since rps follows modular arithmetic
    action_utility[(opp_move - 1) % NUM_ACTIONS] = -1
    
    
    for a in range(NUM_ACTIONS):
        regret[a] += action_utility[a] - action_utility[cfr_move]
    
    #regret might be -ve, which would mess with our strategy, so we fix that here
    positive_regrets = [max(r, 0) for r in regret]
    total_positive = sum(positive_regrets)

    if total_positive > 0:
        for a in range(NUM_ACTIONS):
            strategy[a] = positive_regrets[a] / total_positive
    else:
        for a in range(NUM_ACTIONS):
            strategy[a] = 1 / NUM_ACTIONS

#cfr promises the avg strat follows nash equilibrium not the last strat so we get that here
def get_average_strategy(strategy_sum):
    total = sum(strategy_sum)
    if total > 0:
        return [s / total for s in strategy_sum]
    else:
        return [1 / NUM_ACTIONS] * NUM_ACTIONS


for i in range(NUM_ROUNDS):
    cfr_move = get_cfr_move(strategy)
    opp_move = get_opp_move(opp_strategy)
    update_strategy(strategy, opp_move, cfr_move)

    for a in range(NUM_ACTIONS):
        strategy_sum[a] += strategy[a]

avg_strategy = get_average_strategy(strategy_sum)
print("Average strategy:", avg_strategy)
