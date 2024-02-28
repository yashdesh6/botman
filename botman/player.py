import random
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot

class Player(Bot):
    def __init__(self):
        pass

    def handle_new_round(self, game_state, round_state, active):
        pass

    def handle_round_over(self, game_state, terminal_state, active):
        pass

    def get_action(self, game_state, round_state, active):
        legal_actions = round_state.legal_actions()
        my_hand = round_state.hands[active]
        community_cards = round_state.community_cards if hasattr(round_state, 'community_cards') else []

        hand_strength = self.evaluate_hand_strength(my_hand + community_cards)

        if CheckAction in legal_actions:
            # Prefer to check if possible to stay in the game without additional cost.
            return CheckAction()
        elif RaiseAction in legal_actions and hand_strength >= 3:
            # Raise only with a strong hand (e.g., a pair or better in this simplistic evaluation).
            return RaiseAction(min(round_state.raise_bounds()[1], 100))  # Raise by 100 or max allowed
        elif CallAction in legal_actions and hand_strength >= 2:
            # Call with a decent hand (at least a high card by this evaluation's standards).
            return CallAction()
        return FoldAction()  # Fold as a last resort if the hand is really weak.

    def evaluate_hand_strength(self, cards):
        """Evaluate the hand strength based on a very simple heuristic."""
        rank_counts = {rank: 0 for rank in '23456789TJQKA'}
        for card in cards:
            rank_counts[card[0]] += 1
        
        score = 0
        for count in rank_counts.values():
            if count == 2:
                score += 2  # Pair
            elif count == 3:
                score += 6  # Three-of-a-kind
            elif count == 4:
                score += 12  # Four-of-a-kind

        # Consider high cards as a minimal strength
        high_cards = sum(1 for rank, count in rank_counts.items() if count == 1 and rank in 'TJQKA')
        score += high_cards * 0.5  # Slight increase for high cards

        return score

if __name__ == '__main__':
    run_bot(Player(), parse_args())
