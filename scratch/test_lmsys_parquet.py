import pandas as pd

url = "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset/resolve/main/text/latest-00000-of-00001.parquet"

try:
    print(f"Reading parquet from {url}...")
    df = pd.read_parquet(url)
    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print("\nFirst row preview:")
    print(df.iloc[0].to_dict())
    
    # Print the top 5 models by ELO
    # Let's find column names related to ELO or model
    # Usually it's model, rating (or elo), etc.
    model_col = None
    rating_col = None
    for col in df.columns:
        if "model" in col.lower():
            model_col = col
        if "rating" in col.lower() or "elo" in col.lower():
            rating_col = col
            
    if model_col and rating_col:
        print(f"\nTop 5 models by {rating_col}:")
        top_df = df.sort_values(by=rating_col, ascending=False).head(5)
        for idx, row in top_df.iterrows():
            print(f" - {row[model_col]}: {row[rating_col]}")
except Exception as e:
    print("Error:", e)
