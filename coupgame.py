import random

class CoupState:
    def __init__(
        self,
        card0=None,
        card1=None,
        coins0=6,
        coins1=6,
        stage="p0_action",
        action=None,
        winner=None,
        steal0_blocked=False,
        steal1_blocked=False
    ):
        self.card0 = card0
        self.card1 = card1

        self.coins0 = coins0
        self.coins1 = coins1

        self.stage = stage
        self.action = action
        self.winner = winner

        self.steal0_blocked = steal0_blocked
        self.steal1_blocked = steal1_blocked

class CoupGame:
    def current_player(self, state):
        if state.stage == "p0_action":
            return 0

        if state.stage == "p1_action":
            return 1

        if state.stage == "p1_challenge":
            return 1

        if state.stage == "p0_challenge":
            return 0

        if state.stage == "p1_block":
            return 1

        if state.stage == "p0_challenge_block":
            return 0

        if state.stage == "p0_block":
            return 0

        if state.stage == "p1_challenge_block":
            return 1

    def legal_actions(self, state, player):
        if state.stage == "terminal":
            return []

        if state.stage == "p0_action":
            if state.coins0 >= 7:
                return ["Coup"]

            actions = ["Income", "Tax"]

            if not state.steal0_blocked:
                actions.append("Steal")

            if state.coins0 >= 7:
                actions.append("Coup")

            return actions

        if state.stage == "p1_action":
            if state.coins1 >= 7:
                return ["Coup"]

            actions = ["Income", "Tax"]

            if not state.steal1_blocked:
                actions.append("Steal")

            if state.coins1 >= 7:
                actions.append("Coup")

            return actions

        if state.stage == "p1_challenge":
            return ["Challenge", "Pass"]

        if state.stage == "p0_challenge":
            return ["Challenge", "Pass"]

        if state.stage == "p1_block":
            return ["Block", "Pass"]

        if state.stage == "p0_challenge_block":
            return ["Challenge", "Pass"]

        if state.stage == "p0_block":
            return ["Block", "Pass"]

        if state.stage == "p1_challenge_block":
            return ["Challenge", "Pass"]

    def next_state(self, state, action):
        if state.stage == "p0_action":
            if action == "Income":
                return CoupState(
                    card0=state.card0,
                    card1=state.card1,
                    coins0=state.coins0 + 1,
                    coins1=state.coins1,
                    stage="p1_action",
                    steal0_blocked=state.steal0_blocked,
                    steal1_blocked=state.steal1_blocked
                )

            if action == "Tax":
                return CoupState(
                    card0=state.card0,
                    card1=state.card1,
                    coins0=state.coins0,
                    coins1=state.coins1,
                    stage="p1_challenge",
                    action="Tax",
                    steal0_blocked=state.steal0_blocked,
                    steal1_blocked=state.steal1_blocked
                )

            if action == "Steal":
                return CoupState(
                    card0=state.card0,
                    card1=state.card1,
                    coins0=state.coins0,
                    coins1=state.coins1,
                    stage="p1_challenge",
                    action="Steal",
                    steal0_blocked=state.steal0_blocked,
                    steal1_blocked=state.steal1_blocked
                )

            if action == "Coup":
                return CoupState(
                    card0=state.card0,
                    card1=state.card1,
                    stage="terminal",
                    winner=0
                )

        if state.stage == "p1_action":
            if action == "Income":
                return CoupState(
                    card0=state.card0,
                    card1=state.card1,
                    coins0=state.coins0,
                    coins1=state.coins1 + 1,
                    stage="p0_action",
                    steal0_blocked=state.steal0_blocked,
                    steal1_blocked=state.steal1_blocked
                )

            if action == "Tax":
                return CoupState(
                    card0=state.card0,
                    card1=state.card1,
                    coins0=state.coins0,
                    coins1=state.coins1,
                    stage="p0_challenge",
                    action="Tax",
                    steal0_blocked=state.steal0_blocked,
                    steal1_blocked=state.steal1_blocked
                )

            if action == "Steal":
                return CoupState(
                    card0=state.card0,
                    card1=state.card1,
                    coins0=state.coins0,
                    coins1=state.coins1,
                    stage="p0_challenge",
                    action="Steal",
                    steal0_blocked=state.steal0_blocked,
                    steal1_blocked=state.steal1_blocked
                )

            if action == "Coup":
                return CoupState(
                    card0=state.card0,
                    card1=state.card1,
                    stage="terminal",
                    winner=1
                )

        if state.stage == "p1_challenge":
            if action == "Challenge":
                if state.action == "Tax":
                    if state.card0 == "Duke":
                        return CoupState(
                            card0=state.card0,
                            card1=state.card1,
                            stage="terminal",
                            winner=0
                        )
                    else:
                        return CoupState(
                            card0=state.card0,
                            card1=state.card1,
                            stage="terminal",
                            winner=1
                        )

                if state.action == "Steal":
                    if state.card0 == "Captain":
                        return CoupState(
                            card0=state.card0,
                            card1=state.card1,
                            stage="terminal",
                            winner=0
                        )
                    else:
                        return CoupState(
                            card0=state.card0,
                            card1=state.card1,
                            stage="terminal",
                            winner=1
                        )

            if action == "Pass":
                if state.action == "Tax":
                    return CoupState(
                        card0=state.card0,
                        card1=state.card1,
                        coins0=state.coins0 + 3,
                        coins1=state.coins1,
                        stage="p1_action",
                        steal0_blocked=state.steal0_blocked,
                        steal1_blocked=state.steal1_blocked
                    )

                if state.action == "Steal":
                    return CoupState(
                        card0=state.card0,
                        card1=state.card1,
                        coins0=state.coins0,
                        coins1=state.coins1,
                        stage="p1_block",
                        action="Steal",
                        steal0_blocked=state.steal0_blocked,
                        steal1_blocked=state.steal1_blocked
                    )

        if state.stage == "p0_challenge":
            if action == "Challenge":
                if state.action == "Tax":
                    if state.card1 == "Duke":
                        return CoupState(
                            card0=state.card0,
                            card1=state.card1,
                            stage="terminal",
                            winner=1
                        )
                    else:
                        return CoupState(
                            card0=state.card0,
                            card1=state.card1,
                            stage="terminal",
                            winner=0
                        )

                if state.action == "Steal":
                    if state.card1 == "Captain":
                        return CoupState(
                            card0=state.card0,
                            card1=state.card1,
                            stage="terminal",
                            winner=1
                        )
                    else:
                        return CoupState(
                            card0=state.card0,
                            card1=state.card1,
                            stage="terminal",
                            winner=0
                        )

            if action == "Pass":
                if state.action == "Tax":
                    return CoupState(
                        card0=state.card0,
                        card1=state.card1,
                        coins0=state.coins0,
                        coins1=state.coins1 + 3,
                        stage="p0_action",
                        steal0_blocked=state.steal0_blocked,
                        steal1_blocked=state.steal1_blocked
                    )

                if state.action == "Steal":
                    return CoupState(
                        card0=state.card0,
                        card1=state.card1,
                        coins0=state.coins0,
                        coins1=state.coins1,
                        stage="p0_block",
                        action="Steal",
                        steal0_blocked=state.steal0_blocked,
                        steal1_blocked=state.steal1_blocked
                    )

        if state.stage == "p1_block":
            if action == "Block":
                return CoupState(
                    card0=state.card0,
                    card1=state.card1,
                    coins0=state.coins0,
                    coins1=state.coins1,
                    stage="p0_challenge_block",
                    action="Steal",
                    steal0_blocked=state.steal0_blocked,
                    steal1_blocked=state.steal1_blocked
                )

            if action == "Pass":
                stolen = min(2, state.coins1)

                return CoupState(
                    card0=state.card0,
                    card1=state.card1,
                    coins0=state.coins0 + stolen,
                    coins1=state.coins1 - stolen,
                    stage="p1_action",
                    steal0_blocked=state.steal0_blocked,
                    steal1_blocked=state.steal1_blocked
                )

        if state.stage == "p0_challenge_block":
            if action == "Challenge":
                if state.card1 == "Captain":
                    return CoupState(
                        card0=state.card0,
                        card1=state.card1,
                        stage="terminal",
                        winner=1
                    )
                else:
                    return CoupState(
                        card0=state.card0,
                        card1=state.card1,
                        stage="terminal",
                        winner=0
                    )

            if action == "Pass":
                return CoupState(
                    card0=state.card0,
                    card1=state.card1,
                    coins0=state.coins0,
                    coins1=state.coins1,
                    stage="p1_action",
                    steal0_blocked=True,
                    steal1_blocked=state.steal1_blocked
                )

        if state.stage == "p0_block":
            if action == "Block":
                return CoupState(
                    card0=state.card0,
                    card1=state.card1,
                    coins0=state.coins0,
                    coins1=state.coins1,
                    stage="p1_challenge_block",
                    action="Steal",
                    steal0_blocked=state.steal0_blocked,
                    steal1_blocked=state.steal1_blocked
                )

            if action == "Pass":
                stolen = min(2, state.coins0)

                return CoupState(
                    card0=state.card0,
                    card1=state.card1,
                    coins0=state.coins0 - stolen,
                    coins1=state.coins1 + stolen,
                    stage="p0_action",
                    steal0_blocked=state.steal0_blocked,
                    steal1_blocked=state.steal1_blocked
                )

        if state.stage == "p1_challenge_block":
            if action == "Challenge":
                if state.card0 == "Captain":
                    return CoupState(
                        card0=state.card0,
                        card1=state.card1,
                        stage="terminal",
                        winner=0
                    )
                else:
                    return CoupState(
                        card0=state.card0,
                        card1=state.card1,
                        stage="terminal",
                        winner=1
                    )

            if action == "Pass":
                return CoupState(
                    card0=state.card0,
                    card1=state.card1,
                    coins0=state.coins0,
                    coins1=state.coins1,
                    stage="p0_action",
                    steal0_blocked=state.steal0_blocked,
                    steal1_blocked=True
                )

    def get_terminal_value(self, state):
        if state.winner == 0:
            return 1

        if state.winner == 1:
            return -1

    def information_set(self, state):
        player = self.current_player(state)

        if player == 0:
            return (
                "P0",
                state.stage,
                state.card0,
                state.coins0,
                state.coins1,
                state.steal0_blocked,
                state.steal1_blocked
            )

        return (
            "P1",
            state.stage,
            state.card1,
            state.coins1,
            state.coins0,
            state.steal0_blocked,
            state.steal1_blocked
        )

def random_card():
    return random.choice(["Duke", "Captain"])