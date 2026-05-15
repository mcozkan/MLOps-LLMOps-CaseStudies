import pandas as pd
import requests


df = pd.read_csv("data/raw/customers.csv")

df = df.head(10)

for _, row in df.iterrows():

    payload = {
        "customerId": int(row["customerId"]),
        "customerFName": row["customerFName"],
        "customerLName": row["customerLName"],
        "customerEmail": row["customerEmail"],
        "customerPassword": row["customerPassword"],
        "customerStreet": row["customerStreet"],
        "customerCity": row["customerCity"],
        "customerState": row["customerState"],
        "customerZipcode": str(row["customerZipcode"]),
    }

    response = requests.post(
        "http://localhost:8001/customers",
        json=payload
    )

    print(payload["customerId"], response.status_code, response.text)