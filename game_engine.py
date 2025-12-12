"""Game engine for Supply Chain Strategy Card Game."""

import random
from typing import Optional, Tuple
from cards import Card, Difficulty, get_all_cards


class GameEngine:
    """Main game logic and state management."""

    def __init__(self, player_name: str):
        """Initialize a new game session."""
        self.player_name = player_name
        self.score = 0
        self.cards_played = 0
        self.cards_won = 0
        self.current_card: Optional[Card] = None
        self.difficulty_streak = {Difficulty.EASY: 0, Difficulty.INTERMEDIATE: 0, Difficulty.HARD: 0}
        self.all_cards = get_all_cards()
        self.used_cards = set()

    def draw_card(self, difficulty: Difficulty) -> Card:
        """Draw a random card from the specified difficulty level."""
        available_cards = [
            card for card in self.all_cards[difficulty]
            if card.title not in self.used_cards
        ]

        if not available_cards:
            # Reset used cards for that difficulty if we've played them all
            available_cards = self.all_cards[difficulty]
            self.used_cards = {c.title for d in self.all_cards for c in self.all_cards[d]} - {
                c.title for c in available_cards
            }

        self.current_card = random.choice(available_cards)
        self.used_cards.add(self.current_card.title)
        self.cards_played += 1
        return self.current_card

    def answer_question(self, answer_index: int) -> Tuple[bool, int, str]:
        """Process player's answer to current card.

        Returns:
            (is_correct, points_earned, explanation)
        """
        if not self.current_card:
            return False, 0, "No card drawn yet!"

        if answer_index < 0 or answer_index >= len(self.current_card.answers):
            return False, 0, "Invalid answer selection."

        answer = self.current_card.answers[answer_index]

        if answer.is_correct:
            self.cards_won += 1
            points = answer.points_if_correct
            self.score += points
            self.difficulty_streak[self.current_card.difficulty] += 1
            return True, points, answer.explanation
        else:
            # Reset streak on wrong answer
            self.difficulty_streak[self.current_card.difficulty] = 0
            return False, 0, answer.explanation

    def get_streak_bonus(self) -> int:
        """Calculate bonus points for consecutive correct answers."""
        bonus = 0
        for difficulty, streak in self.difficulty_streak.items():
            if streak >= 3:
                # Bonus increases with difficulty
                bonus_multiplier = {
                    Difficulty.EASY: 1,
                    Difficulty.INTERMEDIATE: 2,
                    Difficulty.HARD: 5,
                }
                bonus += (streak - 2) * bonus_multiplier[difficulty]
        return bonus

    def apply_streak_bonus(self):
        """Apply streak bonus to total score."""
        bonus = self.get_streak_bonus()
        self.score += bonus
        return bonus

    def get_accuracy(self) -> float:
        """Get accuracy percentage."""
        if self.cards_played == 0:
            return 0.0
        return (self.cards_won / self.cards_played) * 100

    def get_game_stats(self) -> dict:
        """Get current game statistics."""
        return {
            "player_name": self.player_name,
            "total_score": self.score,
            "cards_played": self.cards_played,
            "cards_won": self.cards_won,
            "accuracy": self.get_accuracy(),
            "easy_streak": self.difficulty_streak[Difficulty.EASY],
            "intermediate_streak": self.difficulty_streak[Difficulty.INTERMEDIATE],
            "hard_streak": self.difficulty_streak[Difficulty.HARD],
            "streak_bonus": self.get_streak_bonus(),
        }

    def end_game(self) -> dict:
        """End the game and return final stats."""
        bonus = self.apply_streak_bonus()
        return {
            **self.get_game_stats(),
            "streak_bonus_applied": bonus,
            "final_score": self.score,
        }


class RankingSystem:
    """Manages player rankings and leaderboard."""

    def __init__(self):
        """Initialize ranking system."""
        self.players = []

    def add_player_score(self, player_name: str, score: int, accuracy: float, cards_played: int):
        """Add a player score to the rankings."""
        self.players.append({
            "name": player_name,
            "score": score,
            "accuracy": accuracy,
            "cards_played": cards_played,
        })

    def get_leaderboard(self, top_n: int = 10) -> list:
        """Get top N players by score."""
        sorted_players = sorted(
            self.players,
            key=lambda x: (x["score"], x["accuracy"], x["cards_played"]),
            reverse=True
        )
        return sorted_players[:top_n]

    def get_player_rank(self, player_name: str) -> Optional[int]:
        """Get a player's rank."""
        sorted_players = sorted(
            self.players,
            key=lambda x: (x["score"], x["accuracy"]),
            reverse=True
        )
        for rank, player in enumerate(sorted_players, 1):
            if player["name"].lower() == player_name.lower():
                return rank
        return None