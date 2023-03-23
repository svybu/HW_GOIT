from collections import UserList


class AmountPaymentList(UserList):
    def amount_payment(self):
        sum = 0
        for value in self:
            if value > 0:
                sum = sum + value
        return sum



