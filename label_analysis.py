from typing import List
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

from data_loader import DataLoader
from model import Issue
import config

class LabelAnalysis:
    """
    Analyzes the labels associated with GitHub issues to determine
    the distribution of topics (e.g., bugs, features, documentation).
    """

    def __init__(self):
        # Allow filtering by a specific label if passed via --label command line arg
        self.TARGET_LABEL: str = config.get_parameter('label')

    def run(self):
        print("Running Label Analysis...")
        issues: List[Issue] = DataLoader().get_issues()

        # 1. Collect all labels from all issues
        all_labels = []
        for issue in issues:
            if issue.labels:
                for label in issue.labels:
                    # Handle raw dictionaries or simple strings
                    if isinstance(label, dict):
                        name = label.get('name')
                        if name:
                            all_labels.append(name)
                    elif isinstance(label, str):
                        all_labels.append(label)

        if not all_labels:
            print("No labels found in the dataset.")
            return

        # 2. Count frequency of each label
        label_counts = Counter(all_labels)

        # 3. Convert to DataFrame for easy handling and plotting
        df = pd.DataFrame.from_dict(label_counts, orient='index', columns=['count'])
        
        # Sort by count descending
        df = df.sort_values(by='count', ascending=False)

        print("\n\n--- TOP 20 LABELS BY FREQUENCY ---")
        print(df.head(20))

        # 4. Plotting
        plt.figure(figsize=(14, 8))
        
        # Plot top 20
        top_20 = df.head(20)
        bars = plt.bar(top_20.index, top_20['count'], color='skyblue')
        
        plt.title(f"Top 20 Issue Labels (n={len(issues)} issues)")
        plt.xlabel("Label Name")
        plt.ylabel("Frequency")
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Highlight requested label if provided
        if self.TARGET_LABEL:
            print(f"\nHighlighting requested label: {self.TARGET_LABEL}")
            for bar, label in zip(bars, top_20.index):
                if label == self.TARGET_LABEL:
                    bar.set_color('red')

        plt.show()

if __name__ == '__main__':
    LabelAnalysis().run()
