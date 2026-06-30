import requests

response = requests.get("https://openrouter.ai/api/v1/models", timeout=12)
if response.status_code == 200:
    data = response.json()
    models = data.get("data", [])
    benchmark_arenas = set()
    benchmark_categories = set()
    models_with_benchmarks = []
    
    for m in models:
        bench = m.get("benchmarks")
        if bench:
            models_with_benchmarks.append(m["id"])
            for arena, details in bench.items():
                benchmark_arenas.add(arena)
                if isinstance(details, list):
                    for detail in details:
                        if isinstance(detail, dict) and "category" in detail:
                            benchmark_categories.add(detail["category"])
                        elif isinstance(detail, dict) and "name" in detail:
                            benchmark_categories.add(detail["name"])
                elif isinstance(details, dict):
                    for category in details.keys():
                        benchmark_categories.add(category)
                        
    print(f"Total models with benchmarks: {len(models_with_benchmarks)}")
    print(f"Arenas found: {list(benchmark_arenas)}")
    print(f"Categories found: {list(benchmark_categories)[:30]}...")
    if models_with_benchmarks:
        print(f"Example models with benchmarks: {models_with_benchmarks[:5]}")
        # Print the benchmark structure of the first model with benchmarks
        for m in models:
            if m["id"] == models_with_benchmarks[0]:
                import json
                print(f"\nBenchmark structure for {m['id']}:")
                print(json.dumps(m["benchmarks"], indent=2))
                break
else:
    print(f"Error: {response.status_code}")
