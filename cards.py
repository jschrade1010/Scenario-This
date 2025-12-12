"""Card and Problem definitions for Supply Chain Strategy Card Game."""

from dataclasses import dataclass
from enum import Enum
from typing import List


class Difficulty(Enum):
    """Problem difficulty levels."""
    EASY = 1
    INTERMEDIATE = 2
    HARD = 3


@dataclass
class Answer:
    """Represents a possible answer to a problem."""
    text: str
    is_correct: bool
    explanation: str
    points_if_correct: int


@dataclass
class Card:
    """Represents a strategy problem card."""
    title: str
    description: str
    difficulty: Difficulty
    answers: List[Answer]
    category: str  # supply_chain, merchant_strategy, risk_management
    real_world_impact: str


# ============================================================================
# EASY CARDS (1-3 points per correct answer)
# ============================================================================

EASY_CARDS = [
    Card(
        title="Inventory Overstock Alert",
        description="Your warehouse is overstocked with winter inventory, but it's now spring. What do you do?",
        difficulty=Difficulty.EASY,
        category="supply_chain",
        real_world_impact="Prevents dead stock and frees up warehouse space",
        answers=[
            Answer(
                text="A) Reduce orders and run a clearance sale",
                is_correct=True,
                explanation="Smart move! Clearing overstock prevents losses and frees capital.",
                points_if_correct=3
            ),
            Answer(
                text="B) Keep inventory and hope it sells next season",
                is_correct=False,
                explanation="Risky! Storage costs add up and items may become obsolete.",
                points_if_correct=0
            ),
            Answer(
                text="C) Send all inventory to discount stores",
                is_correct=False,
                explanation="Too aggressive and damages brand value.",
                points_if_correct=0
            ),
            Answer(
                text="D) Donate it all for tax write-off",
                is_correct=False,
                explanation="Not efficient. Selling at a discount gets revenue.",
                points_if_correct=0
            ),
        ]
    ),
    Card(
        title="Supplier Shortage",
        description="Your main supplier just had a fire and can't deliver next month's order. What's your move?",
        difficulty=Difficulty.EASY,
        category="supply_chain",
        real_world_impact="Ensures business continuity and prevents stockouts",
        answers=[
            Answer(
                text="A) Immediately contact backup suppliers",
                is_correct=True,
                explanation="Correct! Always have backup suppliers for emergencies.",
                points_if_correct=3
            ),
            Answer(
                text="B) Hope they get back online quickly",
                is_correct=False,
                explanation="Too passive. You need a plan NOW.",
                points_if_correct=0
            ),
            Answer(
                text="C) Tell customers you're out of stock",
                is_correct=False,
                explanation="Loses customers to competitors.",
                points_if_correct=0
            ),
            Answer(
                text="D) Raise prices to reduce demand",
                is_correct=False,
                explanation="Damages customer relationships unnecessarily.",
                points_if_correct=0
            ),
        ]
    ),
    Card(
        title="Slow-Moving SKU",
        description="A product is barely selling despite good shelf placement. What action do you take?",
        difficulty=Difficulty.EASY,
        category="merchant_strategy",
        real_world_impact="Improves inventory turnover and cash flow",
        answers=[
            Answer(
                text="A) Analyze customer feedback and adjust pricing/marketing",
                is_correct=True,
                explanation="Smart! Data-driven decisions beat guessing.",
                points_if_correct=3
            ),
            Answer(
                text="B) Just keep it on shelves longer",
                is_correct=False,
                explanation="Wastes shelf space that could sell better items.",
                points_if_correct=0
            ),
            Answer(
                text="C) Remove it immediately",
                is_correct=False,
                explanation="Too hasty. Might just need better marketing.",
                points_if_correct=0
            ),
            Answer(
                text="D) Double the price",
                is_correct=False,
                explanation="That'll make it even slower! Bad move.",
                points_if_correct=0
            ),
        ]
    ),
    Card(
        title="Demand Surge",
        description="A viral TikTok just made your product blow up! Demand is 3x normal. What happens next?",
        difficulty=Difficulty.EASY,
        category="merchant_strategy",
        real_world_impact="Capitalizes on trending products and maximizes revenue",
        answers=[
            Answer(
                text="A) Quickly scale production and marketing",
                is_correct=True,
                explanation="Capitalize on the trend before it fades!",
                points_if_correct=3
            ),
            Answer(
                text="B) Do nothing and let it naturally cool off",
                is_correct=False,
                explanation="Missed opportunity for huge revenue!",
                points_if_correct=0
            ),
            Answer(
                text="C) Raise prices 50% to reduce demand",
                is_correct=False,
                explanation="Could work but might kill momentum and goodwill.",
                points_if_correct=0
            ),
            Answer(
                text="D) Only service existing customers",
                is_correct=False,
                explanation="Leaves money on the table.",
                points_if_correct=0
            ),
        ]
    ),
]


# ============================================================================
# INTERMEDIATE CARDS (4-6 points per correct answer)
# ============================================================================

INTERMEDIATE_CARDS = [
    Card(
        title="Sourcing Complexity",
        description="You can source from a cheap overseas supplier (15% cheaper) but shipping takes 6 weeks vs 2 weeks domestic. Your sales are unpredictable. Choose wisely.",
        difficulty=Difficulty.INTERMEDIATE,
        category="supply_chain",
        real_world_impact="Balances cost savings against demand responsiveness",
        answers=[
            Answer(
                text="A) Use blend: 60% domestic, 40% overseas based on demand forecasts",
                is_correct=True,
                explanation="Perfect balance! Cheap supply for predictable items, fast supply for volatile items.",
                points_if_correct=6
            ),
            Answer(
                text="B) Go 100% overseas (pure cost optimization)",
                is_correct=False,
                explanation="Risky. You'll stockout on trends and lose sales.",
                points_if_correct=0
            ),
            Answer(
                text="C) Stay 100% domestic for safety",
                is_correct=False,
                explanation="You're leaving 15% margin on the table long-term.",
                points_if_correct=2
            ),
            Answer(
                text="D) Switch suppliers based on gut feeling",
                is_correct=False,
                explanation="That's how companies go broke. Use data!",
                points_if_correct=0
            ),
        ]
    ),
    Card(
        title="Private Label Strategy",
        description="You want to develop a private label competitor to a bestselling brand. High margin but high risk. How do you validate the market first?",
        difficulty=Difficulty.INTERMEDIATE,
        category="merchant_strategy",
        real_world_impact="De-risks product development and maximizes ROI on new products",
        answers=[
            Answer(
                text="A) Run small test in 5 stores, gather data before full launch",
                is_correct=True,
                explanation="Smart MVP approach! Test, learn, scale.",
                points_if_correct=6
            ),
            Answer(
                text="B) Launch nationally to capture market share fast",
                is_correct=False,
                explanation="Huge risk. Could waste millions if it flops.",
                points_if_correct=0
            ),
            Answer(
                text="C) Survey customers about what they'd pay",
                is_correct=False,
                explanation="Customer surveys are notoriously inaccurate. Actual behavior matters.",
                points_if_correct=1
            ),
            Answer(
                text="D) Copy the brand exactly but cheaper",
                is_correct=False,
                explanation="That's infringement. Plus quality matters, not just price.",
                points_if_correct=0
            ),
        ]
    ),
    Card(
        title="Last-Mile Delivery Crisis",
        description="Your delivery costs jumped 40% due to fuel prices and labor shortage. Customer expectations are high. You have 3 options. Pick the best combo.",
        difficulty=Difficulty.INTERMEDIATE,
        category="supply_chain",
        real_world_impact="Optimizes logistics costs while maintaining service quality",
        answers=[
            Answer(
                text="A) Negotiate with carriers, optimize routes, offer slower shipping discount",
                is_correct=True,
                explanation="Multi-faceted approach. Address cost, efficiency, AND customer choice.",
                points_if_correct=6
            ),
            Answer(
                text="B) Just raise prices 40%",
                is_correct=False,
                explanation="Customers flee to competitors.",
                points_if_correct=0
            ),
            Answer(
                text="C) Cut delivery frequency and speed",
                is_correct=False,
                explanation="Customers hate slow delivery. They'll switch.",
                points_if_correct=1
            ),
            Answer(
                text="D) Build your own delivery fleet",
                is_correct=False,
                explanation="Huge capital cost and complexity. Not the short-term fix needed.",
                points_if_correct=0
            ),
        ]
    ),
    Card(
        title="Category Performance Divergence",
        description="Food category is booming (+25% YoY) but Electronics is flat (+1% YoY). You have limited marketing budget. How do you allocate?",
        difficulty=Difficulty.INTERMEDIATE,
        category="merchant_strategy",
        real_world_impact="Maximizes marketing ROI and portfolio growth",
        answers=[
            Answer(
                text="A) 70% to Food to capture growth, 30% to Electronics to stabilize",
                is_correct=True,
                explanation="Smart capital allocation. Ride the winners, defend the rest.",
                points_if_correct=6
            ),
            Answer(
                text="B) Split 50-50 to be fair",
                is_correct=False,
                explanation="That's not how portfolio management works. Back winners!",
                points_if_correct=2
            ),
            Answer(
                text="C) Put everything in Electronics to turn it around",
                is_correct=False,
                explanation="Starving a growing category is silly.",
                points_if_correct=0
            ),
            Answer(
                text="D) Cut both categories and invest in new categories",
                is_correct=False,
                explanation="You're leaving money on the table where customers are.",
                points_if_correct=0
            ),
        ]
    ),
]


# ============================================================================
# HARD CARDS (7-10 points per correct answer)
# ============================================================================

HARD_CARDS = [
    Card(
        title="Disruption: AI-Powered Competitive Entry",
        description="A well-funded startup with AI-driven supply chain optimization just entered your market. They're underpricing you 20% and growing fast. Your current cost structure can't match them. What's your multi-year strategy?",
        difficulty=Difficulty.HARD,
        category="strategy",
        real_world_impact="Determines long-term competitiveness and market survival",
        answers=[
            Answer(
                text="A) Invest in own AI/automation, differentiate on service, build moats (loyalty programs)",
                is_correct=True,
                explanation="This is how incumbents survive disruption. Match tech, compete on non-price dimensions, build switching costs.",
                points_if_correct=10
            ),
            Answer(
                text="B) Cut prices 25% to match them",
                is_correct=False,
                explanation="Margin death spiral. You can't beat them on cost alone.",
                points_if_correct=0
            ),
            Answer(
                text="C) Acquire the startup",
                is_correct=False,
                explanation="Could work but integration is hard. Maybe premature.",
                points_if_correct=4
            ),
            Answer(
                text="D) Exit the market segment",
                is_correct=False,
                explanation="Conceding without fighting? That's a business school case study of failure.",
                points_if_correct=0
            ),
        ]
    ),
    Card(
        title="Geographic Expansion Risk",
        description="You want to expand to 3 new countries. Market size potential is huge but regulatory risk, logistics complexity, and local competition vary widely. How do you prioritize and sequence the expansion?",
        difficulty=Difficulty.HARD,
        category="merchant_strategy",
        real_world_impact="Determines expansion success rate and capital efficiency",
        answers=[
            Answer(
                text="A) Score each by (market size × regulatory ease × competitive intensity), sequence by score",
                is_correct=True,
                explanation="Rigorous framework beats gut feel. Risk-adjusted market opportunity analysis.",
                points_if_correct=10
            ),
            Answer(
                text="B) Go to the biggest market first",
                is_correct=False,
                explanation="Size alone doesn't matter if regulatory/competitive barriers are brutal.",
                points_if_correct=2
            ),
            Answer(
                text="C) Start where competitors haven't gone yet",
                is_correct=False,
                explanation="Maybe those markets are small for a reason.",
                points_if_correct=3
            ),
            Answer(
                text="D) Simultaneous expansion to all 3",
                is_correct=False,
                explanation="Spreads your team and capital too thin. Sequential > simultaneous.",
                points_if_correct=0
            ),
        ]
    ),
    Card(
        title="Recession Playbook",
        description="Recession is coming (economists are signaling -2% GDP). Your business is counter-cyclical but margins are tight. How do you prepare operationally and strategically over the next 6-12 months?",
        difficulty=Difficulty.HARD,
        category="supply_chain",
        real_world_impact="Determines survival and relative market share gains in downturns",
        answers=[
            Answer(
                text="A) Reduce fixed costs, build cash reserves, prepare to acquire distressed competitors",
                is_correct=True,
                explanation="Recession playbook 101: De-lever, preserve cash, be ready to pounce on opportunities.",
                points_if_correct=10
            ),
            Answer(
                text="B) Invest heavily to gain market share now",
                is_correct=False,
                explanation="Wrong timing. You need dry powder for recession, not spending now.",
                points_if_correct=0
            ),
            Answer(
                text="C) Maintain status quo and hope it passes quickly",
                is_correct=False,
                explanation="Passive = death in recessions. Competitors will out-maneuver you.",
                points_if_correct=1
            ),
            Answer(
                text="D) Cut marketing and innovation spending drastically",
                is_correct=False,
                explanation="Some cutting yes, but too much and you exit recession weakened.",
                points_if_correct=3
            ),
        ]
    ),
    Card(
        title="Supply Chain Resilience Paradox",
        description="Having multiple suppliers = resilience but increases complexity and cost. Having one supplier = efficiency but fragile. You're a $5B company. How do you structure your supply base?",
        difficulty=Difficulty.HARD,
        category="supply_chain",
        real_world_impact="Balances efficiency gains against catastrophic risk mitigation",
        answers=[
            Answer(
                text="A) 70-30 split: primary supplier (economies of scale) + strategic backup (for critical items)",
                is_correct=True,
                explanation="Best of both worlds. Primary supplier keeps costs down, backup for critical risk mitigation.",
                points_if_correct=10
            ),
            Answer(
                text="B) Strict 50-50 to ensure zero single point of failure",
                is_correct=False,
                explanation="Loses economics of scale. Costs stay high.",
                points_if_correct=4
            ),
            Answer(
                text="C) One supplier for cost optimization",
                is_correct=False,
                explanation="One disruption (like COVID) destroys your business.",
                points_if_correct=0
            ),
            Answer(
                text="D) 5-6 suppliers to maximize optionality",
                is_correct=False,
                explanation="Unmanageable complexity and quality dilution.",
                points_if_correct=0
            ),
        ]
    ),
]


def get_all_cards():
    """Return all cards by difficulty."""
    return {
        Difficulty.EASY: EASY_CARDS,
        Difficulty.INTERMEDIATE: INTERMEDIATE_CARDS,
        Difficulty.HARD: HARD_CARDS,
    }