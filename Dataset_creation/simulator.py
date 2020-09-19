import random

import pandas as pd

from Dataset_creation.models import Behaviour, Customer

if __name__ == "__main__":
    df = pd.DataFrame()
    for _ in range(500):
        behaviour = Behaviour()

        customer = Customer(behaviour)

        df_customer = customer.simulate_transactions(num_of_transactions=random.randint(1, 50))
        df = df.append(df_customer)

    df.to_csv('Dataset_creation/data/df_simulated.csv', index=False)
