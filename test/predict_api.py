import os
import sys

project_root = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, project_root)

from src.predictor import predict_colleges


results = predict_colleges(
    rank=1000,
    quota=None,
    state=None,
    course="MBBS",
    allottedCategory=None,
    candidateCategory="General",
    phase=1,
    top_n=10
)

print("\nPrediction Test Results:\n")

for index, college in enumerate(results, start=1):
    print(f"{index}. {college['institute']}")
    print(f"   State: {college['state']}")
    print(f"   Closing Rank: {college['predictedClosingRank']}")
    print()