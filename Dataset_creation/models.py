import datetime as dt
import random
from typing import Union

import ccy
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
                 payment_amount_upper_bound: int = None,
                 id):
        self.id = id

        if self.id == 2:
            self.payment_amount_lower_bound = 50000
        else:
            self.payment_amount_lower_bound = payment_amount_lower_bound or 0

        if self.if == 1:
            self.payment_amount_upper_bound = 1000
        else:
            self.payment_amount_upper_bound = payment_amount_upper_bound or 50000

    def get_id(self):
        return self.id


class Customer:
    """
    Customer object
    """

    def __init__(self, behaviour: Behaviour):
        """
        Initialises the Customer object.

        :param behaviour: Specifies a set of "rules" that each Customer should follow
        """
        self.faker = Faker()
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

    def get_behaviour_id(self):
        return self.behaviour.get_id()

    def get_payment_execution_date(self, payment_authorisation_date_and_time: dt) -> dt:
        """
        Example (DataFrame): 2016-11-01

        Random time with range 1-3 days after Payment Authorisation Date and Time.

        :param payment_authorisation_date_and_time: Payment Authorisation Date and Time
        :return: Datetime object
        """

        day_delta = random.randint(1, 3)
        hour_delta = random.randint(1, 23)
        min_delta = random.randint(1, 59)
        sec_delta = random.randint(1, 59)
        return payment_authorisation_date_and_time + dt.timedelta(days=day_delta, hours=hour_delta, minutes=min_delta, seconds=sec_delta)

    def get_payment_modification_date_and_time(self, payment_creation_date_and_time: dt, payment_authorisation_date_and_time: dt) -> dt:
        """
        Example (DataFrame): 11/1/16 1:47 AM

        70 percent empty, 30 percent filled with a random date between payment creation date and time and payment authorisation date and time.

        :param payment_creation_date_and_time: Payment Creation Date and Time
        :param payment_authorisation_date_and_time: Payment Authorisation Date and Time
        :return: Datetime object
        """
        modification_date = self.faker.date_time_between_dates(payment_creation_date_and_time, payment_authorisation_date_and_time)

        return pd.to_datetime(random.choices([modification_date, ""], weights=(70, 30))[0])

    def get_payment_creation_date_and_time(self, payment_authorisation_date_and_time: dt) -> dt:
        """
        Example (DataFrame): 11/1/16 1:47 AM

        Random date anytime from 30 days before Payment Authorisation Date and Time.

        :param payment_authorisation_date_and_time: Payment Authorisation Date and Time
        :return: Datetime object
        """
        day_delta = random.randint(1, 30)
        hour_delta = random.randint(1, 23)
        min_delta = random.randint(1, 59)
        sec_delta = random.randint(1, 59)
        return payment_authorisation_date_and_time - dt.timedelta(days=day_delta, hours=hour_delta, minutes=min_delta, seconds=sec_delta)

    def get_payment_authorisation_date_and_time(self) -> dt:
        """
        Example (DataFrame): 11/1/16 1:47 AM

        Within range of 5 years backdated from current date.
        :return: Datetime object
        """
        return self.faker.date_time_between(start_date='-5y', end_date='now')

    def get_payment_file_format_channel(self) -> str:
        """
        Types of File Format Channels are Connexis, SWIFT and Orion2.

        :return: string
        """
        channels = ["Connexis", "SWIFT", "Orion2"]

        return random.choice(channels)

    def get_ordering_bank_code(self) -> str:
        """
        Example (DataFrame): BNPASGSGXXX

        SWIFT 11 code (need to think of how to generate wrt location).

        :return: string
        """
        return self.faker.swift11(primary=True)

    def get_ordering_account_number(self) -> str:
        """
        Example (DataFrame): 00200200223080USD

        Need to think of how to generate this.

        :return: string
        """
        return "00200200223080USD"

    def get_client_entity_name(self) -> str:
        """
        Example (DataFrame): ABC LTD

        Need to think of how to generate wrt location.

        :return: string
        """
        return self.faker.company()

    def get_beneficiary_account_number(self, beneficiary_country: str) -> str:
        """
        Example (DataFrame): XXXXXXXXX

        Length and format may vary depending on the beneficiary country/market

        :param beneficiary_country: Beneficiary Country
        :return: string
        """
        return "XXXXXXXXX"

    def get_beneficiary_name(self, beneficiary_country: str) -> str:
        """
        Example (DataFrame): ABC LTD

        Need to think of how to generate wrt location.

        :param beneficiary_country: Beneficiary Country
        :return: string
        """
        return self.faker.company()

    def get_beneficiary_address(self, beneficiary_country: str) -> str:
        """
        Example (DataFrame): XXXXXXXXX

        Need to think of how to generate wrt location.

        :param beneficiary_country: Beneficiary Country
        :return: string
        """
        return "XXXXXXXXX"

    def get_beneficiary_bank_code(self, user_country_geo_location: str) -> str:
        """
        Example (DataFrame): HBUKGB4BXXX

        Need to think of how to generate wrt location.

        :param user_country_geo_location: User Country Geo Location
        :return: string
        """
        return self.faker.swift11(primary=True)

    def get_beneficiary_country(self, beneficiary_bank_code: str) -> str:
        """
        Example (DataFrame): UK

        In ISO 2 letter country code format. Uses beneficiary bank code to derive the beneficiary code

        :param beneficiary_bank_code: Beneficiary Bank Code
        :return: string
        """
        return beneficiary_bank_code[4:6]

    def get_instruction_payment_type(self) -> str:
        """
        Types of Instruction Payment: Normal Payment, INTC Payment and Payroll
        :return: string
        """
        payment_types = ["Normal Payment", "INTC Payment", "Payroll"]

        return random.choice(payment_types)
 
    def get_payment_amount(self) -> Union[int, float]:
        """
        Example (DataFrame): 500000

        Need to check for the range and whether integer or float

        :return: int or float
        """
        l_bound = self.behaviour.payment_amount_lower_bound
        u_bound = self.behaviour.payment_amount_upper_bound
        return round(random.uniform(l_bound, u_bound), 2)

    def get_payment_currency(self, user_country_geo_location: str) -> str:
        """
        Example (DataFrame): USD

        Derives the currency from the user_country_geo_location

        :param user_country_geo_location: User Country Geo Location
        :return: string
        """
        return ccy.countryccy(user_country_geo_location)

    def get_remittance_advice(self) -> str:
        """
        Example (DataFrame): lasjhdlasjldjasdjklasdj

        Max 4x35 characters.

        :return: string
        """
        return self.faker.text(max_nb_chars=4 * 35)

    def get_connexis_user_id_maker(self) -> str:
        """
        Example (DataFrame): ASDASDA
        :return: string
        """
        return self.faker.user_name().upper()

    def get_connexis_user_id_authoriser(self) -> str:
        """
        Example (DataFrame): ASDASDA
        :return: string
        """
        return self.faker.user_name().upper()

    def get_user_country_geo_location(self) -> str:
        """
        Example (DataFrame): SG

        :return: string
        """
        return "SG"

    def get_user_last_successful_login_date_time(self, payment_authorisation_date_and_time: dt) -> str:
        """
        Example (DataFrame): 11/1/16 1:47 AM
        :param payment_authorisation_date_and_time: Payment Authorisation Date and Time
        :return: Datetime object
        """
        day_delta = random.randint(1, 15)
        hour_delta = random.randint(1, 23)
        min_delta = random.randint(1, 59)
        sec_delta = random.randint(1, 59)

        return payment_authorisation_date_and_time - dt.timedelta(days=day_delta, hours=hour_delta, minutes=min_delta, seconds=sec_delta)

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
            user_last_successful_login_date_time = self.get_user_last_successful_login_date_time(payment_authorisation_date_and_time)
            payment_creation_date_and_time = self.get_payment_creation_date_and_time(payment_authorisation_date_and_time)
            payment_modification_date_and_time = self.get_payment_modification_date_and_time(payment_creation_date_and_time,
                                                                                             payment_authorisation_date_and_time)
            payment_execution_date = self.get_payment_execution_date(payment_authorisation_date_and_time)
            payment_currency = self.get_payment_currency(user_country_geo_location)
            payment_amount = self.get_payment_amount()

            payment_file_format_channel = self.get_payment_file_format_channel()
            ordering_bank_code = self.get_ordering_bank_code()
            ordering_account_number = self.get_ordering_account_number()
            remittance_advice = self.get_remittance_advice()

            client_entity_name = self.get_client_entity_name()
            beneficiary_bank_code = self.get_beneficiary_bank_code(user_country_geo_location)
            beneficiary_country = self.get_beneficiary_country(beneficiary_bank_code)
            beneficiary_account_number = self.get_beneficiary_account_number(beneficiary_country)
            beneficiary_name = self.get_beneficiary_name(beneficiary_country)
            beneficiary_address = self.get_beneficiary_address(beneficiary_country)

            instruction_payment_type = self.get_instruction_payment_type()

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

        df['Payment Modification Date and Time'] = df['Payment Modification Date and Time'].dt.strftime('%m/%d/%Y, %H:%M %p')
        df['Payment Creation Date and Time'] = df['Payment Creation Date and Time'].dt.strftime('%m/%d/%Y, %H:%M %p')
        df['Payment Authorisation Date and Time'] = df['Payment Authorisation Date and Time'].dt.strftime('%m/%d/%Y, %H:%M %p')
        df['User last successful login date/time'] = df['User last successful login date/time'].dt.strftime('%m/%d/%Y, %H:%M %p')

        df['Payment Execution Date'] = df['Payment Execution Date'].dt.strftime('%Y-%m-%d')

        return df
