import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    try:
        dataset = sm.datasets.get_rdataset("SwissLabor", "AER", cache=True)
    except Exception as e:
        print("Fehler beim Laden des Datasets:", e)
        return

    print(dataset.__doc__)
    swiss_labor = dataset.data.copy()

    # Aufgabe 1 - kurze Ausgaben
    print("\n--- Aufgabe 1 ---")
    print(swiss_labor.head(10))
    print("rows,cols:", swiss_labor.shape)
    print(swiss_labor.describe())

    # Aufgabe 2 - Income transform
    swiss_labor['income'] = np.exp(swiss_labor['income'])
    print("income non-null nach exp:", swiss_labor['income'].notna().sum())

    # Aufgabe 3 - Age
    swiss_labor['age'] = (swiss_labor['age'] * 10).astype(int)
    print(swiss_labor['age'].describe())

    # Aufgabe 4 - Filter (angepasst: age > 21 wie Kommentar)
    df_filtered = swiss_labor[(swiss_labor['foreign'] == 'no') & (swiss_labor['age'] > 21)
                              & (swiss_labor['participation'] == 'yes')]
    print("\n--- Aufgabe 4 (filtered) ---")
    print(df_filtered.info())
    print('foreign uniques:', df_filtered['foreign'].unique())
    print('participation uniques:', df_filtered['participation'].unique())
    if not df_filtered.empty:
        print('max age filtered:', df_filtered['age'].max())

    # Aufgabe 5
    print(df_filtered.groupby('age', observed=False).size().reset_index(name='n'))

    # Aufgabe 6
    num_participants = swiss_labor[swiss_labor['participation'] == 'yes'].shape[0]
    print(f"Number of participants in the labor market: {num_participants}. "
          f"This resembles {num_participants / len(swiss_labor) * 100:.2f}% of the total.")

    # Aufgabe 7
    counts = swiss_labor.value_counts(['foreign', 'participation']).rename('n').reset_index()
    counts['percentage'] = counts['n'] / counts.groupby(['foreign'])['n'].transform('sum') * 100
    print('\nCounts:\n', counts)

    # Aufgabe 8
    print('\nMedian income:', swiss_labor['income'].median())
    swiss_labor['kids'] = np.where((swiss_labor['youngkids'] != 0) | (swiss_labor['oldkids'] != 0), 'yes', 'no')
    income_kids = swiss_labor.groupby('kids')['income'].median().reset_index(name='median_income')
    print(income_kids)

    # Aufgabe 9 - Plot mit dropna und block=True
    print('\nHistogramm...')
    plt.figure(figsize=(8, 6))
    sns.histplot(swiss_labor['income'].dropna(), bins=100)
    plt.title('Income Distribution')
    plt.xlabel('Income')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show(block=True)


if __name__ == '__main__':
    main()