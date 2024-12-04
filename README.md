# Forest Fire Analysis Project

## 📋 Introduction
This project analyzes a dataset of environmental conditions relevant to forest fires in a national park in Portugal. The aim is to present the data in an accessible way, uncover interesting patterns, and explore correlations between variables to better understand fire behavior.

### Dataset Variables:
- **Temporal Data:** Month and day of fire occurrences.
- **FFMC (Fine Fuel Moisture Code):** Moisture content of litter and fine fuels.
- **DMC (Duff Moisture Code):** Fuel moisture of decomposed organic material.
- **DC (Drought Code):** Moisture content in deep compact organic layers.
- **ISI (Initial Spread Index):** Expected fire spread rate, based on wind speed and FFMC.
- **Temperature (°C):** Daily temperature during fires.
- **Relative Humidity (RH):** Air moisture ratio as a percentage.
- **Wind Speed:** Speed of wind during the day.
- **Rain:** Amount of rainfall on the day.
- **Burned Area:** Total area engulfed by flames.

## 🛠️ Project Workflow

### Problem 1: Data Preparation
- Imported the dataset into a Pandas DataFrame for easy manipulation.
- Checked and handled missing values to ensure reliable data processing.
![image](https://github.com/user-attachments/assets/ab73d416-31d7-4cc5-bbb4-f37fd44cbd79)

---

### Problem 2: Visualizing Fire Distribution
- Created a bar chart to visualize fire frequency by month using `matplotlib`.
- Key findings:
  - **August** and **September** are peak months for fires.
  - Higher temperatures in June and July create drier conditions, leading to more fires later.

---

### Problem 3: Temperature and Area Correlation
- Standardized data using `StandardScaler` from `sklearn` for correlation analysis.
- Outliers were detected using the Z-score and removed to improve accuracy.
- Correlation Results:
  - **Temperature vs. Area:** Weak positive correlation (0.0697).
  - **Humidity vs. Fires:** Weak negative correlation (-0.1015).
  - Interpretation: Fire severity and frequency depend on multiple factors beyond temperature and humidity.

---

### Problem 4: Seasonal and Monthly Trends
- Plots created using `matplotlib` to explore:
  - Burned area by month.
  - Number of fires by season.
  - Average monthly variable trends.
- Observations:
  - Duff Moisture Code (DMC) and Drought Code increase as fire frequency rises.
  - DMC correlation with fire count is weak but positive (0.073).

---

### Problem 5: Principal Component Analysis (PCA)
- Applied PCA to reduce dimensionality and visualize relationships between variables.
- Tools: `sklearn` for PCA, `pandas` for data handling, and `matplotlib` for visualization.
- Insights:
  - **PC1:** Influenced by weather factors like temperature, rainfall, and fuel moisture.
  - **PC2:** Represents variability in fire occurrence and environmental conditions.

---

### Problem 6: Multiple Linear Regression
- Built a multiple linear regression model using `sklearn` to predict fire behavior based on environmental variables.

---

## 🧰 Tools and Libraries
- **Python**: Core programming language.
- **Pandas**: Data manipulation and analysis.
- **Matplotlib**: Data visualization.
- **Scikit-learn**: Standardization, PCA, and regression modeling.

## 📊 Key Takeaways
- Environmental variables such as fuel moisture, humidity, and temperature play crucial roles in fire behavior but are not sole predictors.
- PCA and regression modeling provide valuable insights into the interplay of these factors, revealing the complexity of fire dynamics.

---

## 🚀 How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/forest-fire-analysis.git
