import os
import asyncio
import httpx
import pandas as pd
from datasets import load_dataset
import re

class LLMDataIngester:
    def __init__(self):
        self.openrouter_url = "https://openrouter.ai/api/v1/models"
        self.artificial_analysis_url = "https://artificialanalysis.ai/api/v2/language/models"
        self.cache_file = os.path.join(os.path.dirname(__file__), "local_metrics_cache.json")

    async def fetch_openrouter(self, client: httpx.AsyncClient) -> list:
        try:
            print("Fetching OpenRouter models...")
            response = await client.get(self.openrouter_url, timeout=15)
            response.raise_for_status()
            data = response.json()
            models = []
            for item in data.get("data", []):
                pricing = item.get("pricing", {})
                prompt_cost = float(pricing.get("prompt", 0)) * 1_000_000
                completion_cost = float(pricing.get("completion", 0)) * 1_000_000
                
                models.append({
                    "model_id": item.get("id"),
                    "name": item.get("name", item.get("id")),
                    "context_length": item.get("context_length", 8000),
                    "cost_input_per_m": prompt_cost,
                    "cost_output_per_m": completion_cost,
                    "hosting": "Solo Cloud (APIs / OpenRouter)"
                })
            print(f"OpenRouter returned {len(models)} models.")
            return models
        except Exception as e:
            print(f"Error fetching OpenRouter: {e}")
            return []

    async def fetch_artificial_analysis(self, client: httpx.AsyncClient) -> list:
        api_key = os.getenv("ARTIFICIAL_ANALYSIS_API_KEY")
        if not api_key:
            print("No Artificial Analysis API key found in env. Skipping API call.")
            return []
        headers = {"x-api-key": api_key}
        try:
            print("Fetching Artificial Analysis models...")
            response = await client.get(self.artificial_analysis_url, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            models_list = []
            if isinstance(data, list):
                models_list = data
            elif isinstance(data, dict):
                for k in ["data", "models", "results"]:
                    if k in data and isinstance(data[k], list):
                        models_list = data[k]
                        break
                if not models_list:
                    for k, v in data.items():
                        if isinstance(v, dict) and "performance" in v:
                            v["model_id"] = k
                            models_list.append(v)
                            
            parsed = []
            for item in models_list:
                model_id = item.get("id") or item.get("model") or item.get("model_id") or item.get("name")
                perf = item.get("performance", {})
                ttft = perf.get("time_to_first_token")
                tps = perf.get("tokens_per_second")
                
                if ttft is not None:
                    ttft = float(ttft)
                    if ttft < 10.0:
                        ttft = ttft * 1000.0
                
                parsed.append({
                    "model_id": model_id,
                    "tps": float(tps) if tps is not None else None,
                    "ttft_ms": float(ttft) if ttft is not None else None
                })
            print(f"Artificial Analysis returned {len(parsed)} models.")
            return parsed
        except Exception as e:
            print(f"Error fetching Artificial Analysis: {e}")
            return []

    async def fetch_huggingface_leaderboard(self) -> pd.DataFrame:
        try:
            print("Fetching Hugging Face leaderboard...")
            dataset = await asyncio.to_thread(
                load_dataset, 'open-llm-leaderboard/contents', split='train'
            )
            df = dataset.to_pandas()
            col_map = {
                "fullname": "model_id",
                "IFEval": "ifeval",
                "MMLU-PRO": "mmlu",
                "GPQA": "gpqa",
                "#Params (B)": "parameters_b"
            }
            existing_cols = {k: v for k, v in col_map.items() if k in df.columns}
            df_subset = df[list(existing_cols.keys())].rename(columns=existing_cols)
            print(f"Hugging Face leaderboard returned {len(df_subset)} models.")
            return df_subset
        except Exception as e:
            print(f"Error fetching Hugging Face Leaderboard: {e}")
            return pd.DataFrame()

    async def ingest_live(self) -> pd.DataFrame:
        async with httpx.AsyncClient(verify=True) as client:
            or_task = self.fetch_openrouter(client)
            aa_task = self.fetch_artificial_analysis(client)
            hf_task = self.fetch_huggingface_leaderboard()
            
            or_data, aa_data, hf_df = await asyncio.gather(or_task, aa_task, hf_task)
            
        if not or_data and hf_df.empty:
            print("No data fetched from live APIs.")
            return pd.DataFrame()
            
        or_df = pd.DataFrame(or_data) if or_data else pd.DataFrame(columns=["model_id", "name", "context_length", "cost_input_per_m", "cost_output_per_m", "hosting"])
        aa_df = pd.DataFrame(aa_data) if aa_data else pd.DataFrame(columns=["model_id", "tps", "ttft_ms"])
        
        def normalize_id(mid):
            if not isinstance(mid, str):
                return ""
            return mid.lower().strip().replace("_", "-")
            
        if not or_df.empty:
            or_df["norm_id"] = or_df["model_id"].apply(normalize_id)
        else:
            or_df["norm_id"] = ""
            
        if not hf_df.empty:
            hf_df["norm_id"] = hf_df["model_id"].apply(normalize_id)
        else:
            hf_df["norm_id"] = ""
            
        if not aa_df.empty:
            aa_df["norm_id"] = aa_df["model_id"].apply(normalize_id)
        else:
            aa_df["norm_id"] = ""
            
        merged_records = {}
        
        if not hf_df.empty:
            for _, row in hf_df.iterrows():
                mid = row["model_id"]
                norm = row["norm_id"]
                params = row.get("parameters_b")
                
                params_b = float(params) if params is not None and not pd.isna(params) else self.extract_params_from_id(mid)
                
                attention_type = "GQA"
                if "deepseek" in mid.lower():
                    attention_type = "MLA"
                elif "gpt" in mid.lower() or "claude" in mid.lower() or "mpt" in mid.lower():
                    attention_type = "MHA"
                    
                layers = 32 if params_b < 15 else (40 if params_b < 35 else 80)
                hidden_size = 4096 if params_b < 15 else (5120 if params_b < 35 else 8192)
                num_heads = 32 if params_b < 15 else (40 if params_b < 35 else 64)
                num_kv_heads = 8
                
                merged_records[norm] = {
                    "model_id": mid,
                    "name": f"Local: {mid.split('/')[-1].replace('-', ' ').title()}",
                    "parameters_b": params_b,
                    "layers": layers,
                    "hidden_size": hidden_size,
                    "num_heads": num_heads,
                    "num_kv_heads": num_kv_heads,
                    "attention_type": attention_type,
                    "hosting": "Solo Local (Privado / GGUF)",
                    "native_context": 128000 if "qwen" in mid.lower() else (32000 if "mistral" in mid.lower() else 8000),
                    "speed_local": round(80.0 / (params_b ** 0.5), 1) if params_b > 0 else 50.0,
                    "speed_cloud": 0.0,
                    "ttft_ms": 120 + int(params_b * 4),
                    "cost_input_per_m": 0.0,
                    "cost_output_per_m": 0.0,
                    "format": "Local",
                    "ifeval": float(row.get("ifeval")) if row.get("ifeval") is not None and not pd.isna(row.get("ifeval")) else None,
                    "mmlu": float(row.get("mmlu")) if row.get("mmlu") is not None and not pd.isna(row.get("mmlu")) else None,
                    "gpqa": float(row.get("gpqa")) if row.get("gpqa") is not None and not pd.isna(row.get("gpqa")) else None,
                    "benchmarks_verificados": True
                }

        if not or_df.empty:
            for _, row in or_df.iterrows():
                mid = row["model_id"]
                norm = row["norm_id"]
                
                ifeval = None
                mmlu = None
                gpqa = None
                bench_verified = False
                
                hf_match = None
                if norm in merged_records:
                    hf_match = merged_records[norm]
                else:
                    for k, v in merged_records.items():
                        if k in norm or norm in k:
                            hf_match = v
                            break
                            
                if hf_match:
                    ifeval = hf_match["ifeval"]
                    mmlu = hf_match["mmlu"]
                    gpqa = hf_match["gpqa"]
                    bench_verified = True
                    
                params_b = self.extract_params_from_id(mid)
                attention_type = "GQA"
                if "deepseek" in mid.lower():
                    attention_type = "MLA"
                elif "gpt" in mid.lower() or "claude" in mid.lower():
                    attention_type = "MHA"
                    
                merged_records[norm] = {
                    "model_id": mid,
                    "name": f"Cloud: {row['name']}",
                    "parameters_b": params_b,
                    "layers": 32,
                    "hidden_size": 4096,
                    "num_heads": 32,
                    "num_kv_heads": 8,
                    "attention_type": attention_type,
                    "hosting": "Solo Cloud (APIs / OpenRouter)",
                    "native_context": int(row["context_length"]),
                    "speed_local": 0.0,
                    "speed_cloud": 25.0 if params_b > 50 else (60.0 if params_b > 10 else 100.0),
                    "ttft_ms": 200 + (300 if params_b > 50 else 100),
                    "cost_input_per_m": float(row["cost_input_per_m"]),
                    "cost_output_per_m": float(row["cost_output_per_m"]),
                    "format": "API / SaaS",
                    "ifeval": ifeval,
                    "mmlu": mmlu,
                    "gpqa": gpqa,
                    "benchmarks_verificados": bench_verified
                }
                
        if not aa_df.empty:
            for _, row in aa_df.iterrows():
                norm = row["norm_id"]
                tps = row["tps"]
                ttft = row["ttft_ms"]
                
                match_key = None
                if norm in merged_records:
                    match_key = norm
                else:
                    for k in merged_records.keys():
                        if k in norm or norm in k:
                            match_key = k
                            break
                if match_key:
                    if tps is not None:
                        if merged_records[match_key]["format"] == "API / SaaS":
                            merged_records[match_key]["speed_cloud"] = tps
                        else:
                            merged_records[match_key]["speed_local"] = tps
                    if ttft is not None:
                        merged_records[match_key]["ttft_ms"] = ttft
                        
        df_unified = pd.DataFrame(list(merged_records.values()))
        return df_unified

    def extract_params_from_id(self, model_id: str) -> float:
        match = re.search(r'(\d+(?:\.\d+)?)\s*[Bb]', model_id)
        if match:
            return float(match.group(1))
        match_m = re.search(r'(\d+(?:\.\d+)?)\s*[Mm]', model_id)
        if match_m:
            return float(match_m.group(1)) / 1000.0
            
        if "opus" in model_id.lower() or "sonnet" in model_id.lower() or "gpt-4" in model_id.lower():
            return 100.0
        if "haiku" in model_id.lower() or "mini" in model_id.lower() or "gpt-3.5" in model_id.lower():
            return 8.0
        return 7.0

    def load_cache(self) -> pd.DataFrame:
        if os.path.exists(self.cache_file):
            try:
                return pd.read_json(self.cache_file)
            except Exception as e:
                print(f"Error reading cache_file: {e}")
        orig_cache = "model_catalog_cache.json"
        if os.path.exists(orig_cache):
            try:
                return pd.read_json(orig_cache)
            except Exception as e:
                print(f"Error reading orig_cache: {e}")
        return pd.DataFrame()

    def save_cache(self, df: pd.DataFrame):
        try:
            df.to_json(self.cache_file, orient="records", indent=2, force_ascii=False)
            print(f"Cache saved successfully with {len(df)} records.")
        except Exception as e:
            print(f"Error saving cache: {e}")

    async def ingest(self) -> pd.DataFrame:
        try:
            df = await self.ingest_live()
            if not df.empty:
                self.save_cache(df)
                return df
            else:
                raise ValueError("Ingested DataFrame is empty")
        except Exception as e:
            print(f"Ingest failed: {e}. Loading cache...")
            return self.load_cache()

async def main():
    ingester = LLMDataIngester()
    df = await ingester.ingest()
    print("Unified DataFrame columns:", list(df.columns))
    print("Total rows:", len(df))
    if not df.empty:
        print("Sample models:")
        print(df[["model_id", "hosting", "ifeval", "mmlu", "gpqa"]].head(5))

if __name__ == "__main__":
    asyncio.run(main())
