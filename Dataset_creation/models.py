import random
from typing import Union

import pandas as pd
from faker import Faker


class Behaviour:
    """
    Models the behaviour of a Customer. Can define parameters here that specifies a certain behaviour in the customer.

    For example, can set upper and lower bounds of payment_amount (payment_bounds = [100, 50000]).
    If not specified, set to a default value.
    """

    def __init__(self,
                 payment_amount_lower_bound: int = None,
                 payment_amount_upper_bound: int = None):
        self.payment_amount_lower_bound = payment_amount_lower_bound or 0
        self.payment_amount_upper_bound = payment_amount_upper_bound or 50000


class Customer:
    """
    Customer object
    """

    def __init__(self, behaviour: Behaviour, seeded=True):
        """
        Initialises the Customer object.

        :param behaviour: Specifies a set of "rules" that each Customer should follow
        """
        self.faker = Faker()
        if seeded:
            self.faker.seed_instance(0)
            random.seed(0)

        self.behaviour = behaviour

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

    def get_payment_execution_date(self) -> str:
        """2016-11-01"""
        return "2016-11-01"

    def get_payment_modification_date_and_time(self) -> str:
        """11/1/16 1:47 AM"""
        return "11/1/16 1:47 AM"

    def get_payment_creation_date_and_time(self) -> str:
        """11/1/16 1:47 AM"""
        return "11/1/16 1:47 AM"

    def get_payment_authorisation_date_and_time(self) -> str:
        """11/1/16 1:47 AM"""
        return "11/1/16 1:47 AM"

    def get_payment_file_format_channel(self) -> str:
        """Connexis/SWIFT/Orion2"""
        channels = ["Connexis", "SWIFT", "Orion2"]

        return random.choice(channels)

    def get_ordering_bank_code(self) -> str:
        """BNPASGSGXXX"""
        return "BNPASGSGXXX"

    def get_ordering_account_number(self) -> str:
        """00200200223080USD"""
        return "00200200223080USD"

    def get_client_entity_name(self) -> str:
        """ABC LTD"""
        return "ABC LTD"

    def get_beneficiary_account_number(self) -> str:
        """XXXXXXXXX, Length and format may vary depending on the beneficiary country/market"""
        return "XXXXXXXXX"

    def get_beneficiary_name(self) -> str:
        """DEF LTD"""
        return "DEF LTD"

    def get_beneficiary_address(self) -> str:
        """XXXXXXXXX, May or may not be present"""
        return "XXXXXXXXX"

    def get_beneficiary_bank_code(self) -> str:
        """HBUKGB4BXXX"""
        return "HBUKGB4BXXX"

    def get_beneficiary_country(self) -> str:
        """UK, In ISO 2 letter country code format"""
        return "UK"

    def get_instruction_payment_type(self) -> str:
        """Normal Payment/ INTC Payment/ Payroll"""
        payment_types = ["Normal Payment", "INTC Payment", "Payroll"]

        return random.choice(payment_types)

    def get_payment_amount(self) -> Union[int, float]:
        """500000"""
        l_bound = self.behaviour.payment_amount_lower_bound
        u_bound = self.behaviour.payment_amount_upper_bound
        return 500000

    def get_payment_currency(self) -> str:
        """USD"""
        return "USD"

    def get_remittance_advice(self) -> str:
        """lasjhdlasjldjasdjklasdj, Max 4x35 characters"""
        return "lasjhdlasjldjasdjklasdj"

    def get_connexis_user_id_maker(self) -> str:
        """ASDASDA"""
        return "ASDASDA"

    def get_connexis_user_id_authoriser(self) -> str:
        """ASDASDA"""
        return "ASDASDA"

    def get_user_country_geo_location(self) -> str:
        """SG"""
        return "SG"

    def get_user_last_successful_login_date_time(self) -> str:
        """11/1/16 1:47 AM"""
        return "11/1/16 1:47 AM"

    def simulate_transactions(self, *, num_of_transactions: int) -> pd.DataFrame:
        """
        Gets a Simulated DataFrame of BNP dataset with 21 headers in total

        :param num_of_transactions: Specifies the number of rows to be included in the dataset
        :return: A DataFrame of (num_rows x 21) shape
        """

        connexis_user_id_maker = self.get_connexis_user_id_maker()
        connexis_user_id_authoriser = self.get_connexis_user_id_authoriser()

        for _ in range(num_of_transactions):
            # needs to be re-ordered accordingly
            user_country_geo_location = self.get_user_country_geo_location()
            payment_authorisation_date_and_time = self.get_payment_authorisation_date_and_time()
            user_last_successful_login_date_time = self.get_user_last_successful_login_date_time()
            payment_creation_date_and_time = self.get_payment_creation_date_and_time()
            payment_modification_date_and_time = self.get_payment_modification_date_and_time()
            payment_execution_date = self.get_payment_execution_date()
            payment_currency = self.get_payment_currency()
            payment_amount = self.get_payment_amount()

            payment_file_format_channel = self.get_payment_file_format_channel()
            ordering_bank_code = self.get_ordering_bank_code()
            ordering_account_number = self.get_ordering_account_number()
            client_entity_name = self.get_client_entity_name()
            beneficiary_account_number = self.get_beneficiary_account_number()
            beneficiary_name = self.get_beneficiary_name()
            beneficiary_address = self.get_beneficiary_address()
            beneficiary_bank_code = self.get_beneficiary_bank_code()
            beneficiary_country = self.get_beneficiary_country()
            instruction_payment_type = self.get_instruction_payment_type()
            remittance_advice = self.get_remittance_advice()

            self.payment_execution_date.append(payment_execution_date)
            self.payment_modification_date_and_time.append(payment_modification_date_and_time)
            self.payment_creation_date_and_time.append(payment_creation_date_and_time)
            self.payment_authorisation_date_and_time.append(payment_authorisation_date_and_time)
            self.payment_file_format_channel.append(payment_file_format_channel)
            self.ordering_bank_code.append(ordering_bank_code)
            self.ordering_account_number.append(ordering_account_number)
            self.client_entity_name.append(client_entity_name)
            self.beneficiary_account_number.append(beneficiary_account_number)
            self.beneficiary_name.append(beneficiary_name)
            self.beneficiary_address.append(beneficiary_address)
            self.beneficiary_bank_code.append(beneficiary_bank_code)
            self.beneficiary_country.append(beneficiary_country)
            self.instruction_payment_type.append(instruction_payment_type)
            self.payment_amount.append(payment_amount)
            self.payment_currency.append(payment_currency)
            self.remittance_advice.append(remittance_advice)
            self.connexis_user_id_maker.append(connexis_user_id_maker)
            self.connexis_user_id_authoriser.append(connexis_user_id_authoriser)
            self.user_country_geo_location.append(user_country_geo_location)
            self.user_last_successful_login_date_time.append(user_last_successful_login_date_time)

        df = pd.DataFrame(list(self.features.values())).transpose()
        df.columns = list(self.features.keys())

        return df
