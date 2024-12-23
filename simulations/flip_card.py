import random
import multiprocessing as mp
import math
from multiprocessing import Pool
from tqdm import tqdm

# flipping 9 cards, filp 1-3 cards at a time 
# return the average number of flips to make all cards face up
# simulate 100000 times

def simulate(_):
    cards = [0] * 9  # 9张反面牌
    count = 0  # 操作次数
    while sum(cards) < 9:
        # 随机选择1到3张牌进行翻转
        num_to_flip = random.randint(1, 3)
        # 从所有牌中随机选择num_to_flip张牌
        to_flip = random.sample(range(9), num_to_flip)
        # 翻转选中的牌
        for idx in to_flip:
            cards[idx] = 1 - cards[idx]
        count += 1
    return count


if __name__ == '__main__':
    num_simulations = 100000  # 模拟次数
    total_cores = mp.cpu_count()
    num_processes = max(1, math.floor(total_cores * 0.8))  # At least use 1 core

    with Pool(processes=num_processes) as pool:
        results = []
        for result in tqdm(pool.imap(simulate, range(num_simulations)), total=num_simulations, desc="Processing simulations"):
            results.append(result)
    pool.close()
    pool.join()
        
    total_counts = sum(results)
    average_count = total_counts / num_simulations
    print("Average number of flips:", average_count)
