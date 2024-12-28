import random
import multiprocessing as mp
import math
from multiprocessing import Pool
from tqdm import tqdm

def simulate_birthday(group_size):
    """Simulate birthdays for a group and check for duplicates."""
    birthdays = [random.randint(1, 365) for _ in range(group_size)]
    return len(birthdays) != len(set(birthdays))

def process_batch(args):
    """Process a batch of simulations in parallel."""
    batch_size, group_size = args
    return [simulate_birthday(group_size) for _ in range(batch_size)]

def run_simulation(group_size, num_trials=100000):
    """Run the complete simulation with parallel processing."""
    total_cores = mp.cpu_count()
    used_cores = max(1, math.floor(total_cores * 0.8))
    print(f"Using {used_cores} out of {total_cores} CPU cores (80%)")
    
    batch_size = 5000
    num_batches = (num_trials + batch_size - 1) // batch_size
    batch_args = [(min(batch_size, num_trials - batch * batch_size), group_size) 
                 for batch in range(num_batches)]
    
    with Pool(used_cores) as pool:
        all_results = []
        for batch_results in tqdm(
            pool.imap(process_batch, batch_args),
            total=num_batches,
            desc="Processing batches"
        ):
            all_results.extend(batch_results)
    
    probability = sum(all_results) / num_trials
    return probability

if __name__ == "__main__":
    try:
        # Set random seed for reproducibility
        random.seed(42)
        
        # Test group sizes from 2 to 60
        results = {}
        for group_size in range(2, 61):
            print(f"\nSimulating group size: {group_size}")
            prob = run_simulation(group_size)
            results[group_size] = prob
            print(f"Probability of shared birthday: {prob:.4f}")
        
        # Find the group size where probability crosses 50%
        for group_size, prob in results.items():
            if prob >= 0.5:
                print(f"\nGroup size where probability first exceeds 50%: {group_size}")
                break

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
