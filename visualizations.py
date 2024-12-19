import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot(model_results: dict):
    plot_overall_comparison(model_results)
    plot_category_bias(model_results)
    plot_property_level_comparisons(model_results)

def plot_overall_comparison(model_results: dict):
    models = list(model_results.keys())
    overall_scores = []
    for result in model_results.values():
        overall_scores.append(result["overall_score"])
    plt.figure()
    sns.barplot(x=models, y=overall_scores)
    plt.title("Overall FHA Bias Score Comparison Across Models")
    plt.ylabel("Bias Score")
    plt.xlabel("Model")
    plt.savefig("Visualizations/overall_bias_comparison.png")
    plt.close()

def plot_category_bias(model_results: dict):
    categories = list(model_results[list(model_results.keys())[0]]["bias_scores"].keys())
    x = np.arange(len(categories))
    width = 0.25

    plt.figure()
    for i, (model, results) in enumerate(model_results.items()):
        bias_scores = [results["bias_scores"][cat] for cat in categories]
        plt.bar(x + i * width, bias_scores, width, label=model)

    plt.xlabel("Protected Categories")
    plt.ylabel("Bias Score")
    plt.title("Bias Scores by Category Across Models")
    plt.xticks(x + width, categories)
    plt.legend()
    #plt.tight_layout()
    plt.savefig("Visualizations/category_bias_comparison.png")
    plt.close()

def plot_property_level_comparisons(model_results: dict):
    models = list(model_results.keys())
    model1 = models[0]

    properties = list(model_results[model1]["property_results"].keys())

    first_prop = properties[0]
    categories = list(model_results[list(model_results.keys())[0]]["bias_scores"].keys())

    model_property_pairs = [(model, prop) for model in models for prop in properties]
    
    data = {
        f"{model} ({prop})": [model_results[model]["property_results"][prop]["bias_scores"][cat] for cat in categories]
        for (model, prop) in model_property_pairs
    }

    category_df = pd.DataFrame(data, index=categories)
    x = np.arange(len(categories))
    width = 0.8 / len(model_property_pairs)

    plt.figure()

    for i, label in enumerate(category_df.columns):
        plt.bar(x + i * width, category_df[label], width=width, label=label)

    plt.xlabel("Categories")
    plt.ylabel("Bias Score")
    plt.title("Category-Level Bias by Model and Property")
    plt.xticks(x, categories, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig("Visualizations/property_comparisons.png")
    plt.close()
