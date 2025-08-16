
import argparse, os, json
import pandas as pd
def main(input_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.read_csv(input_path)
    for col in ["RowNumber","Surname"]:
        if col in df.columns:
            df = df.drop(columns=[col])
    df_enc = pd.get_dummies(df, columns=["Geography","Gender"], drop_first=True)
    df_enc.to_csv(output_path, index=False)
    feature_cols = [c for c in df_enc.columns if c not in ("Exited","CustomerId")]
    os.makedirs("models", exist_ok=True)
    with open("models/feature_columns.json","w") as f:
        json.dump(feature_cols, f, indent=2)
if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", default="data/processed/churn_processed.csv")
    args = ap.parse_args()
    main(args.input, args.output)
