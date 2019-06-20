from django.test import TestCase
from fraudDetector.models import *
from fraudDetector.fraudDetector import *

class FraudDetectorTests(TestCase):
    last_name = 'Test'
    discount_code = '12345'
    postcode = 'A1B2C3'
    last_four_digits= '1234'
    expiry_month = '01'
    expiry_year = '23'

    def setUp(self):
        user = User.objects.create(last_name=self.last_name, discount_code=self.discount_code)
        Address.objects.create(user_id=user, postcode=self.postcode)
        CreditCard.objects.create(user_id=user, last_four_digits=self.last_four_digits, expiry_month=self.expiry_month, expiry_year=self.expiry_year)
    
    # test cases for getUsersWithMatchingLastName()
    def test_getUsersWithMatchingLastName_single(self):
        fd = FraudDetector(self.last_name, self.postcode, '', '')
        users = fd.getUsersWithMatchingLastName()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], 1)
    
    def test_getUsersWithMatchingLastName_multiple(self):
        user2 = User.objects.create(last_name=self.last_name, discount_code=self.discount_code)
        Address.objects.create(user_id=user2, postcode=self.postcode)
        CreditCard.objects.create(user_id=user2, last_four_digits=self.last_four_digits, expiry_month=self.expiry_month, expiry_year=self.expiry_year)

        fd = FraudDetector(self.last_name, self.postcode, '', '')
        users = fd.getUsersWithMatchingLastName()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0], 1)
        self.assertEqual(users[1], 2)

    def test_getUsersWithMatchingLastName_lowercase(self):
        fd = FraudDetector('test', self.postcode, '', '')
        users = fd.getUsersWithMatchingLastName()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], 1)

    def test_getUsersWithMatchingLastName_uppercase(self):
        fd = FraudDetector('TEST', self.postcode, '', '')
        users = fd.getUsersWithMatchingLastName()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], 1)

    def test_getUsersWithMatchingLastName_mix(self):
        fd = FraudDetector('TeSt', self.postcode, '', '')
        users = fd.getUsersWithMatchingLastName()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], 1)

    # test cases for getUsersWithMatchingPostcode()
    def test_getUsersWithMatchingPostcode_no_spaces_single(self):
        fd = FraudDetector(self.last_name, self.postcode, '', '')
        users = fd.getUsersWithMatchingPostcode()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], 1)

    def test_getUsersWithMatchingPostcode_no_spaces_multiple(self):
        user2 = User.objects.create(last_name=self.last_name, discount_code=self.discount_code)
        Address.objects.create(user_id=user2, postcode=self.postcode)
        CreditCard.objects.create(user_id=user2, last_four_digits=self.last_four_digits, expiry_month=self.expiry_month, expiry_year=self.expiry_year)

        fd = FraudDetector('Test2', self.postcode, '', '')
        users = fd.getUsersWithMatchingPostcode()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0], 1)
        self.assertEqual(users[1], 2)

    def test_getUsersWithMatchingPostcode_with_spaces(self):
        fd = FraudDetector(self.last_name, 'A1B 2C3', '', '')
        users = fd.getUsersWithMatchingPostcode()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], 1)

    def test_getUsersWithMatchingPostcode_lowercase(self):
        fd = FraudDetector(self.last_name, 'a1b2c3', '', '')
        users = fd.getUsersWithMatchingPostcode()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], 1)

    # test cases for getUsersWithMatchingCreditCard()
    def test_getUsersWithMatchingCreditCard_full_card(self):
        fd = FraudDetector(self.last_name, self.postcode, '1234 1234 1234 1234 1234', self.expiry_month + '/' + self.expiry_year)
        users = fd.getUsersWithMatchingCreditCard()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], 1)

    def test_getUsersWithMatchingCreditCard_last_four_digits_single(self):
        fd = FraudDetector(self.last_name, self.postcode, self.last_four_digits, self.expiry_month + '/' + self.expiry_year)
        users = fd.getUsersWithMatchingCreditCard()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], 1)

    def test_getUsersWithMatchingCreditCard_last_four_digits_multiple(self):
        user2 = User.objects.create(last_name=self.last_name, discount_code=self.discount_code)
        Address.objects.create(user_id=user2, postcode=self.postcode)
        CreditCard.objects.create(user_id=user2, last_four_digits=self.last_four_digits, expiry_month=self.expiry_month, expiry_year=self.expiry_year)

        fd = FraudDetector(self.last_name, self.postcode, self.last_four_digits, self.expiry_month + '/' + self.expiry_year)
        users = fd.getUsersWithMatchingCreditCard()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0], 1)
        self.assertEqual(users[1], 2)

    def test_getUsersWithMatchingCreditCard_card_expiry_MM_YYYY(self):
        fd = FraudDetector(self.last_name, self.postcode, self.last_four_digits, '01/2023')
        users = fd.getUsersWithMatchingCreditCard()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], 1)

    def test_getUsersWithMatchingCreditCard_card_expiry_M_YYYY(self):
        fd = FraudDetector(self.last_name, self.postcode, self.last_four_digits, '1/2023')
        users = fd.getUsersWithMatchingCreditCard()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], 1)

    def test_getUsersWithMatchingCreditCard_card_expiry_M_YY(self):
        fd = FraudDetector(self.last_name, self.postcode, self.last_four_digits, '1/23')
        users = fd.getUsersWithMatchingCreditCard()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], 1)
    
    # test cases for isFradulent()
    def test_isFradulent_matching_last_name_and_postcode(self):
        user2 = User.objects.create(last_name=self.last_name, discount_code=self.discount_code)
        Address.objects.create(user_id=user2, postcode=self.postcode)
        CreditCard.objects.create(user_id=user2, last_four_digits='9999', expiry_month='99', expiry_year='99')

        fd = FraudDetector(self.last_name, self.postcode, self.last_four_digits, self.expiry_month + '/' + self.expiry_year)
        self.assertEqual(fd.isFradulent(), True)

    def test_isFradulent_matching_last_name_and_creditcard(self):
        user2 = User.objects.create(last_name=self.last_name, discount_code=self.discount_code)
        Address.objects.create(user_id=user2, postcode='54321')
        CreditCard.objects.create(user_id=user2, last_four_digits=self.last_four_digits, expiry_month=self.expiry_month, expiry_year=self.expiry_year)

        fd = FraudDetector(self.last_name, self.postcode, self.last_four_digits, self.expiry_month + '/' + self.expiry_year)
        self.assertEqual(fd.isFradulent(), True)

    def test_isFradulent_matching_postcode_and_creditcard(self):
        user2 = User.objects.create(last_name='asdf', discount_code=self.discount_code)
        Address.objects.create(user_id=user2, postcode=self.postcode)
        CreditCard.objects.create(user_id=user2, last_four_digits=self.last_four_digits, expiry_month=self.expiry_month, expiry_year=self.expiry_year)

        fd = FraudDetector(self.last_name, self.postcode, self.last_four_digits, self.expiry_month + '/' + self.expiry_year)
        self.assertEqual(fd.isFradulent(), True)

    def test_isFradulent_matching_last_name_and_postcode_and_creditcard(self):
        user2 = User.objects.create(last_name=self.last_name, discount_code=self.discount_code)
        Address.objects.create(user_id=user2, postcode=self.postcode)
        CreditCard.objects.create(user_id=user2, last_four_digits=self.last_four_digits, expiry_month=self.expiry_month, expiry_year=self.expiry_year)

        fd = FraudDetector(self.last_name, self.postcode, self.last_four_digits, self.expiry_month + '/' + self.expiry_year)
        self.assertEqual(fd.isFradulent(), True)

    def test_isFradulent_matches_only_last_name(self):
        new_postcode = '54321'
        new_last_four_digits = '9999'
        new_expiry_month = new_expiry_year = '99'

        fd = FraudDetector(self.last_name, new_postcode, new_last_four_digits, new_expiry_month + '/' + new_expiry_year)
        self.assertEqual(fd.isFradulent(), False)

    def test_isFradulent_matches_only_postcode(self):
        new_last_name = 'asdf'
        new_last_four_digits = '9999'
        new_expiry_month = new_expiry_year = '99'

        fd = FraudDetector(new_last_name, self.postcode, new_last_four_digits, new_expiry_month + '/' + new_expiry_year)
        self.assertEqual(fd.isFradulent(), False)

    def test_isFradulent_matches_only_creditcard(self):
        new_last_name = 'asdf'
        new_postcode = '54321'

        fd = FraudDetector(new_last_name, new_postcode, self.last_four_digits, self.expiry_month + '/' + self.expiry_year)
        self.assertEqual(fd.isFradulent(), False)