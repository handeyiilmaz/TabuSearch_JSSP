import random
import time
import statistics
import os
from jssp_parser import parse_instance
from tabu_search import tabu_search


INSTANCES = [
    # Set A: 20-Job Instances
    ("Dmu01", "instances/rcmax_20_15_4.txt",  "20x15", "rcmax"),
    ("Dmu02", "instances/rcmax_20_15_10.txt", "20x15", "rcmax"),
    ("Dmu03", "instances/rcmax_20_15_5.txt",  "20x15", "rcmax"),
    ("Dmu04", "instances/rcmax_20_15_8.txt",  "20x15", "rcmax"),
    ("Dmu05", "instances/rcmax_20_15_1.txt",  "20x15", "rcmax"),
    ("Dmu06", "instances/rcmax_20_20_6.txt",  "20x20", "rcmax"),
    ("Dmu07", "instances/rcmax_20_20_4.txt",  "20x20", "rcmax"),
    ("Dmu08", "instances/rcmax_20_20_7.txt",  "20x20", "rcmax"),
    ("Dmu09", "instances/rcmax_20_20_8.txt",  "20x20", "rcmax"),
    ("Dmu10", "instances/rcmax_20_20_5.txt",  "20x20", "rcmax"),

    # Set B: 30-Job Instances (rcmax)
    ("Dmu11", "instances/rcmax_30_15_9.txt",  "30x15", "rcmax"),
    ("Dmu12", "instances/rcmax_30_15_10.txt", "30x15", "rcmax"),
    ("Dmu13", "instances/rcmax_30_15_5.txt",  "30x15", "rcmax"),
    ("Dmu14", "instances/rcmax_30_15_4.txt",  "30x15", "rcmax"),
    ("Dmu15", "instances/rcmax_30_15_1.txt",  "30x15", "rcmax"),
    ("Dmu16", "instances/rcmax_30_20_7.txt",  "30x20", "rcmax"),
    ("Dmu17", "instances/rcmax_30_20_10.txt", "30x20", "rcmax"),
    ("Dmu18", "instances/rcmax_30_20_9.txt",  "30x20", "rcmax"),
    ("Dmu19", "instances/rcmax_30_20_8.txt",  "30x20", "rcmax"),
    ("Dmu20", "instances/rcmax_30_20_2.txt",  "30x20", "rcmax"),

    # Set C: 30-Job Instances (cscmax)
    ("Dmu51", "instances/cscmax_30_15_2.txt", "30x15", "cscmax"),
    ("Dmu52", "instances/cscmax_30_15_9.txt", "30x15", "cscmax"),
    ("Dmu53", "instances/cscmax_30_15_10.txt","30x15", "cscmax"),
    ("Dmu54", "instances/cscmax_30_15_5.txt", "30x15", "cscmax"),
    ("Dmu55", "instances/cscmax_30_15_6.txt", "30x15", "cscmax"),
    ("Dmu56", "instances/cscmax_30_20_9.txt", "30x20", "cscmax"),
    ("Dmu57", "instances/cscmax_30_20_7.txt", "30x20", "cscmax"),
    ("Dmu58", "instances/cscmax_30_20_3.txt", "30x20", "cscmax"),
    ("Dmu59", "instances/cscmax_30_20_6.txt", "30x20", "cscmax"),
    ("Dmu60", "instances/cscmax_30_20_4.txt", "30x20", "cscmax"),
]


SEEDS = [42, 123, 456, 789, 1011]


MAX_ITERATIONS = 1000
TABU_TENURE = 10


def run_experiments():
    print("=" * 75)
    print("TABU SEARCH EXPERIMENTS - JSSP (Demirkol Benchmark)")
    print(f"Parameters: max_iterations={MAX_ITERATIONS}, tabu_tenure={TABU_TENURE}")
    print(f"Runs per instance: {len(SEEDS)} (seeds: {SEEDS})")
    print("=" * 75)

    results = []

    for instance_id, filepath, size, itype in INSTANCES:

        
        if not os.path.exists(filepath):
            print(f"[SKIP] {instance_id} — file not found: {filepath}")
            results.append({
                "id": instance_id,
                "size": size,
                "type": itype,
                "skipped": True
            })
            continue

       
        n, m, jobs = parse_instance(filepath)

        print(f"\nRunning {instance_id} ({size}, {itype})...")

        makespans = []
        times = []

        for seed in SEEDS:
            _, best_ms, _, elapsed = tabu_search(
                n, m, jobs,
                max_iterations=MAX_ITERATIONS,
                tabu_tenure=TABU_TENURE,
                seed=seed
            )
            makespans.append(best_ms)
            times.append(elapsed)
            print(f"  Seed {seed:4d} -> Makespan: {best_ms}, Time: {elapsed:.3f}s")

        
        mean_obj  = round(statistics.mean(makespans), 2)
        best_obj  = min(makespans)
        std_dev   = round(statistics.stdev(makespans), 2)
        mean_time = round(statistics.mean(times), 3)
        best_time = round(min(times), 3)

        print(f"  → Mean: {mean_obj}, Best: {best_obj}, "
              f"Std: {std_dev}, AvgTime: {mean_time}s, BestTime: {best_time}s")

        results.append({
            "id":        instance_id,
            "size":      size,
            "type":      itype,
            "mean_obj":  mean_obj,
            "best_obj":  best_obj,
            "std_dev":   std_dev,
            "mean_time": mean_time,
            "best_time": best_time,
            "skipped":   False
        })

    
    print("\n")
    print("=" * 75)
    print("FINAL RESULTS TABLE (Section 6.2)")
    print("=" * 75)
    print(f"{'Instance':<10} {'Size':<8} {'Type':<8} "
          f"{'Mean Obj':>10} {'Best Obj':>10} {'Std Dev':>9} "
          f"{'Mean Time':>11} {'Best Time':>11}")
    print("-" * 75)

    for r in results:
        if r["skipped"]:
            print(f"{r['id']:<10} {r['size']:<8} {r['type']:<8} {'FILE NOT FOUND':>42}")
        else:
            print(f"{r['id']:<10} {r['size']:<8} {r['type']:<8} "
                  f"{r['mean_obj']:>10} {r['best_obj']:>10} {r['std_dev']:>9} "
                  f"{r['mean_time']:>10}s {r['best_time']:>10}s")

    print("=" * 75)

   
    save_results(results)


def save_results(results):
    
    with open("results.txt", "w") as f:
        f.write("TABU SEARCH RESULTS - JSSP\n")
        f.write(f"Parameters: max_iterations={MAX_ITERATIONS}, "
                f"tabu_tenure={TABU_TENURE}\n")
        f.write(f"Seeds: {SEEDS}\n\n")
        f.write(f"{'Instance':<10} {'Size':<8} {'Type':<8} "
                f"{'Mean Obj':>10} {'Best Obj':>10} {'Std Dev':>9} "
                f"{'Mean Time':>11} {'Best Time':>11}\n")
        f.write("-" * 75 + "\n")
        for r in results:
            if r["skipped"]:
                f.write(f"{r['id']:<10} {r['size']:<8} {r['type']:<8} "
                        f"FILE NOT FOUND\n")
            else:
                f.write(f"{r['id']:<10} {r['size']:<8} {r['type']:<8} "
                        f"{r['mean_obj']:>10} {r['best_obj']:>10} "
                        f"{r['std_dev']:>9} "
                        f"{r['mean_time']:>10}s {r['best_time']:>10}s\n")
    print("\nResults saved to results.txt")


if __name__ == "__main__":
    run_experiments()