class Person:
    def __init__(self, name, id_number):
        self.name = name
        self.id_number = id_number

    def change_name(self, new_name):
        self.name = new_name
        return f"Name changed to: {self.name}"

    def display_info(self):
        return f"Person Info - Name: {self.name}, ID: {self.id_number}"

    @staticmethod
    def from_string(person_string):
        name, id_number = person_string.split(',')
        return Person(name.strip(), id_number.strip())


class Account:
    def __init__(self, balance=0):
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    def check_balance(self):
        return f"Current balance: {self.__balance}"

    def display_info(self):
        return f"Account Info - Balance: {self.__balance}"

    @staticmethod
    def create_account(initial_balance=0):
        return Account(initial_balance)


class User(Person):
    def __new__(cls, name, id_number, phone_number):
        instance = super(User, cls).__new__(cls)
        if not instance.is_valid_phone_number(phone_number):
            raise ValueError("Phone number must be a 10-digit number.")
        return instance

    def __init__(self, name, id_number, phone_number):
        super().__init__(name, id_number)
        self.phone_number = phone_number

    def is_valid_phone_number(self, phone_number):
        return len(phone_number) == 10 and phone_number.isdigit()

    def display_info(self):
        return f"User Info - Name: {self.name}, ID: {self.id_number}, Phone: {self.phone_number}"

    @staticmethod
    def validate_phone_number(phone_number):
        return len(phone_number) == 10 and phone_number.isdigit()


class UserAccount(User, Account):
    accounts = {}

    def __new__(cls, name, id_number, phone_number, initial_balance=0, limit=500):
        if id_number in cls.accounts:
            return cls.accounts[id_number]

        # Create a new instance of UserAccount
        instance = super(UserAccount, cls).__new__(cls, name, id_number, phone_number)
        cls.accounts[id_number] = instance
        return instance

    def __init__(self, name, id_number, phone_number, initial_balance=0, limit=500):
        User.__init__(self, name, id_number, phone_number)  # Initialize User
        Account.__init__(self, initial_balance)  # Initialize Account
        self.__limit = limit
        self.is_frozen = False

    @property
    def limit(self):
        return self.__limit

    def print_statement(self):
        return f"Account Statement: {self.display_info()}"

    def deposit(self, amount):
        if amount > 0:
            self._Account__balance += amount
            return f"Deposited: {amount}. New balance: {self.balance}."
        return "Deposit amount must be positive."

    def withdraw(self, amount):
        if self.is_frozen:
            return "Account is frozen. No transactions are allowed."

        if 0 < amount <= self.balance:
            self._Account__balance -= amount
            return f"Withdrew: {amount}. New balance: {self.balance}."
        if amount > self.limit:
            self.is_frozen = True
            return "Transaction limit exceeded. The account has been frozen."
        return "Insufficient funds or invalid amount."

    def display_info(self):
        return f"UserAccount Info - Name: {self.name}, ID: {self.id_number}, Balance: {self.balance}, Limit: {self.limit}, Frozen: {self.is_frozen}"

    @staticmethod
    def get_account_by_id(id_number):
        return UserAccount.accounts.get(id_number, None)


class Admin(Person):
    def __init__(self, name, id_number):
        super().__init__(name, id_number)

    def block_account(self, user_account):
        if user_account.is_frozen:
            return "Account is already frozen."
        user_account.is_frozen = True
        return f"Account of {user_account.name} has been blocked."

    def unblock_account(self, user_account):
        if not user_account.is_frozen:
            return "Account is not frozen."
        user_account.is_frozen = False
        return f"Account of {user_account.name} has been unblocked."

    def display_info(self):
        return f"Admin Info - Name: {self.name}, ID: {self.id_number}"
if __name__ == "__main__":
    user1 = User("Alice Smith", "U001", "5551234567")
    user_account1 = UserAccount("Alice Smith", "U001", "5551234567", initial_balance=1000, limit=500)
    person1 = Person("Nill", "123")
    admin = Admin("Admin1", "A001")  # Fixed the initialization here
    new_person = Person.from_string("John Doe, P002")
    new_account = Account.create_account(500)
    valid_phone = User.validate_phone_number("1234567890")
    account_by_id = UserAccount.get_account_by_id("U001")
    print(new_person.display_info())
    print(new_account.display_info())
    print(f"Is valid phone: {valid_phone}")
    print(account_by_id.display_info() if account_by_id else "Account not found")
    print(person1.display_info())
    print(person1.change_name("Marie"))
    print(person1.display_info())
    print(user1.display_info())
    print(user_account1.print_statement())
    print(user_account1.deposit(200))
    print(user_account1.print_statement())
    print(user_account1.withdraw(300))
    print(user_account1.print_statement())
    print(admin.block_account(user_account1))
    print(user_account1.print_statement())
    print(admin.unblock_account(user_account1))
    print(user_account1.print_statement())
    person1.display_info()
    user1.display_info()
    user_account1.display_info()
    admin.display_info()
