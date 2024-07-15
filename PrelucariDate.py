import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import statsmodels.formula.api as smf
import seaborn as sns
from sklearn.preprocessing import StandardScaler



# The FFMC represents the moisture content of litter and other cured fine fuels in a forest stand
# The Duff Moisture Code (DMC) represents fuel moisture of decomposed organic material underneath the litter
# The Drought code is an indicator of the moisture content in deep compact organic layers.
# This code represents a fuel layer at approximately 10-20 cm deep. 
# The Drought code fuels have a very slow drying rate, with a time lag of 52 days
# The Initial Spread Index (ISI) is a numeric rating of the expected rate of fire spread. It is based on wind speed and FFMC.
# Relative humidity (RH) is the ratio of the amount of moisture in the air to the amount of moisture
#  necessary to saturate the air at the same temperature and pressure. Relative humidity is expressed in percent


forest_fire_data = pd.read_csv("forestfires.csv")
print(forest_fire_data)

# verifying if there are any missing values / Data Cleaning
for column in forest_fire_data.columns:
    if(forest_fire_data[column].isnull().sum()):
        forest_fire_data[column].fillna(forest_fire_data[column].mean(), inplace=True)
    else:
        print("No missing values for:", column)



# Count the number of fires for each month
fires_by_month = forest_fire_data['month'].value_counts()
fires_by_month = fires_by_month.sort_values(ascending=False)


def plot_bar_chart(data, title, xlabel, ylabel):
    plt.figure(figsize=(8, 6))
    data.plot(kind='bar', color='red')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.show()


plot_bar_chart(fires_by_month, 'Number of Fires by Month', 'Month', 'Number of Fires')
print(fires_by_month)
print()
print(40*'-')
print()

# Calculate the average temperature for each month
avg_temp_by_month = forest_fire_data.groupby('month')['temp'].mean().sort_values(ascending=False)

plot_bar_chart(avg_temp_by_month, 'Average Temperature by Month', 'Month', 'Average Temperature')   
print(avg_temp_by_month)
print()
print(40*'-')
print()


# Correlating the temperature and area affected by fires
# Identify and handle outliers
scaler = StandardScaler()
standardized_data = scaler.fit_transform(forest_fire_data.drop(columns=['month', 'day', 'X', 'Y']))
outliers = forest_fire_data[abs(standardized_data) > 3]  
cleaned_df = forest_fire_data.drop(outliers.index)
temperature_cleaned = cleaned_df['temp']
area_affected_cleaned = cleaned_df['area']

correlation_coefficient_cleaned = temperature_cleaned.corr(area_affected_cleaned)



plt.figure(figsize=(8, 6))
plt.scatter(temperature_cleaned, area_affected_cleaned, alpha=0.5)
plt.title('Relationship Between Temperature and Area Affected by Fires (Outliers Removed)')
plt.xlabel('Temperature')
plt.ylabel('Area Affected')
plt.grid(True)
plt.show()

print("Correlation Coefficient (Outliers Removed):", correlation_coefficient_cleaned)
print()
print(40*'-')
print()



# Correlation between relative humidity and number of fires by month
avg_rh_by_month = cleaned_df.groupby('month')['RH'].mean()
fires_by_month = cleaned_df['month'].value_counts()

plt.figure(figsize=(10, 6))
plt.scatter(avg_rh_by_month, fires_by_month, color='skyblue')
plt.title('Correlation between Relative Humidity and Number of Fires by Month')
plt.xlabel('Average Relative Humidity')
plt.ylabel('Number of Fires')
for i, month in enumerate(avg_rh_by_month.index):
    plt.text(avg_rh_by_month.iloc[i], fires_by_month[month], month, ha='center', va='bottom')
plt.grid(True)
plt.show()

correlation = avg_rh_by_month.corr(fires_by_month)
print("Correlation coefficient between Relative Humidity and Fires by Month:", correlation)
print()
print(40*'-')
print()


# Calculate the total area burned for each month
total_area_by_month = forest_fire_data.groupby('month')['area'].sum().sort_values(ascending=False)
max_area_month = total_area_by_month.idxmax()
max_area = total_area_by_month[max_area_month]

print("Month with the largest total burned area:", max_area_month)
print("Total area burned:", max_area)
plot_bar_chart(total_area_by_month, 'Total Area Burned by Month', 'Month', 'Total Area Burned')
print()
print(40*'-')
print()


# Calculate the number of fires for each season
month = forest_fire_data['month']

season_mapping = {
    'jan': 'Winter', 'feb': 'Winter', 'mar': 'Spring',
    'apr': 'Spring', 'may': 'Spring', 'jun': 'Summer',
    'jul': 'Summer', 'aug': 'Summer', 'sep': 'Fall',
    'oct': 'Fall', 'nov': 'Winter', 'dec': 'Winter'
}
season = month.map(season_mapping)
fires_per_season = season.value_counts()

plot_bar_chart(fires_per_season, 'Number of Fires per Season', 'Season', 'Number of Fires') 



# Calculate the average temperature, relative humidity, wind speed, FFMC, DMC, DC, and ISI for each month
avg_factors_by_month = forest_fire_data.groupby('month')[['temp', 'RH', 'wind', 'FFMC', 'DMC', 'DC', 'ISI']].mean()
order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
fires_by_month = forest_fire_data['month'].value_counts().reindex(order)
avg_factors_with_fires = pd.concat([avg_factors_by_month, fires_by_month], axis=1)
avg_factors_with_fires.columns = ['temp', 'RH', 'wind', 'FFMC', 'DMC', 'DC', 'ISI', 'Total Fires']
avg_factors_with_fires = avg_factors_with_fires.reindex(order)

plt.figure(figsize=(12, 8))
for column in avg_factors_with_fires.columns:
    plt.plot(avg_factors_with_fires.index, avg_factors_with_fires[column], marker='o', label=column)

plt.title('Comparison of Environmental Factors and Number of Fires Across Months')
plt.xlabel('Month')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.show()

correlation_dmc_fires = forest_fire_data['DMC'].corr(forest_fire_data['area'])

print("Correlation between DMC and the number of fires:", correlation_dmc_fires)
print()
print(40*'-')
print()


# Droping irrelevant columns
cleaned_df = cleaned_df.drop(columns=['month', 'day', 'X', 'Y'])


# Apply PCA
df_scaled = scaler.fit_transform(cleaned_df)
pca = PCA(n_components=2)
principal_components = pca.fit_transform(df_scaled)
df_pca = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
df_loadings = pd.DataFrame(loadings, columns=['PC1', 'PC2'], index=cleaned_df.columns)

plt.figure(figsize=(8, 6))
plt.scatter(df_pca['PC1'], df_pca['PC2'])
plt.title('PCA of Forest Fire Dataset')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
# plt.show()

print("Loadings:", df_loadings)
print()
print(40*'-')
print()

# Multiple Linear Regression
train = cleaned_df.sample(frac=0.8, random_state=42)  # Example: Splitting data into training and testing sets
test = cleaned_df.drop(train.index)

formula = 'area ~ temp + RH + wind + FFMC + DMC + DC + ISI'

results = smf.ols(formula, data=train).fit()

print(results.params)
print(results.predict(train))

plt.show()