import numpy as np
from tqdm import tqdm
import multiprocessing as mp
from multiprocessing import Pool
import os
import math

# Set parameters
n = 10000
trials = 100000
batch_size = 5000

def calculate_longest_run(sequence):
    """Calculate longest run of 1s in a sequence using NumPy operations."""
    current_run = 0
    max_run = 0
    for val in sequence:
        if val == 1:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 0
    return max_run

def process_batch(args):
    """Process a batch of sequences in parallel."""
    batch_size, n = args
    # Generate random sequences for this batch
    sequences = np.random.randint(0, 2, size=(batch_size, n))
    # Calculate longest runs for each sequence
    return [calculate_longest_run(seq) for seq in sequences]

def simulate_longest_runs():
    """Run the complete simulation with parallel processing."""
    # Get 80% of available CPU cores
    total_cores = mp.cpu_count()
    used_cores = max(1, math.floor(total_cores * 0.8))  # At least use 1 core
    print(f"Using {used_cores} out of {total_cores} CPU cores (80%)")
    
    # Calculate number of batches
    num_batches = (trials + batch_size - 1) // batch_size
    
    # Prepare batch arguments
    batch_args = []
    for batch in range(num_batches):
        current_batch_size = min(batch_size, trials - batch * batch_size)
        batch_args.append((current_batch_size, n))
    
    # Create a process pool and run simulations in parallel
    with Pool(used_cores) as pool:
        # Use tqdm to show progress
        all_results = []
        for batch_results in tqdm(
            pool.imap(process_batch, batch_args),
            total=num_batches,
            desc="Processing batches"
        ):
            all_results.extend(batch_results)
    
    return np.array(all_results[:trials])

if __name__ == '__main__':
    try:
        # Set random seed for reproducibility
        np.random.seed(42)
        
        print(f"Starting simulation...")
        results = simulate_longest_runs()
        
        # Calculate statistics
        values, counts = np.unique(results, return_counts=True)
        probabilities = counts / trials
        
        print("\n模拟次数:", trials)
        print("最长连续正面次数及概率:")
        for val, prob in zip(values, probabilities):
            print(f"最长连续正面次数 {val}: {prob:.6f}")
        
        max_prob_idx = np.argmax(counts)
        max_prob_run = values[max_prob_idx]
        print(f"\n当前概率最高的最长连续正面次数: {max_prob_run}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
