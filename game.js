// Game state
let currentGameId = null;
let currentCard = null;
let isAnswered = false;

// API Base URL
const API_BASE = '/api';

// Screen management
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
    window.scrollTo(0, 0);
}

// Start a new game
function startGame() {
    const playerName = document.getElementById('player-name').value.trim();
    
    if (!playerName) {
        alert('Please enter your name!');
        return;
    }
    
    fetch(`${API_BASE}/start-game`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_name: playerName })
    })
    .then(response => response.json())
    .then(data => {
        currentGameId = data.game_id;
        document.getElementById('player-name-display').textContent = `Player: ${data.player_name}`;
        showScreen('game-screen');
        drawCard('easy');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to start game');
    });
}

// Draw a card
function drawCard(difficulty) {
    if (!currentGameId) return;
    
    fetch(`${API_BASE}/draw-card/${currentGameId}/${difficulty}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        currentCard = data;
        displayCard(data);
        isAnswered = false;
        document.getElementById('result-panel').classList.add('hidden');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to draw card');
    });
}

// Display card on screen
function displayCard(card) {
    // Set difficulty badge color
    const diffClass = card.difficulty.toLowerCase();
    document.getElementById('difficulty-badge').className = `difficulty ${diffClass}`;
    document.getElementById('difficulty-badge').textContent = card.difficulty;
    
    // Set card content
    document.getElementById('card-title').textContent = card.title;
    document.getElementById('card-description').textContent = card.description;
    document.getElementById('card-impact').textContent = card.impact;
    
    // Display answers
    const answersContainer = document.getElementById('answers-container');
    answersContainer.innerHTML = '';
    
    card.answers.forEach((answer, index) => {
        const btn = document.createElement('button');
        btn.className = 'answer-btn';
        btn.textContent = answer.text;
        btn.onclick = () => submitAnswer(index);
        answersContainer.appendChild(btn);
    });
    
    // Update stats
    updateStats();
}

// Submit an answer
function submitAnswer(answerIndex) {
    if (!currentGameId || isAnswered) return;
    
    // Disable all answer buttons
    document.querySelectorAll('.answer-btn').forEach(btn => {
        btn.disabled = true;
    });
    
    isAnswered = true;
    
    fetch(`${API_BASE}/answer/${currentGameId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answer_index: answerIndex })
    })
    .then(response => response.json())
    .then(data => {
        displayResult(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to submit answer');
    });
}

// Display result
function displayResult(result) {
    const resultPanel = document.getElementById('result-panel');
    const resultTitle = document.getElementById('result-title');
    const resultMessage = document.getElementById('result-message');
    const pointsEarned = document.getElementById('points-earned');
    const explanation = document.getElementById('result-explanation');
    
    if (result.is_correct) {
        resultPanel.classList.remove('incorrect');
        resultPanel.classList.add('correct');
        resultTitle.innerHTML = '🎉 CORRECT!';
        resultMessage.textContent = 'Great decision! You understand supply chain strategy.';
    } else {
        resultPanel.classList.remove('correct');
        resultPanel.classList.add('incorrect');
        resultTitle.innerHTML = '❌ Not Quite';
        resultMessage.textContent = 'Good try! Learn from this for next time.';
    }
    
    pointsEarned.textContent = result.points_earned;
    explanation.textContent = result.explanation;
    
    // Show result panel
    resultPanel.classList.remove('hidden');
    
    // Update stats display
    document.getElementById('score-display').textContent = result.total_score;
    document.getElementById('accuracy-display').textContent = result.accuracy;
}

// Go to next card
function nextCard() {
    const difficulty = prompt(
        'Choose difficulty for next card:\n1 = Easy\n2 = Intermediate\n3 = Hard',
        '1'
    );
    
    if (!difficulty) return;
    
    const diffMap = {
        '1': 'easy',
        '2': 'intermediate',
        '3': 'hard'
    };
    
    const selectedDifficulty = diffMap[difficulty];
    if (selectedDifficulty) {
        drawCard(selectedDifficulty);
    } else {
        alert('Invalid choice');
    }
}

// Update game stats
function updateStats() {
    if (!currentGameId) return;
    
    fetch(`${API_BASE}/stats/${currentGameId}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById('score-display').textContent = data.total_score;
        document.getElementById('accuracy-display').textContent = data.accuracy;
        document.getElementById('cards-display').textContent = data.cards_played;
    })
    .catch(error => console.error('Error updating stats:', error));
}

// Quit game
function quitGame() {
    if (!currentGameId) return;
    
    if (!confirm('Are you sure you want to quit? Your game will be recorded.')) {
        return;
    }
    
    fetch(`${API_BASE}/end-game/${currentGameId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        displayFinalResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to end game');
    });
}

// Display final results
function displayFinalResults(data) {
    document.getElementById('final-player-name').textContent = data.player_name;
    document.getElementById('final-score').textContent = data.final_score;
    document.getElementById('final-accuracy').textContent = data.accuracy;
    document.getElementById('final-cards').textContent = data.cards_played;
    document.getElementById('final-won').textContent = data.cards_won;
    document.getElementById('final-bonus').textContent = data.streak_bonus_applied;
    
    // Format rank
    const rankDisplay = document.getElementById('final-rank');
    if (data.rank) {
        const medals = ['🥇', '🥈', '🥉'];
        const medal = data.rank <= 3 ? medals[data.rank - 1] : '';
        rankDisplay.textContent = `${medal} #${data.rank}`;
    } else {
        rankDisplay.textContent = 'Unranked';
    }
    
    currentGameId = null;
    showScreen('results-screen');
}

// Show leaderboard
function showLeaderboard() {
    showScreen('leaderboard-screen');
    loadLeaderboard();
}

// Load leaderboard data
function loadLeaderboard() {
    fetch(`${API_BASE}/leaderboard`)
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('leaderboard-body');
        tbody.innerHTML = '';
        
        if (data.leaderboard.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="loading">No scores yet. Play a game!</td></tr>';
            return;
        }
        
        data.leaderboard.forEach(player => {
            const medals = ['🥇', '🥈', '🥉'];
            const medal = player.rank <= 3 ? medals[player.rank - 1] + ' ' : '';
            
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${medal}#${player.rank}</td>
                <td>${player.name}</td>
                <td>${player.score}</td>
                <td>${player.accuracy}</td>
                <td>${player.cards_played}</td>
            `;
        });
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('leaderboard-body').innerHTML = 
            '<tr><td colspan="5" class="loading">Failed to load leaderboard</td></tr>';
    });
}

// Show about/instructions
function showAbout() {
    showScreen('about-screen');
}

// Back to menu
function backToMenu() {
    currentGameId = null;
    currentCard = null;
    document.getElementById('player-name').value = '';
    showScreen('menu-screen');
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    showScreen('menu-screen');
    
    // Allow pressing Enter to start game
    document.getElementById('player-name').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            startGame();
        }
    });
});