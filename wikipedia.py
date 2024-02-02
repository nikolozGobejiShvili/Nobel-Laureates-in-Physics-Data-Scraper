from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd

# Setting up the Chrome driver
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Navigating to the Wikipedia page on Nobel laureates in Physics
url = 'https://en.wikipedia.org/wiki/List_of_Nobel_laureates_in_Physics'
driver.get(url)

# Extracting laureate data (Year, Laureate, Nationality)
laureate_data = []
table_rows = driver.find_elements(By.CSS_SELECTOR, 'table.wikitable tbody tr')

for row in table_rows:
    columns = row.find_elements(By.TAG_NAME, 'td')
    if columns and len(columns) >= 3: # Ensure the row has at least 3 columns
        year = columns[0].text.strip()
        laureate = columns[1].text.strip()
        nationality = columns[2].text.strip() if len(columns) > 4 else ' '
        laureate_data.append({'Year': year, 'Laureate': laureate, 'Nationality': nationality})

# Creating a DataFrame to store the laureate data
df_laureates = pd.DataFrame(laureate_data)

# Navigating to the Nobel laureates page to extract all Nobel laureates (if needed)
nobel_url = 'https://en.wikipedia.org/wiki/List_of_Nobel_laureates'
driver.get(nobel_url)

# Extracting Physics laureates data
physics_data = []
physics_rows = driver.find_elements(By.CSS_SELECTOR, 'table.wikitable tbody tr')

for row in physics_rows:
    columns = row.find_elements(By.TAG_NAME, 'td')
    if columns and len(columns) >= 2: # Ensure the row has at least 2 columns
        year = columns[0].text.strip()
        physics = columns[1].text.strip()
        physics_data.append({'Year': year, 'Physics': physics})

# Creating a DataFrame for Physics laureates data
df_physics = pd.DataFrame(physics_data)

# Merging the two DataFrames on the "Year" column (if this is the correct logic)
df_combined = pd.merge(df_physics, df_laureates, on="Year", how="left")

# Saving the combined data to a CSV file
df_combined.to_csv('nobel_laureates_combined.csv', index=False)

# Analyzing nationalities using Pandas
nationality_counts = df_combined['Nationality'].value_counts()

# Print the Nationality Analysis
print("\nNationality Analysis:")
print(nationality_counts)

# Quit the driver
driver.quit()
