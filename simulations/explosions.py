import os
import random
from collections import Counter
import pandas as pd
import numpy as np
import multiprocessing as mp
from multiprocessing import Pool
from tqdm import tqdm
import math

# Set parameters
n = 10000
trials = 100000
batch_size = 5000

def simulate_explosion():
    t = 0
    exploded = False
    while not exploded:
        t += 1
        if random.random() < t / 100:
            exploded = True
        else:
            continue
    return t

def process_batch(args):
    batch_size = args
    return [simulate_explosion() for _ in range(batch_size)]

def simulate_explosions_parallel(num_trials):
    total_cores = mp.cpu_count()
    used_cores = max(1, math.floor(total_cores * 0.8))
    print(f"Using {used_cores} out of {total_cores} CPU cores (80%)")
    
    num_batches = (num_trials + batch_size - 1) // batch_size
    batch_args = []
    for batch in range(num_batches):
        current_batch_size = min(batch_size, num_trials - batch * batch_size)
        batch_args.append(current_batch_size)
    
    with Pool(used_cores) as pool:
        all_results = []
        for batch_results in tqdm(
            pool.imap(process_batch, batch_args),
            total=num_batches,
            desc="Processing batches"
        ):
            all_results.extend(batch_results)
    return np.array(all_results[:num_trials])

if __name__ == "__main__":
    try:
        # Set random seed for reproducibility
        np.random.seed(42)
        
        print(f"Starting simulation...")
        results = simulate_explosions_parallel(trials)
        
        # Calculate statistics
        values, counts = np.unique(results, return_counts=True)
        probabilities = counts / trials
        
        print("\n模拟次数:", trials)
        print("爆炸时间及概率:")
        for val, prob in zip(values, probabilities):
            print(f"爆炸时间 {val}: {prob:.6f}")
        
        max_prob_idx = np.argmax(counts)
        max_prob_run = values[max_prob_idx]
        print(f"\n当前概率最高的爆炸时间: {max_prob_run}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
