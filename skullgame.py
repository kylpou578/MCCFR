class SkullState:
    def __init__(
        self,
        card0=None,
        card1=None,
        stage="p0_card",
        bid=None,
        response=None
    ):
        self.card0 = card0
        self.card1 = card1
        self.stage = stage
        self.bid = bid
        self.response = response

class SkullGame:
    def get_terminal_value(self, state):
        if state.bid == "Two":
            if state.card0 == "Rose" and state.card1 == "Rose":
                return 1
            return -1

        if state.response == "Two":
            if state.card0 == "Rose"and state.card1 == "Rose":
                return -1
            return 1

        if state.response == "Pass":
            if state.card0 == "Skull":
                return -1
            return 1

    def current_player(self, state):
        if state.stage == "p0_card":
            return 0

        if state.stage == "p1_card":
            return 1

        if state.stage == "p0_bid":
            return 0

        if state.stage == "p1_response":
            return 1

    def legal_actions(self, state, player):
        if state.stage == "p0_card":
            assert player == 0
            return ["Rose", "Skull"]

        if state.stage == "p1_card":
            assert player == 1
            return ["Rose", "Skull"]

        if state.stage == "p0_bid":
            assert player == 0
            return ["One", "Two"]

        if state.stage == "p1_response":
            assert player == 1
            return ["Two", "Pass"]

        return []

    def next_state(self, state, action):
        if state.stage == "p0_card":
            return SkullState(
                card0=action,
                card1=None,
                stage="p1_card"
            )

        if state.stage == "p1_card":
            return SkullState(
                card0=state.card0,
                card1=action,
                stage="p0_bid"
            )

        if state.stage == "p0_bid":
            if action == "Two":
                return SkullState(
                    card0=state.card0,
                    card1=state.card1,
                    stage="terminal",
                    bid="Two"
                )

            if action == "One":
                return SkullState(
                    card0=state.card0,
                    card1=state.card1,
                    stage="p1_response",
                    bid="One"
                )

        if state.stage == "p1_response":
            return SkullState(
                card0=state.card0,
                card1=state.card1,
                stage="terminal",
                bid="One",
                response=action
            )

    def information_set(self, state):
        if state.stage == "p0_card":
            return ("P1", "choose_card")

        if state.stage == "p1_card":
            return ("P2", "choose_card")

        if state.stage == "p0_bid":
            return ("P1","bid",state.card0)

        if state.stage == "p1_response":
            return ("P2","response",state.card1,"One")