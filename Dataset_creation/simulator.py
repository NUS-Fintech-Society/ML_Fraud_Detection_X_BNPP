import random

import pandas as pd

from Dataset_creation.models import Behaviour, Customer

if __name__ == "__main__":
    df = pd.DataFrame()
    num_of_customers = 500

    for _ in range(num_of_customers):
        behaviour = Behaviour()

        customer = Customer(behaviour)

        num_of_transactions = random.randint(1, 50)
        df_customer = customer.simulate_transactions(num_of_transactions=num_of_transactions)
        df = df.append(df_customer)

    df = df.sort_values('Payment Authorisation Date and Time')
    df.to_csv('Dataset_creation/data/df_simulated.csv', index=False)
