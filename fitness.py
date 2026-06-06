def calculate_makespan(permutation, jobs, n, m):
   


    job_op_index = [0] * n

    
    job_ready_time = [0] * n

    
    machine_ready_time = [0] * m

    
    for job_id in permutation:

        
        op_index = job_op_index[job_id]

       
        machine, duration = jobs[job_id][op_index]

        
        start_time = max(job_ready_time[job_id], machine_ready_time[machine])

        
        end_time = start_time + duration

        
        job_ready_time[job_id] = end_time
        machine_ready_time[machine] = end_time

        
        job_op_index[job_id] += 1

   
    makespan = max(job_ready_time)
    return makespan


def create_initial_solution(n, m):
   
    import random

    
    permutation = []
    for job_id in range(n):
        permutation.extend([job_id] * m)

    
    random.shuffle(permutation)
    return permutation



if __name__ == "__main__":
    import random
    from jssp_parser import parse_instance

    random.seed(42)

    filepath = "instances/cscmax_20_15_1.txt"
    n, m, jobs = parse_instance(filepath)

    
    permutation = create_initial_solution(n, m)

    print(f"Permutation length: {len(permutation)} (should be {n * m} = {n}x{m})")
    print(f"Sample of permutation: {permutation[:20]}...")

    
    makespan = calculate_makespan(permutation, jobs, n, m)
    print(f"\nMakespan of random solution: {makespan}")
   