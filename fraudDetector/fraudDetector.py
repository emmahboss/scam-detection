from fraudDetector.models import *

class FraudDetector:
    def __init__(self, last_name, postcode, card_number, card_expiry):
        # sanitize input
        self.last_name = str(last_name).lower() # converts to lowercase
        self.postcode = str(postcode).replace(' ', '').upper() # remove spaces from postcode and converts to uppercase
        self.card_number = str(card_number)
        self.card_expiry = str(card_expiry)
        self.threshold = 2 # default threshold

    def changeThreshold(self, new_threshold):
        threshold = new_threshold

    def getUsersWithMatchingLastName(self):
        if not self.last_name:
            raise Exception('attribute: last_name cannot be empty string')
        
        # iexact is case-insensitive exact matching
        return User.objects.filter(last_name__iexact=self.last_name).values_list('id', flat=True)

    def getUsersWithMatchingPostcode(self):
        if not self.postcode:
            raise Exception('attribute: postcode cannot be empty string')
        
        # this filter does a table join between User and Address
        # iexact is case-insensitive exact matching
        return User.objects.filter(address__postcode__iexact=self.postcode).values_list('id', flat=True)

    def getUsersWithMatchingCreditCard(self):
        if not self.card_number:
            raise Exception('attribute: card_number cannot be empty string')
        
        if not self.card_expiry:
            raise Exception('attribute: card_expiry cannot be empty string')

        # sanitize
        last_four_digits = self.card_number[-4:] # get last 4 digits of card number

        card_expiry = self.card_expiry.split('/')
        expiry_month = card_expiry[0]
        expiry_year = card_expiry[1]
        if len(expiry_month) < 2:
            expiry_month = '0' + expiry_month
        
        if len(expiry_year) > 2:
            expiry_year = expiry_year[-2:] # get last two digits of the year

        return User.objects.filter(
            creditcard__last_four_digits__exact=last_four_digits
            ).filter(
                creditcard__expiry_month__exact=expiry_month
            ).filter(
                creditcard__expiry_year__exact=expiry_year
            ).values_list(
                'id', flat=True)

    def isFradulent(self):
        # assume that entries in DB are already sanitized and therefore consistent
        # 1. address.postcode does not have spaces, letters are uppercase
        # 2. creditcard.last_four_digits is 4 digits (last 4 digits of card)
        # 3. creditcard.expiry_month is 2 digits (includes leading 0 for single digit months)
        # 4. creditcard.expiry_year is 2 digits (includes leading 0 for single digit years)
        
        # assume that FraudDetector class receives unsanitized input from a client-side form that won't submit unless fields are populated
        # 1. card expiry in any of these forms: 1/12, 01/12, 1/2012, 01/2012
        # 2. postcode with or without spaces
        # 3. last name with caps or no caps, no special characters or numbers allowed

        last_name_user_set = set(self.getUsersWithMatchingLastName())
        postcode_user_set = set(self.getUsersWithMatchingPostcode())
        creditcard_user_set = set(self.getUsersWithMatchingCreditCard())

        if ((last_name_user_set & postcode_user_set) or (last_name_user_set & creditcard_user_set) or (postcode_user_set & creditcard_user_set)):
            return True

        return False