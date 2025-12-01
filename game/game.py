import random

class Game:
    def __init__(self, strategies, dice_per_player=5):
        """
        strategies: list of functions or objects with choose_action(my_dice, history) method
        dice_per_player: number of dice each player rolls
        """
        self.strategies = strategies
        self.num_players = len(strategies)
        self.dice_per_player = dice_per_player
        self.history = []  # list of bids (quantity, face)

    def roll_dice(self, num):
        """Roll `num` dice, return a list of integers 1-6."""
        return [random.randint(1, 6) for _ in range(num)]

    def legal_bid(self, quantity, face):
        """Check if a bid is strictly higher than the previous bid."""
        if not self.history:
            return True
        prev_q, prev_f = self.history[-1]
        return quantity > prev_q or (quantity == prev_q and face > prev_f)

    def count_dice(self, dice, face):
        """Count total dice showing `face` across all players."""
        total = 0
        for d in dice:
            total += d.count(face)
        return total

    def play_game(self):
        """Play a single-round game. Returns winner index."""
        # Roll dice for all players
        dice = [self.roll_dice(self.dice_per_player) for _ in range(self.num_players)]
        current_player = 0

        while True:
            strategy = self.strategies[current_player]
            action = strategy.choose_action(dice[current_player], self.history)

            if action[0] == "call":
                # Challenge previous bid
                last_q, last_f = self.history[-1]
                total_count = self.count_dice(dice, last_f)
                if total_count >= last_q:
                    # Bid is correct → challenger wins
                    return current_player
                else:
                    # Bid is incorrect → challenger loses
                    return (current_player - 1) % self.num_players

            # Otherwise, action is a bid
            _, quantity, face = action
            if not self.legal_bid(quantity, face):
                # Illegal bid → current player loses immediately
                return (current_player - 1) % self.num_players

            self.history.append((quantity, face))
            current_player = (current_player + 1) % self.num_players
