res = requests.get(url, params=params, timeout=5)
url = "https://datasets-server.huggingface.co/search"
    clean_id = model_id.split("/")[-1]
    params = {
        "dataset": "open-llm-leaderboard/contents",
        "config": "default",
        "split": "train",
        "query": clean_id,
        "offset": 0,
        "length": 10
    }