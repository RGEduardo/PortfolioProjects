import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Load your dataset (Data about Mexico City)
df = pd.read_csv('Data.csv')

##DAILY AVG ANALYSIS
# Convert the 'DATE' column to datetime format
df['DATE'] = pd.to_datetime(df['DATE'], format="%d/%m/%Y")
# Convert temperature to Celsius
df['TAVG'] = (df['TAVG'] - 32) * (5/9) 

# Calculate daily temperature averages
daily_avg_temp = df.groupby('DATE')['TAVG'].mean().reset_index()

# Perform linear regression for trendline
X1 = daily_avg_temp['DATE'].dt.year.values.reshape(-1, 1)
y1 = daily_avg_temp['TAVG'].values.reshape(-1, 1)
regressor = LinearRegression()
regressor.fit(X1, y1)
y_pred1 = regressor.predict(X1)

# Calculate the trend slope
slope = regressor.coef_[0][0]
print(f"Daily Average Temperature Trend in Mexico City (Slope): {slope:.4f} °C/year")
print("The temperature is increasing over time.")

# Create a subplot for daily average temperature
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
sns.lineplot(x='DATE', y='TAVG', data=daily_avg_temp, color='b')
plt.title('Daily Average Temperature Over Time in Mexico City')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.grid(True)

# Create a subplot for linear trendline
plt.subplot(2, 1, 2)
sns.lineplot(x=daily_avg_temp['DATE'], y=y_pred1.flatten(), color='r', label='Trendline')
sns.scatterplot(x='DATE', y='TAVG', data=daily_avg_temp, color='b', label='Daily Avg Temp')
plt.title('Linear Trendline for Daily Average Temperature in Mexico City')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.grid(True)

# Adjust subplot layout
plt.tight_layout()

##SEASONAL ANALYSIS
# Extract year and month from the 'DATE' column
df['YEAR'] = df['DATE'].dt.year
df['MONTH'] = df['DATE'].dt.month

# Define a function to categorize months into seasons
def categorize_season(month):
    if 3 <= month <= 5:
        return 'Spring'
    elif 6 <= month <= 8:
        return 'Summer'
    elif 9 <= month <= 11:
        return 'Fall'
    else:
        return 'Winter'

# Apply the categorize_season function to create a 'SEASON' column
df['SEASON'] = df['MONTH'].apply(categorize_season)

# Calculate seasonal temperature averages
seasonal_avg_temp = df.groupby(['YEAR', 'SEASON'])['TAVG'].mean().unstack()

# Create a bar chart for seasonal average temperature
plt.figure(figsize=(12, 6))
seasonal_avg_temp.plot(kind='bar', figsize=(12, 6))
plt.title('Seasonal Avg Temperature Over the Years in Mexico City')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')

# Add a legend with custom colors
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(reversed(handles), reversed(labels), loc='upper left', title='Season', bbox_to_anchor=(1, 1))

plt.grid(axis='y')
plt.tight_layout()

# Calculate and print the season with the highest average temperature
max_season = seasonal_avg_temp.mean(axis=0).idxmax()
max_temp = seasonal_avg_temp.mean(axis=0).max()
print(f"The season with the highest average temperature in Mexico City is {max_season} with an average temperature of {max_temp:.2f} °C.")

##LONG TERM TRENDS
# Calculate annual temperature averages
annual_avg_temp = df.groupby(df['YEAR'])['TAVG'].mean()

# Perform linear regression for long-term trendline
X = annual_avg_temp.index.values.reshape(-1, 1)
y = annual_avg_temp.values.reshape(-1, 1)
regressor = LinearRegression()
regressor.fit(X, y)
y_pred = regressor.predict(X)

# Calculate the trend slope
slope = regressor.coef_[0][0]
print(f"Annual Average Temperature Trend in Mexico City (Slope): {slope:.4f} °C/year")
print("The temperature is increasing over the years.")

# Create a scatter plot for long-term trends
plt.figure(figsize=(12, 6))
plt.scatter(X, y, label='Annual Avg Temp', color='blue', marker='o', s=50)
plt.plot(X, y_pred, color='red', linewidth=2, label='Trendline')
        
plt.title('Annual Average Temperature Trends Over Years in Mexico City')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')

# Extend the trendline
year_range = np.arange(min(X), max(X) + 10)  # Extend the trendline by 10 years
plt.plot(year_range, regressor.predict(pd.DataFrame(year_range, columns=['Year'])), color='red', linestyle='--', linewidth=2, label='Extended Trendline')

plt.legend()
plt.grid(True)
plt.show()

