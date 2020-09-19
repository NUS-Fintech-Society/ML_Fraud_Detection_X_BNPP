import random

import pandas as pd

from Dataset_creation.models import Behaviour, Customer

if __name__ == "__main__":
    df = pd.DataFrame()
    num_of_customers = 500

    for _ in range(num_of_customers):

        """
        0: Normal Customer
        1: Multiple Small Transactions
        2: One Large Transaction
        3: Transaction occurs outside of normal working hours of client
        4: Time of last login and transaction has very huge time gap
        5: Account only has incoming transactions with no outgoing transactions
        """

        behaviour = Behaviour(random.randint(0,5)) 
        #for now we leave it as an even spread? if in future we wanna do a spread maybe
        #we can use NumPy's choice fn to select the weights we want

        customer = Customer(behaviour)

        if customer.get_behaviour_id == 1:
            num_of_transactions = 100
        elif customer.get_behaviour_id ==2:
            num_of_transactions = 1
        else:
            num_of_transactions = random.randint(1, 50)

        df_customer = customer.simulate_transactions(num_of_transactions=num_of_transactions)
        df = df.append(df_customer)

    df = df.sort_values('Payment Authorisation Date and Time')
    df.to_csv('Dataset_creation/data/df_simulated.csv', index=False)
