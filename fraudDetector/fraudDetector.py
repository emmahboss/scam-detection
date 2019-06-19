from fraudDetector.models import *

class FraudDetector:
    def __init__(self, last_name, postcode, card_number, card_expiry):
        # sanitize input
        self.last_name = str(last_name).lower() # converts to lowercase
        self.postcode = str(postcode).replace(' ', '').upper() # remove spaces from postcode and converts to uppercase
        self.card_number = card_number
        self.card_expiry = str(card_expiry)
        self.threshold = 2 # default threshold

    def changeThreshold(self, new_threshold):
        threshold = new_threshold

    def getUsersWithMatchingLastName(self):
        if not self.last_name:
            raise Exception('attribute: last_name cannot be empty string')
        
        # iexact is case-insensitive exact matching
        return User.objects.filter(last_name__iexact=self.last_name)

    def getUsersWithMatchingPostcode(self):
        if not self.postcode:
            raise Exception('attribute: postcode cannot be empty string')
        
        # this filter does a table join between User and Address
        # iexact is case-insensitive exact matching
        return User.objects.filter(address__postcode__iexact=self.postcode)

    def isFradulent(self):
        # assume that entries in DB are already sanitized and therefore consistent:
        # 1. address.postcode does not have spaces, letters are uppercase
        # 2. creditcard.last_four_digits is 4 digits (last 4 digits of card)
        # 3. creditcard.expiry_month is 2 digits (includes leading 0 for single digit months)
        # 4. creditcard.expiry_year is 2 digits (includes leading 0 for single digit years)
        # assume that FraudDetector class receives unsanitized input from front-end form

        
