import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df = pd.read_csv("../data/raw/customers.csv")

print(df.head())

df.info()