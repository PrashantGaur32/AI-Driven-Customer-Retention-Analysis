
import argparse, os, json, joblib, numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score, classification_report, confusion_matrix

def risk_bucket(p):
    return "High" if p>=0.70 else ("Medium" if p>=0.40 else "Low")

def main(input_path):
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    df = pd.read_csv(input_path)
    X = df.drop(columns=["Exited","CustomerId"])
    y = df["Exited"]
    ids = df["CustomerId"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    pipe = Pipeline([("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=1500, solver="liblinear", class_weight="balanced", random_state=42))])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    y_prob = pipe.predict_proba(X_test)[:,1]
    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision_recall_f1": list(map(float, precision_recall_fscore_support(y_test, y_pred, average="binary", zero_division=0)[:3])),
        "roc_auc": float(roc_auc_score(y_test, y_prob)),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "report": classification_report(y_test, y_pred, digits=4)
    }
    with open("outputs/metrics.json","w") as f:
        json.dump(metrics, f, indent=2)
    joblib.dump(pipe, "models/best_model.joblib")
    full_prob = pipe.predict_proba(X)[:,1]
    out = pd.DataFrame({"CustomerId": ids, "Exited": y.values, "churn_probability": full_prob})
    out["risk_segment"] = out["churn_probability"].apply(risk_bucket)
    keep_cols = [c for c in ["Age","Balance","CreditScore","Tenure","NumOfProducts","HasCrCard","IsActiveMember","EstimatedSalary",
                             "Geography_Germany","Geography_Spain","Gender_Male"] if c in df.columns]
    out = out.join(df[keep_cols])
    out.to_csv("outputs/predictions_for_dashboard.csv", index=False)
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="data/processed/churn_processed.csv")
    args = ap.parse_args()
    main(args.input)
