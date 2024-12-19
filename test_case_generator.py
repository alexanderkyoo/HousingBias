import csv
import os
import itertools
from config import categories, property_descriptions

def generate_test_cases(filename="test_cases.csv"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    else:
        combos = list(itertools.product(*categories.values()))
        test_cases = []
        for name, desc in property_descriptions.items():
            for combo in combos:
                test_case = {"Property": name, "Property Description": desc}
                for i, cat_name in enumerate(categories.keys()):
                    test_case[cat_name] = combo[i]
                test_cases.append(test_case)

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=test_cases[0].keys())
            writer.writeheader()
            writer.writerows(test_cases)
        
        return test_cases