import random
import time
from jssp_parser import parse_instance
from fitness import calculate_makespan, create_initial_solution


def get_neighbors(permutation):
   
    neighbors = []
    n = len(permutation)

    num_swaps = 200

    seen = set()
    attempts = 0

    while len(neighbors) < num_swaps and attempts < num_swaps * 10:
        attempts += 1
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)

        
        if i != j and permutation[i] != permutation[j]:
            key = (min(i, j), max(i, j))
            if key not in seen:
                seen.add(key)
                new_perm = permutation[:]
                new_perm[i], new_perm[j] = new_perm[j], new_perm[i]
                neighbors.append((new_perm, (i, j)))

    return neighbors


def tabu_search(n, m, jobs, max_iterations=500, tabu_tenure=10, seed=42):
   

    random.seed(seed)

    # Initialization 
    current_solution = create_initial_solution(n, m)
    current_makespan = calculate_makespan(current_solution, jobs, n, m)

    best_solution = current_solution[:]
    best_makespan = current_makespan

   
    tabu_list = {}

    history = [best_makespan]
    no_improve_count = 0
    start_time = time.time()

    print(f"  Starting makespan: {current_makespan}")

    
    for iteration in range(max_iterations):

        
        neighbors = get_neighbors(current_solution)

        best_candidate = None
        best_candidate_makespan = float('inf')
        best_candidate_move = None

        
        for neighbor_perm, move in neighbors:
            neighbor_makespan = calculate_makespan(neighbor_perm, jobs, n, m)

            
            normalized_move = (min(move[0], move[1]), max(move[0], move[1]))
            is_tabu = normalized_move in tabu_list

            
            if not is_tabu or neighbor_makespan < best_makespan:
                if neighbor_makespan < best_candidate_makespan:
                    best_candidate = neighbor_perm
                    best_candidate_makespan = neighbor_makespan
                    best_candidate_move = normalized_move

        
        if best_candidate is None:
            continue

       
        current_solution = best_candidate
        current_makespan = best_candidate_makespan

        
        tabu_list[best_candidate_move] = tabu_tenure

        
        expired = [move for move, tenure in tabu_list.items() if tenure <= 1]
        for move in expired:
            del tabu_list[move]
        for move in tabu_list:
            tabu_list[move] -= 1

        
        if current_makespan < best_makespan:
            best_makespan = current_makespan
            best_solution = current_solution[:]
            no_improve_count = 0
        else:
            no_improve_count += 1

        history.append(best_makespan)

        
        if (iteration + 1) % 100 == 0:
            elapsed = time.time() - start_time
            print(f"  Iteration {iteration + 1}/{max_iterations} | "
                  f"Best makespan: {best_makespan} | "
                  f"Time: {elapsed:.2f}s")

       
        if no_improve_count >= 100:
            print(f"  Stopped early at iteration {iteration + 1} "
                  f"(no improvement for 100 iterations)")
            break

    elapsed = time.time() - start_time
    return best_solution, best_makespan, history, elapsed



if __name__ == "__main__":

    filepath = "instances/cscmax_20_15_1.txt"
    n, m, jobs = parse_instance(filepath)

    print("=" * 55)
    print("TABU SEARCH - JSSP")
    print(f"Instance: cscmax_20_15_1 ({n} jobs x {m} machines)")
    print("=" * 55)

    best_sol, best_ms, history, elapsed = tabu_search(
        n, m, jobs,
        max_iterations=1000,
        tabu_tenure=10,
        seed=42
    )

    print("=" * 55)
    print(f"  RESULT")
    print(f"  Best Makespan Found : {best_ms}")
    print(f"  Initial Makespan    : {history[0]}")
    print(f"  Improvement         : {history[0] - best_ms} "
          f"({((history[0] - best_ms) / history[0]) * 100:.1f}%)")
    print(f"  Total Time          : {elapsed:.3f} seconds")
    print("=" * 55)