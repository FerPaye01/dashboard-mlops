import os
import sys
sys.path.insert(0, os.getcwd())

from huggingface_hub import HfApi
import json

api = HfApi()
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
try:
    info = api.model_info(model_id)
    print(f"Model: {model_id}")
    print(f"Card Data: {type(info.card_data)}")
    if info.card_data:
        card_dict = info.card_data.to_dict()
        print("Card Data Keys:", list(card_dict.keys()))
        # Print results or metrics if they exist
        if "model-index" in card_dict:
            print("\nModel Index found!")
            print(json.dumps(card_dict["model-index"][:2], indent=2))
        elif "evaluations" in card_dict:
            print("\nEvaluations found!")
            print(json.dumps(card_dict["evaluations"], indent=2))
        elif "metrics" in card_dict:
            print("\nMetrics found!")
            print(json.dumps(card_dict["metrics"], indent=2))
        else:
            # Print first 20 keys and values of card_dict
            print("\nFull Card Data sample:")
            sample = {k: card_dict[k] for k in list(card_dict.keys())[:10]}
            print(json.dumps(sample, indent=2))
except Exception as e:
    print(f"Error: {e}")
