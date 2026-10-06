import os
import sys

project_root = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, project_root)

from src.predictor import predict_colleges


results = predict_colleges(
    rank=1000,
    quota="All India",
    state="Andhra Pradesh",
    course="MBBS",
    allottedCategory="Open",
    candidateCategory="General",
    phase=1,
    top_n=10
)

print()
print("===== TOP 10 COLLEGE PREDICTIONS =====")

if not results:
    print("No matching colleges found.")

else:
    for i, college in enumerate(results, start=1):
        print(f"{i}. {college['institute']}")
        print(f"   State: {college['state']}")
        print(f"   Course: {college['course']}")
        print(f"   Quota: {college['quota']}")
        print(
            f"   Predicted Closing Rank: "
            f"{college['predictedClosingRank']}"
        )
        print()