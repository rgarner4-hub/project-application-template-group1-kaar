from typing import List
from data_loader import DataLoader
from model import Issue
import matplotlib.pyplot as plt
import pandas as pd

class DayOfWeekAnalysis:

    def run(self):
        # Load all issues from the JSON file
        issues: List[Issue] = DataLoader().get_issues()

        day_counts = {}

        # Go through each issue and count how many on each day
        for issue in issues:
            created = pd.to_datetime(issue.created_date)
            day_name = created.day_name()

            if day_name not in day_counts:
                day_counts[day_name] = 0
            day_counts[day_name] += 1

        print("\nIssues created by day of the week:")
        for day, count in day_counts.items():
            print(f"{day}: {count}")

        # Make a bar chart
        plt.figure(figsize=(10, 5))
        plt.bar(day_counts.keys(), day_counts.values())
        plt.title("Issues Created by Day of the Week")
        plt.xlabel("Day of Week")
        plt.ylabel("Number of Issues")
        plt.grid(axis='y')
        plt.show()
