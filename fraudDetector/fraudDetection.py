class User:
    def __init_(self, last_name, address, credit_card):
        self.last_name = last_name
        self.address = address
        self.credit_card = credit_card

class Address:
    def __init__(self, user_id, postcode):
        self.user_id = user_id
        self.postcode = postcode

class CreditCard:
    def __init__(self, last_four_digits, expiry_month, expiry_year):
        self.last_four_digits = last_four_digits
        self.expiry_month = expiry_month
        self.expiry_year = expiry_year

class FraudDetector:
    def __init__(self, last_name, postcode, card_number, card_expiry):
        self.last_name = last_name
        self.postcode = postcode
        self.card_number = card_number
        self.card_expiry = card_expiry
        self.threshold = 2 # default threshold

    def changeThreshold(self, new_threshold):
        threshold = new_threshold

    def retrieveUser(self):
        

    # 1. check last name
    # 2. check postcode
    # 3. check credit card (match both last 4 digits and expiry)
    # if 2 or more match, then return true
    # else return false
    def isFradulent(self):


