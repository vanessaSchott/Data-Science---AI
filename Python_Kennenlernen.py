import numpy as np
import pandas as pd
import statsmodels.api as sm 
import matplotlib.pyplot as plt
import seaborn as sns

dataset = sm.datasets.get_rdataset("SwissLabor", "AER", cache=True)
print(dataset.__doc__)
swiss_labor = sm.datasets.get_rdataset("SwissLabor", "AER", cache=True).data.copy()

#Aufgabe 1 
swiss_labor.head(10)
len(swiss_labor)
len(swiss_labor.columns)
swiss_labor.info()
swiss_labor.describe()
swiss_labor.shape

#Aufgabe 2
swiss_labor['income'] = np.exp(swiss_labor['income'])
swiss_labor['income'].describe()

#Aufgabe 3 
swiss_labor['age'] = swiss_labor['age'] * 10
swiss_labor['age'] = swiss_labor['age'].astype(int)
swiss_labor['age'].describe()

#Aufgabe 4 
# filter for foreign == no, age > 21 & participation == yes
df_filtered = swiss_labor[(swiss_labor['foreign'] == 'no') & (swiss_labor['age'] <= 21) 
                          & (swiss_labor['participation'] == 'yes')]
df_filtered.info()
print(df_filtered['foreign'].unique())
print(df_filtered['participation'].unique())
print(df_filtered['age'].max())

#Aufgabe 5
df_filtered.groupby("age", observed=False).size().reset_index(name='n')

#Aufgabe 6
# wie viele Personen sind Teil des Arbeitsmarktes?
num_participants = swiss_labor[swiss_labor['participation'] == 'yes'].shape[0]
print(f"Number of participants in the labor market: {num_participants}. \
      This resembles {num_participants / len(swiss_labor) * 100:.2f}% of the total.")

#Aufgabe 7
counts = swiss_labor.value_counts(['foreign', 'participation']).rename("n").reset_index()
counts['percentage'] = counts['n'] / counts.groupby(['foreign'])['n'].transform('sum') * 100
counts

#Aufgabe 8
print(swiss_labor['income'].median())
swiss_labor['kids'] = np.where(
    (swiss_labor['youngkids'] != 0) | (swiss_labor['oldkids'] != 0),
    "yes",
    "no"
)
swiss_labor.info()
income_kids = swiss_labor.groupby('kids')['income'].median().reset_index(name='median_income')
print(income_kids)

swiss_labor.head(100)

#Aufgabe 9
sns.histplot(swiss_labor['income'], bins=100)
plt.title('Income Distribution')
plt.xlabel('Income')
plt.ylabel('Frequency')
plt.show()