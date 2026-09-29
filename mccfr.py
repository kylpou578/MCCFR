import random

from coupgame import CoupState, CoupGame, random_card
from skullgame import SkullState, SkullGame

def sample_from_distribution(probabilities):
    r = random.random()
    cumulative = 0.0

    for i, probability in enumerate(probabilities):
        cumulative += probability

        if r <= cumulative:
            return i

    return len(probabilities) - 1

class InfoSet:
    def __init__(self, actions):
        self.actions = tuple(actions)

        self.regret_sum = [0.0 for _ in self.actions]
        self.strategy_sum = [0.0 for _ in self.actions]

    def strategy(self):
        positive_regrets = [max(r, 0.0) for r in self.regret_sum]
        total = sum(positive_regrets)
        if total > 0:
            return [r / total for r in positive_regrets]

        n = len(self.actions)

        return [1.0 / n] * n

    def average_strategy(self):
        total = sum(self.strategy_sum)

        if total <= 0:
            n = len(self.actions)
            return [1.0 / n] * n

        return [value / total for value in self.strategy_sum]

class MCCFR:
    def __init__(self, game):
        self.game = game
        self.infosets = {}

    def get_infoset(self, state, player):
        key = self.game.information_set(state)

        if key not in self.infosets:
            actions = self.game.legal_actions(state,player)
            self.infosets[key] = InfoSet(actions)

        return self.infosets[key]

    def cfr(self,state,traverser):
        if state.stage == "terminal":
            utility = self.game.get_terminal_value(state)

            if traverser == 1:
                utility = -utility

            return utility

        player = self.game.current_player(state)

        infoset = self.get_infoset(state,player)

        strategy = infoset.strategy()

        if player == traverser:
            action_utilities = []
            for action in infoset.actions:
                child = self.game.next_state(state,action)
                utility = self.cfr(child,traverser)
                action_utilities.append(utility)

            node_utility = sum(strategy[i] * action_utilities[i] for i in range(len(strategy)))

            for i in range(len(strategy)):
                regret = action_utilities[i] - node_utility
                infoset.regret_sum[i] += regret

            return node_utility

        for i in range(len(strategy)):
            infoset.strategy_sum[i] += strategy[i]

        action_index = sample_from_distribution(strategy)

        action = infoset.actions[action_index]

        child = self.game.next_state(state,action)

        return self.cfr(child,traverser)

    def train(self, iterations):
        for _ in range(iterations):
            """state = SkullState()
            self.cfr(state,traverser=0)
            
            state = SkullState()
            self.cfr(state,traverser=1)"""
            state = CoupState(card0=random_card(),card1=random_card())
            self.cfr(state,traverser=0)

            state = CoupState(card0=random_card(),card1=random_card())
            self.cfr(state,traverser=1)

def main():
    #game = SkullGame()
    game = CoupGame()
    solver = MCCFR(game)
    solver.train(100000)
    print("Learned strategies:")
    for key, infoset in sorted(solver.infosets.items(),key=lambda x: str(x[0])):
        strategy = infoset.average_strategy()
        print(f"Information set: {key}")

        for action, probability in zip(infoset.actions,strategy):
            print(f"    {action:>5}: {probability:.4f}")

if __name__ == "__main__":
    main()