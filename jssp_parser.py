def parse_instance(filepath):
   
    with open(filepath, 'r') as f:
        lines = f.readlines()

   
    lines = [line.strip() for line in lines if line.strip()]

    
    first_line = lines[0].split()
    n = int(first_line[0]) 

    jobs = []

    
    for i in range(1, n + 1):
        numbers = list(map(int, lines[i].split()))
        operations = []
        
        for j in range(0, len(numbers), 2):
            machine = numbers[j]
            duration = numbers[j + 1]
            operations.append((machine, duration))
        jobs.append(operations)

    return n, m, jobs



if __name__ == "__main__":
    import sys

    
    filepath = "instances/cscmax_20_15_1.txt"

    n, m, jobs = parse_instance(filepath)

    print(f"Number of jobs (n): {n}")
    print(f"Number of machines (m): {m}")
    print(f"\nFirst job operations (machine, duration):")
    for idx, (machine, duration) in enumerate(jobs[0]):
        print(f"  Operation {idx + 1}: Machine {machine}, Duration {duration}")