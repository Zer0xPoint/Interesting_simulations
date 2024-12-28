# Interesting Simulations

A collection of interesting mathematical and scientific simulations implemented in Python.

## Simulations

### 1. Longest Run of Heads
Simulates coin flips and calculates the probability distribution of the longest run of consecutive heads. Uses parallel processing for efficient computation.

### 2. Explosions
Models the probability distribution of when an explosion occurs, with the probability increasing over time.

### 3. Pass Simulation
Simulates passing a ball between three players to calculate the probability of which player ends up with the ball after a series of passes.

### 4. Flip Card
Calculates the average number of flips needed to turn all 9 cards face up, where 1-3 random cards are flipped each time.

### 5. Birthday Paradox
Simulates groups of random birthdays to calculate the probability of shared birthdays in groups of different sizes.

#### Requirements
- Python 3.x
- NumPy
- tqdm

#### Usage
```bash
python simulations/coin_flip_runs.py
python simulations/explosions.py
python simulations/pass_simulation.py
python simulations/flip_card.py
python simulations/birthday_paradox.py
```

## Project Structure
```
.
├── README.md
├── requirements.txt
└── simulations/
    ├── coin_flip_runs.py
    ├── explosions.py
    ├── pass_simulation.py
    ├── flip_card.py
    └── birthday_paradox.py
```

## Installation
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Contributing
Feel free to add more interesting simulations to this collection!
