import os
from test_case_generator import generate_test_cases
from response_handler import get_response
from analysis import analyze
from visualizations import plot
import pandas as pd

def main():
    model_names = {
        "gpt-3.5-turbo": "gpt-3.5-turbo",
        "gpt-4o": "gpt-4o"
    }

    test_cases = generate_test_cases()
    model_results = {}

    for model_type, model_name in model_names.items():
        results_file = model_type + "_audit_results.csv"

        if os.path.exists(results_file):
            print("Found file for " + model_type)
            response_df = pd.read_csv(results_file)
        else:
            responses = []
            for case in test_cases:
                temp = get_response(case, model_name=model_name)
                responses.append(temp)
            response_df = pd.DataFrame(responses).dropna(subset=["Rental Price"])
            response_df.to_csv(model_type + "_audit_results.csv", index=False)
        model_results[model_type] = analyze(response_df, model_type)
    
    # print(model_results)
    plot(model_results)

if __name__ == "__main__":
    main()
