# charger type c but phone support type a => then you get adapter
# act as a bridge between 2 systems
class BankService:
    def make_payment(self, amount):
        print(f"Processing payment of ${amount} through Bankservice")


# Interface 
class PaymentService:
    def pay(self, amount):
        pass


# Adapter
class BankServiceAdapter(PaymentService):
    def __init__(self, bank_service: BankService):
        self.bank_service = bank_service
    
    def pay(self, amount):
        self.bank_service.make_payment(amount)


# Client code: expects a 'pay(amount)' method  
def process_payment(payment_service, amount):
    payment_service.pay(amount)


bank_service = BankService()
process_payment(bank_service, 100)  # This throw an error

# but we can not modify the main bankservice because what if it is coming from 
# third party
bank_service_adapter = BankServiceAdapter(BankService)
process_payment(bank_service_adapter, 100)  # This throw an error

# pro - reusability is high
# flexibity
# non - invasive

# cons - complexity
# overhead

# usage - integrating api's - but there interfaces does not align
# ui components
