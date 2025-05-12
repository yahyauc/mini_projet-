#partie 1 :
import os  # Import OS module for file operations
import pandas as pd  # Handle tabular data
import numpy as np  # Perform statistical calculations
import matplotlib.pyplot as plt  # Basic data visualizations
import seaborn as sns  # Advanced plots and heatmaps
from datetime import datetime  # Work with date and time
import calendar  # Handle day names




# Load the dataset
df = pd.read_csv("visionnage_series.csv")
# Convert 'date' to datetime format
df['date'] = pd.to_datetime(df['date'])
# Convert 'heure_debut' to time format
df['heure_debut'] = pd.to_datetime(df['heure_debut'], format='%H:%M').dt.time
# Extract the day of the week
df['jour_semaine'] = df['date'].dt.day_name()
# Add a rounded hour column
df['heure_arrondie'] = df['heure_debut'].apply(lambda x: x.hour)
# Handle missing values using forward fill
df.fillna(method='ffill', inplace=True)
# Remove duplicate rows if any exist
df.drop_duplicates(inplace=True)
# Display first few rows of cleaned dataset
print(df.head())



#partie 2:

# Create the folder for saving images if it doesn't exist
output_folder = "streaming_data_visuals"
os.makedirs(output_folder, exist_ok=True)

# Analyze session distribution by hour of the day
hourly_distribution = df['heure_arrondie'].value_counts().sort_index()

# Analyze session distribution by day of the week
weekly_distribution = df['jour_semaine'].value_counts()

# Create a pivot table for heatmap (day vs. hour)
heatmap_data = df.pivot_table(index="jour_semaine", columns="heure_arrondie", values="durée", aggfunc="sum")

# Set up a proper order for days (Sunday to Saturday)
days_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
heatmap_data = heatmap_data.reindex(days_order)

# Plot session distribution by hour (curve)
plt.figure(figsize=(10,5))  # Set figure size
plt.plot(hourly_distribution, marker='o', color='b')  # Plot data
plt.xlabel("Hour of the Day")  # Label X-axis
plt.ylabel("Number of Sessions")  # Label Y-axis
plt.title("Viewing Sessions by Hour")  # Set title
plt.grid(True)  # Add grid lines
plt.savefig(f"{output_folder}/sessions_by_hour.png")  # Save the figure
plt.show()  # Display the plot

# Plot session distribution by day (bar chart)
plt.figure(figsize=(10,5))  # Set figure size
weekly_distribution.plot(kind="bar", color="purple")  # Plot data
plt.xlabel("Day of the Week")  # Label X-axis
plt.ylabel("Number of Sessions")  # Label Y-axis
plt.title("Viewing Sessions by Day")  # Set title
plt.savefig(f"{output_folder}/sessions_by_day.png")  # Save the figure
plt.show()  # Display the plot

# Plot heatmap for viewing intensity
plt.figure(figsize=(12,6))  # Set figure size
sns.heatmap(heatmap_data, cmap="coolwarm", annot=True, fmt=".0f")  # Create heatmap
plt.xlabel("Hour of the Day")  # Label X-axis
plt.ylabel("Day of the Week")  # Label Y-axis
plt.title("Viewing Heatmap: Day vs. Hour")  # Set title
plt.savefig(f"{output_folder}/heatmap_viewing.png")  # Save the figure
plt.show()  # Display the plot

# Save the results in a renamed file
df.to_csv("streaming_insights_summary.csv", index=False)



#partie 3:
# Identify the most-watched series on each platform
most_watched_series = df.groupby('plateforme')['série'].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else "No Data")

# Identify the dominant genre on each platform
dominant_genre = df.groupby('plateforme')['genre'].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else "No Data")

# Compare average session durations by genre
avg_duration_by_genre = df.groupby('genre')['durée'].mean().sort_values(ascending=False)

# Display results
print("Most Watched Series on Each Platform:\n", most_watched_series)
print("\nDominant Genre on Each Platform:\n", dominant_genre)
print("\nAverage Session Duration by Genre:\n", avg_duration_by_genre)

# Convert most watched series into a DataFrame for better handling
most_watched_series_df = most_watched_series.reset_index()
most_watched_series_df.columns = ['plateforme', 'série']

# Visualization: Most-watched series per platform (bar chart)
plt.figure(figsize=(10,5))
plt.bar(most_watched_series_df['plateforme'], most_watched_series_df['série'], color="green")
plt.xlabel("Streaming Platform")
plt.ylabel("Most Watched Series")
plt.title("Most Watched Series per Platform")
plt.xticks(rotation=45)
plt.savefig(f"{output_folder}/most_watched_series.png")
plt.show()

# Convert dominant genre into a DataFrame for better handling
dominant_genre_df = dominant_genre.reset_index()
dominant_genre_df.columns = ['plateforme', 'genre']

# Visualization: Dominant genre per platform (bar chart)
plt.figure(figsize=(10,5))
plt.bar(dominant_genre_df['plateforme'], dominant_genre_df['genre'], color="blue")
plt.xlabel("Streaming Platform")
plt.ylabel("Dominant Genre")
plt.title("Dominant Genre per Platform")
plt.xticks(rotation=45)
plt.savefig(f"{output_folder}/dominant_genre.png")
plt.show()

# Visualization: Average session duration by genre (bar chart)
plt.figure(figsize=(10,5))
avg_duration_by_genre.plot(kind="bar", color="red")
plt.xlabel("Genre")
plt.ylabel("Average Session Duration (minutes)")
plt.title("Average Session Duration by Genre")
plt.xticks(rotation=45)
plt.savefig(f"{output_folder}/avg_session_duration_by_genre.png")
plt.show()




#partie 4:
# Calculate average evening viewing time (18:00 - 00:00) per platform
evening_sessions = df[(df['heure_arrondie'] >= 18) & (df['heure_arrondie'] < 24)]
avg_evening_time = evening_sessions.groupby('plateforme')['durée'].mean()

# Count number of long sessions (> 60 min) per platform
long_sessions = df[df['durée'] > 60]
long_session_count = long_sessions.groupby('plateforme').size()

# Compare weekday vs. weekend viewing behavior per platform
df['is_weekend'] = df['jour_semaine'].apply(lambda x: x in ["Saturday", "Sunday"])
weekend_sessions = df[df['is_weekend'] == True].groupby('plateforme').size()
weekday_sessions = df[df['is_weekend'] == False].groupby('plateforme').size()

# Display results
print("Average Evening Viewing Time per Platform:\n", avg_evening_time)
print("\nNumber of Long Sessions per Platform:\n", long_session_count)
print("\nWeekend vs. Weekday Viewing Sessions:\n")
print("Weekends:\n", weekend_sessions)
print("Weekdays:\n", weekday_sessions)

# Visualization: Evening viewing time per platform (bar chart)
plt.figure(figsize=(10,5))
avg_evening_time.plot(kind="bar", color="orange")
plt.xlabel("Streaming Platform")
plt.ylabel("Average Evening Viewing Time (minutes)")
plt.title("Average Evening Viewing Time per Platform")
plt.xticks(rotation=45)
plt.savefig(f"{output_folder}/avg_evening_time.png")
plt.show()

# Visualization: Long session counts per platform (bar chart)
plt.figure(figsize=(10,5))
long_session_count.plot(kind="bar", color="cyan")
plt.xlabel("Streaming Platform")
plt.ylabel("Number of Long Sessions")
plt.title("Long Viewing Sessions (> 60 min) per Platform")
plt.xticks(rotation=45)
plt.savefig(f"{output_folder}/long_session_count.png")
plt.show()

# Visualization: Weekday vs. weekend sessions per platform (grouped bar chart)
weekend_weekday_df = pd.DataFrame({'Weekday': weekday_sessions, 'Weekend': weekend_sessions})
weekend_weekday_df.plot(kind="bar", figsize=(10,5), color=["blue", "red"])
plt.xlabel("Streaming Platform")
plt.ylabel("Number of Sessions")
plt.title("Weekday vs. Weekend Viewing Sessions per Platform")
plt.xticks(rotation=45)
plt.savefig(f"{output_folder}/weekday_vs_weekend.png")
plt.show()


#partie 5:

# Define output file names
results_file = "final_streaming_analysis.csv"

# Create a folder for saving analysis if it doesn’t exist
os.makedirs(output_folder, exist_ok=True)

# Save key results into a CSV file
summary_data = pd.DataFrame({
    "Platform": avg_evening_time.index,
    "Avg Evening Viewing Time": avg_evening_time.values,
    "Long Session Count": long_session_count.values,
    "Weekday Sessions": weekday_sessions.values,
    "Weekend Sessions": weekend_sessions.values
})

summary_data.to_csv(f"{output_folder}/{results_file}", index=False)

# Confirm successful completion
print(f"All results have been successfully saved in '{output_folder}/{results_file}'")

#Hamza Yahya
#Ahmed Daou
