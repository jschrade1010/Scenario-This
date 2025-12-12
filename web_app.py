"""Flask web app for Supply Chain Strategy Card Game."""

from flask import Flask, render_template, request, jsonify, session
from game_engine import GameEngine, RankingSystem
from cards import Difficulty
import os
import json

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Global ranking system (in-memory)
ranking_system = RankingSystem()

# Store active games (in-memory)
active_games = {}


@app.route('/')
def index():
    """Serve the main game page."""
    return render_template('index.html')


@app.route('/api/start-game', methods=['POST'])
def start_game():
    """Start a new game for a player."""
    data = request.get_json()
    player_name = data.get('player_name', 'Anonymous')
    
    if not player_name:
        return jsonify({'error': 'Player name required'}), 400
    
    # Create a unique game ID (simplified - in production use UUID)
    game_id = f"{player_name}_{len(active_games)}"
    
    # Initialize game
    game = GameEngine(player_name)
    active_games[game_id] = game
    
    return jsonify({
        'game_id': game_id,
        'player_name': player_name,
        'message': f'Welcome, {player_name}!'
    })


@app.route('/api/draw-card/<game_id>/<difficulty>', methods=['POST'])
def draw_card(game_id, difficulty):
    """Draw a card for a specific game."""
    if game_id not in active_games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = active_games[game_id]
    
    # Parse difficulty
    difficulty_map = {
        'easy': Difficulty.EASY,
        'intermediate': Difficulty.INTERMEDIATE,
        'hard': Difficulty.HARD,
    }
    
    diff = difficulty_map.get(difficulty.lower())
    if not diff:
        return jsonify({'error': 'Invalid difficulty'}), 400
    
    # Draw card
    card = game.draw_card(diff)
    
    return jsonify({
        'card_id': card.title,
        'title': card.title,
        'description': card.description,
        'category': card.category,
        'difficulty': difficulty.upper(),
        'impact': card.real_world_impact,
        'answers': [
            {'id': i, 'text': ans.text}
            for i, ans in enumerate(card.answers)
        ],
        'cards_played': game.cards_played,
    })


@app.route('/api/answer/<game_id>', methods=['POST'])
def submit_answer(game_id):
    """Submit an answer to the current card."""
    if game_id not in active_games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = active_games[game_id]
    data = request.get_json()
    answer_index = data.get('answer_index')
    
    if answer_index is None:
        return jsonify({'error': 'Answer required'}), 400
    
    # Process answer
    is_correct, points, explanation = game.answer_question(answer_index)
    
    # Get current stats
    stats = game.get_game_stats()
    
    return jsonify({
        'is_correct': is_correct,
        'points_earned': points,
        'explanation': explanation,
        'total_score': stats['total_score'],
        'accuracy': f"{stats['accuracy']:.1f}%",
        'cards_won': stats['cards_won'],
        'cards_played': stats['cards_played'],
        'streak_bonus': stats['streak_bonus'],
    })


@app.route('/api/stats/<game_id>', methods=['GET'])
def get_stats(game_id):
    """Get current game statistics."""
    if game_id not in active_games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = active_games[game_id]
    stats = game.get_game_stats()
    
    return jsonify({
        'player_name': stats['player_name'],
        'total_score': stats['total_score'],
        'cards_played': stats['cards_played'],
        'cards_won': stats['cards_won'],
        'accuracy': f"{stats['accuracy']:.1f}%",
        'easy_streak': stats['easy_streak'],
        'intermediate_streak': stats['intermediate_streak'],
        'hard_streak': stats['hard_streak'],
        'streak_bonus': stats['streak_bonus'],
    })


@app.route('/api/end-game/<game_id>', methods=['POST'])
def end_game(game_id):
    """End a game and record the score."""
    if game_id not in active_games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = active_games[game_id]
    final_stats = game.end_game()
    
    # Add to leaderboard
    ranking_system.add_player_score(
        final_stats['player_name'],
        final_stats['final_score'],
        final_stats['accuracy'],
        final_stats['cards_played']
    )
    
    # Get player rank
    rank = ranking_system.get_player_rank(final_stats['player_name'])
    
    # Clean up
    del active_games[game_id]
    
    return jsonify({
        'player_name': final_stats['player_name'],
        'final_score': final_stats['final_score'],
        'accuracy': f"{final_stats['accuracy']:.1f}%",
        'cards_played': final_stats['cards_played'],
        'cards_won': final_stats['cards_won'],
        'streak_bonus_applied': final_stats['streak_bonus_applied'],
        'rank': rank,
    })


@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get the leaderboard."""
    leaderboard = ranking_system.get_leaderboard(top_n=10)
    
    return jsonify({
        'leaderboard': [
            {
                'rank': rank,
                'name': player['name'],
                'score': player['score'],
                'accuracy': f"{player['accuracy']:.1f}%",
                'cards_played': player['cards_played'],
            }
            for rank, player in enumerate(leaderboard, 1)
        ]
    })


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'service': 'supply-chain-game'})


if __name__ == '__main__':
    # In production, use a real WSGI server
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))