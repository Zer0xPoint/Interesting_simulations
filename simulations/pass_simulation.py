import random, os
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

num_cores = os.cpu_count()
num_workers = max(1, int(num_cores * 0.8))

def pass_ball(n_passes):
    current_player = 'A'
    for _ in range(n_passes):
        if current_player == 'A':
            current_player = random.choice(['B', 'C'])
        elif current_player == 'B':
            current_player = random.choice(['A', 'C'])
        else:  # current_player == 'C'
            current_player = random.choice(['A', 'B'])
    return current_player

def run_batch(n_passes, n_simulations):
    results = []
    num_workers = 8  # Assuming you are using 8 cores
    simulations_per_worker = n_simulations // num_workers  # Ensure each worker runs a portion of the total simulations
    for i in range(simulations_per_worker):
        try:
            result = pass_ball(n_passes)
            results.append(result)
        except Exception as e:
            print(f"Error in pass_ball with n_passes={n_passes}: {e}")
    return results

def calculate_probability(n_passes, total_simulations, batch_size):

    
    total_results = []
    with tqdm(total=total_simulations, desc="Processing simulations") as pbar:
        for i in range(0, total_simulations, batch_size):
            with ProcessPoolExecutor(max_workers=num_workers) as executor:
                futures = [executor.submit(run_batch, n_passes, min(batch_size, total_simulations - i)) for _ in range(num_workers)]
                for future in as_completed(futures):
                    batch_results = future.result()
                    total_results.extend(batch_results)
                    pbar.update(len(batch_results))
    
    # Debugging: check the total number of results
    if len(total_results) != total_simulations:
        print(f"Warning: Total results count ({len(total_results)}) does not match total_simulations ({total_simulations})")
    
    # Debugging: check if counts add up
    count_A = total_results.count('A')
    count_B = total_results.count('B')
    count_C = total_results.count('C')
    
    if count_A + count_B + count_C != total_simulations:
        print("Warning: Counts do not add up to total_simulations", count_A + count_B + count_C)
    
    total_simulations = total_simulations  # Set total_simulations from input parameter

    prob_A = count_A / total_simulations
    prob_B = count_B / total_simulations
    prob_C = count_C / total_simulations
    
    print("Final Probability of returning to A after %d passes: %.4f" % (n_passes, prob_A))
    print("Final Probability of returning to B after %0d passes: %.4f" % (n_passes, prob_B))
    print("Final Probability of returning to C after %0d passes: %.4f" % (n_passes, prob_C))

if __name__ == '__main__':
    N_PASSES = 10
    TOTAL_SIMULATIONS = 100_000
    BATCH_SIZE = 5_000
    calculate_probability(N_PASSES, TOTAL_SIMULATIONS, BATCH_SIZE)
