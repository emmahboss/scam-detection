from fraudDetector.models import *

class FraudDetector:
    def __init__(self, last_name, postcode, card_number, card_expiry):
        if not last_name or not postcode or not card_number or not card_expiry:
            raise ValueError('FraudDetector constructor attributes cannot be empty')

        # sanitize input
        self.last_name = str(last_name).lower() # converts to lowercase
        self.postcode = str(postcode).replace(' ', '').upper() # remove spaces from postcode and converts to uppercase
        if len(card_number) < 4:
            raise ValueError('card_number attribute cannot be less than 4 digits long')
        self.card_number = str(card_number)[-4:] # get last 4 digits of card
        self.card_expiry = str(card_expiry)
        self.threshold = 2 # default threshold

    def changeThreshold(self, new_threshold):
        threshold = new_threshold

    def getUsersWithMatchingLastName(self):
        # iexact is case-insensitive exact matching
        return User.objects.filter(last_name__iexact=self.last_name).values_list('id', flat=True)

    def getUsersWithMatchingPostcode(self):
        # this filter does a table join between User and Address
        # iexact is case-insensitive exact matching
        return User.objects.filter(address__postcode__iexact=self.postcode).values_list('id', flat=True)

    def getUsersWithMatchingCreditCard(self):
        # separate card expiry to expiry month and expiry year
        card_expiry = self.card_expiry.split('/')
        expiry_month = card_expiry[0]
        expiry_year = card_expiry[1]
        if len(expiry_month) < 2:
            expiry_month = '0' + expiry_month
        
        if len(expiry_year) > 2:
            expiry_year = expiry_year[-2:] # get last two digits of the year

        # filter by matching credit card number AND expiry dates
        return User.objects.filter(
            creditcard__last_four_digits__exact=self.card_number
            ).filter(
                creditcard__expiry_month__exact=expiry_month
            ).filter(
                creditcard__expiry_year__exact=expiry_year
            ).values_list(
                'id', flat=True)

    def isFradulent(self):
        # assume that entries in DB are already sanitized and therefore consistent
        # 1. address.postcode does not have spaces; letters are uppercase
        # 2. creditcard.expiry_month is 2 digits (includes leading 0 for single digit months)
        # 3. creditcard.expiry_year is 2 digits (includes leading 0 for single digit years)
        
        # assume that FraudDetector class receives unsanitized input from a client-side form that won't submit unless fields are populated with correct type
        # 1. card expiry in any of these forms: 1/12, 01/12, 1/2012, 01/2012 and not gibberish
        # 2. postcode with or without spaces
        # 3. last name with caps or no caps, no special characters or numbers allowed

        last_name_user_set = set(self.getUsersWithMatchingLastName())
        postcode_user_set = set(self.getUsersWithMatchingPostcode())
        creditcard_user_set = set(self.getUsersWithMatchingCreditCard())

        # set intersection to determine if 2 sets contain the same user
        if ((last_name_user_set & postcode_user_set) or (last_name_user_set & creditcard_user_set) or (postcode_user_set & creditcard_user_set)):
            return True

        return False