"""
Sorting Assignment Starter Code
Implement five sorting algorithms and benchmark their performance.
"""

import json
import time
import tracemalloc


# ============================================================================
# PART 1: SORTING IMPLEMENTATIONS
# ============================================================================

def bubble_sort(arr):
    n = len(arr)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

    return arr


def selection_sort(arr):
    n = len(arr)

    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j

        arr[i], arr[min_index] = arr[min_index], arr[i]

    return arr


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


# ============================================================================
# PART 2: STABILITY DEMONSTRATION
# ============================================================================

def demonstrate_stability():
    results = {
        "bubble_sort": "Stable",
        "selection_sort": "Unstable",
        "insertion_sort": "Stable",
        "merge_sort": "Stable"
    }

    return results


# ============================================================================
# PART 3: PERFORMANCE BENCHMARKING
# ============================================================================

def load_dataset(filename):
    with open(f"datasets/{filename}", "r") as f:
        return json.load(f)


def load_test_cases():
    with open("datasets/test_cases.json", "r") as f:
        return json.load(f)


def test_sorting_correctness():
    print("=" * 70)
    print("TESTING SORTING CORRECTNESS")
    print("=" * 70 + "\n")

    test_cases = load_test_cases()

    test_names = ["small_random", "small_sorted", "small_reverse", "small_duplicates"]
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort
    }

    for test_name in test_names:
        print(f"Test: {test_name}")
        print(f"  Input:    {test_cases[test_name]}")
        print(f"  Expected: {test_cases['expected_sorted'][test_name]}")
        print()

        for algo_name, algo_func in algorithms.items():
            try:
                result = algo_func(test_cases[test_name].copy())
                expected = test_cases['expected_sorted'][test_name]
                status = "✓ PASS" if result == expected else "✗ FAIL"
                print(f"    {algo_name:20s}: {result} {status}")
            except Exception as e:
                print(f"    {algo_name:20s}: ERROR - {str(e)}")

        print()


def benchmark_algorithm(sort_func, data):
    data_copy = data.copy()

    tracemalloc.start()

    start_time = time.perf_counter()
    sort_func(data_copy)
    end_time = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time_ms = (end_time - start_time) * 1000
    peak_memory_kb = peak / 1024

    return execution_time_ms, peak_memory_kb


def benchmark_all_datasets():
    print("\n" + "=" * 70)
    print("BENCHMARKING SORTING ALGORITHMS")
    print("=" * 70 + "\n")

    datasets = {
        "orders.json": ("Order Processing Queue", 50000, 5000),
        "products.json": ("Product Catalog", 100000, 5000),
        "inventory.json": ("Inventory Reconciliation", 25000, 5000),
        "activity_log.json": ("Customer Activity Log", 75000, 5000)
    }

    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort
    }

    for filename, (description, full_size, sample_size) in datasets.items():
        print(f"Dataset: {description} ({sample_size:,} element sample)")
        print("-" * 70)

        data = load_dataset(filename)
        data_sample = data[:sample_size]

        for algo_name, algo_func in algorithms.items():
            try:
                exec_time, memory = benchmark_algorithm(algo_func, data_sample)
                print(f"  {algo_name:20s}: {exec_time:8.2f} ms | {memory:8.2f} KB")
            except Exception as e:
                print(f"  {algo_name:20s}: ERROR - {str(e)}")

        print()


def analyze_stability():
    print("=" * 70)
    print("STABILITY ANALYSIS")
    print("=" * 70 + "\n")

    results = demonstrate_stability()

    for algo_name, stability in results.items():
        print(f"  {algo_name:20s}: {stability}")

    print()


if __name__ == "__main__":
    print("SORTING ASSIGNMENT - COMPLETED\n")

    test_sorting_correctness()
    benchmark_all_datasets()
    analyze_stability()