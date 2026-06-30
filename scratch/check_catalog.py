import sys
import os
sys.path.insert(0, os.getcwd())

from logic import cargar_catalogo_modelos

df = cargar_catalogo_modelos("Ambos (Híbrido)")
print(f"Total models: {len(df)}")
if "benchmarks_verificados" in df.columns:
    verified_count = df["benchmarks_verificados"].sum()
    print(f"Verified count: {verified_count}")
    print("\nSome verified models:")
    print(df[df["benchmarks_verificados"]][["model_id", "ifeval", "mmlu", "gpqa"]].head(10))
    print("\nSome non-verified models:")
    print(df[~df["benchmarks_verificados"]][["model_id", "ifeval", "mmlu", "gpqa"]].head(10))
else:
    print("Column 'benchmarks_verificados' NOT in DataFrame!")
