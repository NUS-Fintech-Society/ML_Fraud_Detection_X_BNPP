import random

import pandas as pd

from Dataset_creation.models import Behaviour, Customer

if __name__ == "__main__":
    df = pd.DataFrame()
    num_of_customers = 500

    for _ in range(num_of_customers):
        behaviour_id = random.choices([0, 1, 2, 3, 4], weights=(90, 2.5, 2.5, 2.5, 2.5))[0]
        behaviour = Behaviour(behaviour_id)

        customer = Customer(behaviour)

        df_customer = customer.simulate_transactions()
        df = df.append(df_customer)

    df.to_csv('Dataset_creation/data/df_simulated.csv', index=False)
