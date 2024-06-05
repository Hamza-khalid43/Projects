import json
from abc import ABC, abstractmethod
import time


def delay_printing(x):
    for i in x:
        print(i, end='', flush=True)
        time.sleep(0.3)
    print()


class DataHandling:
    def __init__(self):
        self.data = {}

    def load_data(self):
        with open('accounts_data.json', 'r') as file:
            self.data = json.load(file)

    def save_data(self):
        with open('accounts_data.json', 'w') as file:
            json.dump(self.data, file)


class Account(ABC):
    def __init__(self, ins, user_name, date, balance=0):
        self.ins = ins
        self.user_name = user_name
        self.date = date
        self.balance = balance

    @abstractmethod
    def withdraw(self):
        pass

    @abstractmethod
    def deposit(self):
        pass

    def get_date(self):
        datee = input('Enter the date (DD/MM/YYYY): ')
        datee = datee.split('/')
        self.current_date = {
            'day': int(datee[0]),
            'month': int(datee[1]),
            'year': int(datee[2])
        }

    def time_interval(self, current_date):
        self.current_date = current_date
        interval = (self.current_date['year'] - self.ins.data[self.user_name]['date']['year']) * 12
        interval += (self.current_date['month'] - self.ins.data[self.user_name]['date']['month'])
        return interval


class CheckingAccount(Account):
    fee = 1000

    def __init__(self, ins, user_name, date, balance=0, credit_pending=0, credit_limit=10000):
        super().__init__(ins, user_name, date, balance)
        self.credit_pending = credit_pending
        self.credit_limit = credit_limit

    def deposit(self):
        self.amount = int(input('ENTER THE AMOUNT YOU WANT TO DEPOSIT: '))
        if self.credit_pending > 0:
            if self.credit_pending <= 10000 and self.amount >= (self.credit_pending + CheckingAccount.fee):
                self.balance += (self.amount - self.credit_pending)
                self.credit_pending = 0
            elif self.amount >= CheckingAccount.fee:
                self.credit_pending -= self.amount
            else:
                print('The amount you want to deposit is too less. Kindly deposit a greater amount.')
        else:
            self.balance += self.amount
        self.ins.data[self.user_name]['transactions'].append(f"you deposited Rs{self.amount} on {self.date['day']}/{self.date['month']}/{self.date['year']}.")

    def withdraw(self):
        self.amount = int(input('ENTER AMOUNT YOU WANT TO WITHDRAW: '))
        if self.amount <= self.balance:
            self.balance -= self.amount
        elif self.amount >= self.balance and self.amount <= (self.balance + self.credit_limit) and self.credit_pending <= 10000:
            self.credit_pending = (self.amount - self.balance) + CheckingAccount.fee
            self.balance = 0
        else:
            print('YOU HAVE INSUFFICIENT BALANCE')
        self.ins.data[self.user_name]['transactions'].append(
            f"you withdraw Rs{self.amount} on {self.date['day']}/{self.date['month']}/{self.date['year']}.")

    def update(self):
        self.ins.data[self.user_name].update({
            'balance': self.balance,
            'credit_pending': self.credit_pending,
            'credit_limit': self.credit_limit
        })


class SavingsAccount(Account):
    possible_withdrawals = 6

    def __init__(self, ins, user_name, date, balance=0, withdrawals=0, interest_rate=0.583):
        super().__init__(ins, user_name, date, balance)
        self.withdrawals = withdrawals
        self.interest_rate = interest_rate
        if self.user_name in self.ins.data:
            self.interval = Account.time_interval(self, date)
        else:
            self.interval = 0
        SavingsAccount.withdraw_reset(self)
        SavingsAccount.add_interest(self)

    def deposit(self):
        self.amount = int(input('ENTER THE AMOUNT YOU WANT TO DEPOSIT: '))
        self.balance += self.amount
        self.ins.data[self.user_name]['transactions'].append(
            f"you deposited Rs{self.amount} on {self.date['day']}/{self.date['month']}/{self.date['year']}.")

    def withdraw(self):
        if self.withdrawals < SavingsAccount.possible_withdrawals:
            amount = int(input('ENTER THE AMOUNT YOU WANT TO WITHDRAW: '))
            self.balance -= amount
            self.withdrawals += 1
        else:
            print('You reached your monthly withdrawal limit.')
        self.ins.data[self.user_name]['transactions'].append(
            f"you withdraw Rs{self.amount} on {self.date['day']}/{self.date['month']}/{self.date['year']}.")

    def withdraw_reset(self):
        if self.interval >= 1:
            self.withdrawals = 0

    def add_interest(self):
        if self.interval > 0:
            self.balance += ((self.balance * self.interest_rate) * self.interval)
        else:
            print('You didn\'t hit the minimum requirement to earn interest.')

    def update(self):
        self.ins.data[self.user_name].update({
            'date':{
                'day':self.date['day'],
                'month':self.date['month'],
                'year':self.date['year']
            },
            'balance': self.balance,
            'withdrawals': self.withdrawals,
            'interest_rate': self.interest_rate
        })


class LoanAccount(Account):
    def __init__(self, ins, user_name, date, balance=0, principal_amount=0, interest_rate=0.1, loan_duration=0):
        super().__init__(ins, user_name, date, balance)
        self.principal_amount = principal_amount
        self.interest_rate = interest_rate
        self.loan_duration = loan_duration
        if self.user_name in self.ins.data:
            self.interval = Account.time_interval(self, date)
        else:
            self.interval = 0
        LoanAccount.late_fee(self)

    def withdraw(self):
        self.amount = int(input('ENTER AMOUNT YOU WANT TO WITHDRAW: '))
        self.balance -= self.amount
        self.ins.data[self.user_name]['transactions'].append(
            f"you deposited Rs{self.amount} on {self.date['day']}/{self.date['month']}/{self.date['year']}.")

    def loan_add(self):
        amount = int(input('HOW MUCH LOAN DO YOU WANT? '))
        self.balance = amount
        self.principal_amount += ((self.balance) + (amount * self.interest_rate))
        self.loan_duration = 12

    def deposit(self):
        amount = int(input('HOW MUCH AMOUNT DO YOU WANT TO PAY: '))
        self.principal_amount -= amount
        if self.principal_amount == 0:
            self.loan_duration = 0
        else:
            self.loan_duration -= self.interval
        self.ins.data[self.user_name]['transactions'].append(
            f"you payed loan of Rs{self.amount} on {self.date['day']}/{self.date['month']}/{self.date['year']}.")

    def late_fee(self):
        if self.interval >= 12:
            self.principal_amount += 5000

    def update(self):
        self.ins.data[self.user_name].update({
            'date': {
                'day': self.date['day'],
                'month': self.date['month'],
                'year': self.date['year']
            },
            'L.balance': self.balance,
            'L.principal_amount': self.principal_amount,
            'L.interest_rate': self.interest_rate,
            'L.loan_duration': self.loan_duration
        })


class Customer:
    def set_customer(self, ins):
        self.ins = ins
        self.name = input('Enter your name: ')
        self.user_name = input('Enter a unique user name: ')
        self.password = input('Enter a unique password: ')
        self.address = input('Enter your address: ')

    def verification(self):
        print('Verifying the given information', end='')
        delay_printing('!!!!!!!')
        delay_printing('-_-_-_-_-_-_-_-_-_-_-_-')
        if self.user_name in self.ins.data and self.ins.data[self.user_name]['user_name'] == self.user_name:
            return True
        else:
            return False

    def choosing_account(self):
        print('Select the type of account you want:')
        print('1. Checking Account')
        print('2. Savings Account')
        self.account_type = int(input())
        if self.account_type == 1:
            self.account_type = 'checking account'
        else:
            self.account_type = 'savings account'

    def get_date(self):
        datee = input('Enter the date (DD/MM/YYYY): ')
        datee = datee.split('/')
        self.current_date = {
            'day': int(datee[0]),
            'month': int(datee[1]),
            'year': int(datee[2])
        }

    def updating(self):
        self.ins.data.update({
            self.user_name: {
                'name': self.name,
                'password': self.password,
                'account_type': self.account_type,
                'date': self.current_date,
                'transactions': []
            }
        })


class Admin:
    def __init__(self):
        self.f = DataHandling()
        self.f.load_data()
        print('What do you want?')
        print('1. A report on all customers')
        print('2. A report on a particular customer')
        self.choice = int(input())
        print('Loading Data', flush=True)
        delay_printing('.......')
        if self.choice == 1:
            for key, values in self.f.data.items():
                print(f'User Name: {key}')
                for key1, values1 in values.items():
                    print(f'{key1}: {values1}')
        else:
            self.username = input('Enter the user name of the customer you want a report on: ')
            if self.username in self.f.data:
                for key, values in self.f.data[self.username].items():
                    print(f'{key}: {values}')
            else:
                print(f"The customer with user name '{self.username}' was not found!")


class Start:
    def __init__(self):
        self.f2 = DataHandling()
        self.f2.load_data()
        print('------------------SHELBY BANKING LIMITED------------------')
        print('--------------------------WELCOME--------------------------')
        print('ARE YOU')
        delay_printing('?????')
        print('1. NEW CUSTOMER')
        print('2. OLD CUSTOMER')
        print('3. ADMIN')
        self.choice = int(input())
        self.open1()
        self.open2()
        self.open3()

    def open1(self):
        if self.choice == 1:
            print('GIVE US YOUR AUTHENTIC CREDENTIALS')
            c = Customer()
            c.set_customer(self.f2)
            c1 = c.verification()
            while c1:
                print('THE USERNAME HAS ALREADY BEEN TAKEN. TRY ANOTHER ONE.')
                c.set_customer(self.f2)
                c1 = c.verification()
            print('CAN YOU TELL US WHAT DATE IS TODAY?')
            c.get_date()
            print('ACCOUNT SELECTION')
            c.choosing_account()
            if c.account_type == 'checking account':
                self.account = CheckingAccount(self.f2, c.user_name, c.current_date)
            else:
                self.account = SavingsAccount(self.f2, c.user_name, c.current_date)
            c.updating()
            self.account.update()
            self.f2.save_data()
            print('CONGRATULATIONS! YOU HAVE OPENED YOUR ACCOUNT IN SHELBY BANKING LIMITED')
            self.choice = 2
        self.f2.save_data()

    def open2(self):
        c = Customer()
        c.get_date()
        if self.choice == 2:
            print('FOR SIGN UP, GIVE US YOUR USER NAME AND PASSWORD')
            self.user_name = input('USER NAME: ')
            self.password = input('PASSWORD: ')
            if self.user_name in self.f2.data and self.password == self.f2.data[self.user_name]['password']:
                self.account_type = self.f2.data[self.user_name]['account_type']
                if self.account_type == 'checking account':
                    self.account_type = CheckingAccount(
                        self.f2, self.user_name, self.f2.data[self.user_name]['date'],
                        self.f2.data[self.user_name]['balance'], self.f2.data[self.user_name]['credit_pending']
                    )
                    print('WHAT DO YOU WANT TO DO?')
                    print('1. DEPOSIT')
                    print('2. WITHDRAW')
                    print('3. GET LOAN')
                    self.action = int(input())
                    if self.action == 1:
                        self.account_type.deposit()
                        self.account_type.update()
                    elif self.action == 2:
                        self.account_type.withdraw()
                        self.account_type.update()
                    else:
                        print(f'FOR MAKING LOAN ACCOUNT')
                        c.set_customer(self.f2)
                        self.l = LoanAccount(self.f2, c.user_name, c.current_date,)
                        self.l.loan_add()
                        c.account_type = 'loan_account'
                        c.updating()
                        self.l.update()
                elif self.account_type == 'savings account':
                    self.account_type = SavingsAccount(
                        self.f2, self.user_name, c.current_date,
                        self.f2.data[self.user_name]['balance'], self.f2.data[self.user_name]['withdrawals']
                    )
                    print('WHAT DO YOU WANT TO DO?')
                    print('1. DEPOSIT')
                    print('2. WITHDRAW')
                    print('3. GET LOAN')
                    self.action = int(input())
                    if self.action == 1:
                        self.account_type.deposit()
                        self.account_type.update()
                    elif self.action == 2:
                        self.account_type.withdraw()
                        self.account_type.update()
                    else:
                        print(f'FOR MAKING LOAN ACCOUNT')
                        c.set_customer(self.f2)
                        self.l = LoanAccount(self.f2, c.user_name, c.current_date)
                        self.l.loan_add()
                        c.account_type = 'loan_account'
                        self.l.update()
                else:
                    self.account_type = LoanAccount(
                        self.f2, self.user_name, c.current_date,
                        self.f2.data[self.user_name]['L.balance'],
                        self.f2.data[self.user_name]['L.principal_amount'],
                        self.f2.data[self.user_name]['L.interest_rate'],
                        self.f2.data[self.user_name]['L.loan_duration']
                    )
                    print('WHAT DO YOU WANT TO DO?')
                    print('1. PAY LOAN')
                    print('2. WITHDRAW LOAN')
                    self.action = int(input())
                    if self.action == 1:
                        self.account_type.deposit()
                        self.account_type.update()
                    else:
                        self.account_type.withdraw()
                        self.account_type.update()
        self.f2.save_data()

    def open3(self):
        if self.choice == 3:
            a = Admin()
        self.f2.save_data()


s = Start()
