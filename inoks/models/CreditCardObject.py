class CreditCardObject(object):

    def __init__(self, id, cardNumber, cvv, name, card_name_lastName):
        self.id = id
        self.cardNumber = cardNumber
        self.name = name
        self.cvv = cvv
        self.card_name_lastName = card_name_lastName
