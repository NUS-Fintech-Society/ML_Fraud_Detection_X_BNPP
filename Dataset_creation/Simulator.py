import random

import pandas as pd
from faker import Faker


class Simulator:
    """
    Class used to simulate BNP data with the specified headers (21 in total)
    """

    def __init__(self):
        """
        Initialises the Simulator Object
        """
        self.payment_execution_date = []
        self.payment_modification_date_and_time = []
        self.payment_creation_date_and_time = []
        self.payment_authorisation_date_and_time = []
        self.payment_file_format_channel = []
        self.ordering_bank_code = []
        self.ordering_account_number = []
        self.client_entity_name = []
        self.beneficiary_account_number = []
        self.beneficiary_name = []
        self.beneficiary_address = []
        self.beneficiary_bank_code = []
        self.beneficiary_country = []
        self.instruction_payment_type = []
        self.payment_amount = []
        self.payment_currency = []
        self.remittance_advice = []
        self.connexis_user_id_maker = []
        self.connexis_user_id_authoriser = []
        self.user_country_geo_location = []
        self.user_last_successful_login_date_time = []

        self.features = {
            "Payment Execution Date": self.payment_execution_date,
            "Payment Modification Date and Time": self.payment_modification_date_and_time,
            "Payment Creation Date and Time": self.payment_creation_date_and_time,
            "Payment Authorisation Date and Time": self.payment_authorisation_date_and_time,
            "Payment File Format/Channel": self.payment_file_format_channel,
            "Ordering Bank (Swift Code or Local Bank Code)": self.ordering_bank_code,
            "Ordering Account Number": self.ordering_account_number,
            "Client Entity Name": self.client_entity_name,
            "Beneficiary Account Number": self.beneficiary_account_number,
            "Beneficiary Name": self.beneficiary_name,
            "Beneficiary Address": self.beneficiary_address,
            "Beneficiary Bank (Swift Code or Local Bank Code)": self.beneficiary_bank_code,
            "Beneficiary Country": self.beneficiary_country,
            "Instruction/Payment Type": self.instruction_payment_type,
            "Payment Amount": self.payment_amount,
            "Payment Currency": self.payment_currency,
            "Remittance Advice": self.remittance_advice,
            "Connexis User ID (Maker)": self.connexis_user_id_maker,
            "Connexis User ID (Authoriser)": self.connexis_user_id_authoriser,
            "User Country Geo-Location": self.user_country_geo_location,
            "User last successful login date/time": self.user_last_successful_login_date_time
        }

    def get_simulated_df(self, *, num_rows: int, seeded: bool = True) -> pd.DataFrame:
        """
        Gets a Simulated DataFrame of BNP dataset with 21 headers in total

        :param num_rows: Specifies the number of rows to be included in the dataset
        :param seeded: Default is to set the seed for the random generator
        :return: A DataFrame of (num_rows x 21) shape
        """
        faker = Faker()

        if seeded:
            faker.seed_instance(0)
            random.seed(0)

        for _ in range(num_rows):
            # should probably consider to add more logic in here. For example, should payment_execution_date be
            # before or after payment_modification_date_and_time? or should the beneficiary_address and
            # beneficiary_country be the same area? etc

            # double-check the meaning of the dataset headers because idk what they actl mean tbh

            self.payment_execution_date.append(faker.date_time())
            self.payment_modification_date_and_time.append(faker.date_time())
            self.payment_creation_date_and_time.append(faker.date_time())
            self.payment_authorisation_date_and_time.append(faker.date_time())
            self.payment_file_format_channel.append(faker.file_extension()) # dk what type of file extensions to specify
            self.ordering_bank_code.append(faker.iban())  # tried to get the swift one but faker module got some prob
            self.ordering_account_number.append(faker.credit_card_number())
            self.client_entity_name.append(faker.name())
            self.beneficiary_account_number.append(faker.credit_card_number())
            self.beneficiary_name.append(faker.name())
            self.beneficiary_address.append(faker.address())
            self.beneficiary_bank_code.append(faker.iban())
            self.beneficiary_country.append(faker.country())
            # self.instruction_payment_type.append(faker.text())    # dk what this is
            # floating numbers capped at 20000, should probably think about mapping it based on the currency value
            self.payment_amount.append(random.randint(0, 20000) * random.random())
            self.payment_currency.append(faker.currency())
            # self.remittance_advice.append(faker.text())   # dk what this is either
            self.connexis_user_id_maker.append(faker.user_name())
            self.connexis_user_id_authoriser.append(faker.user_name())
            self.user_country_geo_location.append(faker.country())
            self.user_last_successful_login_date_time.append(faker.date_time())

        df = pd.DataFrame(list(self.features.values())).transpose()
        df.columns = list(self.features.keys())

        return df
