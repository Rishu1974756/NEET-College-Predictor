from src.predictor import predict_colleges


results = predict_colleges(
    rank=100000,
    quota="All India",
    state="Andhra Pradesh",
    course="MBBS",
    allottedCategory="Open",
    candidateCategory="General",
    phase=1,
    top_n=10
)


print("===== TOP 10 COLLEGE PREDICTIONS =====")

if not results:
    print("No matching colleges found.")

else:
    for i, result in enumerate(results, start=1):

        print(f"{i}. {result['institute']}")

        print(f"   State: {result['state']}")
        print(f"   Course: {result['course']}")
        print(f"   Quota: {result['quota']}")
        print(f"   Category: {result['allottedCategory']}")

        print(
            f"   Predicted Closing Rank: "
            f"{int(result['predictedClosingRank']):,}"
        )

        print(f"   Phase: {result['phase']}")

        print()