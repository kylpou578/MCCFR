Code is run by running mccfr.py. To change the game, alter the game_name variable

The Skull game implemented is a simplified version of the board game Skull. In this version, two players secretly place face down either a skull or a rose token. The goal is to make a claim for how many roses you can flip face up without flipping over a skull, starting with your own token. If your opponent doesn't raise your claim, you win if you can successfully flip over a number of roses up to your claim, and lose otherwise. Given there are only two tokens, there is a maximum claim size of 2. Here is the game tree:

P1 places face down either a rose or a skull
P2 places face down either a rose or a skull
P1 makes a claim of either "One" or "Two":
    If "Two", P1 wins if both tokens are roses
    If "One", P2 can either "Raise" the claim to two, or "Pass", letting P1 flip over their token:
        If "Raise", P2 wins if both tokens are roses
        If "Pass", P1 must flip over their token first, so P1 wins if it is a rose and loses if it is a skull

The Coup game implemented is a simplified version of Coup. It is between two players and there is only Captain and Duke. Players start with one influence instead of two, and they start the game with an independent 50% chance each of having a captain or duke. Even though I have implemented an extra feature where a Captain can not steal again if successfully blocked, the solver still goes in an infinite loop if the starting coin count is below six because the option still exists for both players to continually allow the stealing of two coins between them.