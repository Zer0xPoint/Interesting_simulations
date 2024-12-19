"""
Module for simulating passing in a game.
"""

import os
import random
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

NUM_CORES = os.cpu_count()
NUM_WORKERS = max(1, int(NUM_CORES * 0.8))


def pass_ball(num_passes):
    """
    Simulates passing the ball between players A, B, and C.
    """
    current_player = 'A'
    for _ in range(num_passes):
        if current_player == 'A':
            current_player = random.choice(['B', 'C'])
        elif current_player == 'B':
            current_player = random.choice(['A', 'C'])
        else:  # current_player == 'C'
            current_player = random.choice(['A', 'B'])
    return current_player


def run_batch(num_passes, num_simulations):
    """
    Runs a batch of simulations.
    """
    results = []
    simulations_per_worker = num_simulations // NUM_WORKERS  # Ensure each worker runs a portion of the total simulations
    for _ in range(simulations_per_worker):
        try:
            result = pass_ball(num_passes)
            results.append(result)
        except Exception as e:  # Catch specific exception
            print(f"Error in pass_ball with num_passes={num_passes}: {e}")
    return results


def calculate_probability(num_passes, total_simulations, batch_size):
    """
    Calculates the probabilities of returning to player A, B, or C after a number of passes.
    """
    total_results = []
    with tqdm(total=total_simulations, desc="Processing simulations") as pbar:
        for i in range(0, total_simulations, batch_size):
            with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
                futures = [executor.submit(run_batch, num_passes, min(batch_size, total_simulations - i)) for _ in range(NUM_WORKERS)]
                for future in as_completed(futures):
                    batch_results = future.result()
                    total_results.extend(batch_results)
                    pbar.update(len(batch_results))
    
    # Debugging: check the total number of results
    if len(total_results) != total_simulations:
        print(f"Warning: Total results count ({len(total_results)}) does not match total_simulations ({total_simulations})")
    
    # Debugging: check if counts add up
    count_a = total_results.count('A')
    count_b = total_results.count('B')
    count_c = total_results.count('C')
    
    if count_a + count_b + count_c != total_simulations:
        print("Warning: Counts do not add up to total_simulations", count_a + count_b + count_c)
    
    prob_a = count_a / total_simulations
    prob_b = count_b / total_simulations
    prob_c = count_c / total_simulations
    
    print(f"Final Probability of returning to A after {num_passes} passes: {prob_a:.4f}")
    print(f"Final Probability of returning to B after {num_passes} passes: {prob_b:.4f}")
    print(f"Final Probability of returning to C after {num_passes} passes: {prob_c:.4f}")

if __name__ == '__main__':
    N_PASSES = 10
    TOTAL_SIMULATIONS = 100_000
    BATCH_SIZE = 5_000
    calculate_probability(N_PASSES, TOTAL_SIMULATIONS, BATCH_SIZE)
