from app.calculations import (
    BankAccount,
    InsufficientFunds,
    add,
    subtract,
    multiply,
    divide,
)
import pytest


@pytest.mark.parametrize("num1,num2,expected", [(1, 4, 5), (2, 4, 6)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_subtract():
    assert subtract(5, 3) == 2


def test_multiply():
    assert multiply(5, 3) == 15


def test_divide():
    assert round(divide(5, 3), 2) == 1.67


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(100)


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 100


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_bank_withdraw_amount(bank_account):
    bank_account.withdraw(50)
    assert bank_account.balance == 50


def test_bank_deposit_amount(bank_account):
    bank_account.deposit(50)
    assert bank_account.balance == 150


def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()
    assert int(bank_account.balance) == 110


@pytest.mark.parametrize(
    "deposited,withdraw,expected",
    [(200, 100, 100), (50, 10, 40), (90, 40, 50)],
)
def test_bank_transaction(zero_bank_account, deposited, withdraw, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(zero_bank_account):
    with pytest.raises(InsufficientFunds):
        zero_bank_account.withdraw(100)
