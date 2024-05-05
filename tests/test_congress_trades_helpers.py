import pytest
import pandas as pd
from datetime import datetime, timedelta
from ..utils.congress_trades_helpers import calc_gains


def test_buy_only():
    trades = pd.DataFrame(
        {
            "Transaction": ["Purchase"],
            "Amount": [1000],
            "trade_price": [100],
            "current_price": [300],
            "TransactionDate": [datetime.now() - timedelta(3)],
        }
    )
    realized_gains, unrealized_gains = calc_gains(trades)
    assert realized_gains == None
    assert unrealized_gains == 200


def test_sell_only():
    trades = pd.DataFrame(
        {
            "Transaction": ["Sell"],
            "Amount": [1000],
            "trade_price": [100],
            "current_price": [300],
            "TransactionDate": [datetime.now() - timedelta(3)],
        }
    )
    realized_gains, unrealized_gains = calc_gains(trades)
    assert realized_gains == None
    assert unrealized_gains == None


def test_buy_sell_round_trip():
    trades = pd.DataFrame(
        {
            "Transaction": ["Purchase", "Sale"],
            "Amount": [1000, 1000],
            "trade_price": [100, 200],
            "current_price": [300, 300],
            "TransactionDate": [
                datetime.now() - timedelta(3),
                datetime.now() - timedelta(2),
            ],
        }
    )
    realized_gains, unrealized_gains = calc_gains(trades)
    assert realized_gains == 100
    assert unrealized_gains == 200


def test_sell_buy_round_trip():
    trades = pd.DataFrame(
        {
            "Transaction": ["Sale", "Purchase"],
            "Amount": [1000, 1000],
            "trade_price": [100, 200],
            "current_price": [300, 300],
            "TransactionDate": [
                datetime.now() - timedelta(3),
                datetime.now() - timedelta(2),
            ],
        }
    )
    realized_gains, unrealized_gains = calc_gains(trades)
    assert realized_gains == None
    assert unrealized_gains == 50


def test_multiple_trades_multiple_buys():
    trades = pd.DataFrame(
        {
            "Transaction": ["Purchase", "Purchase", "Sale", "Purchase"],
            "Amount": [1000, 1000, 500, 400],
            "trade_price": [100, 200, 250, 200],
            "current_price": [300, 300, 300, 300],
            "TransactionDate": [
                datetime.now() - timedelta(4),
                datetime.now() - timedelta(3),
                datetime.now() - timedelta(2),
                datetime.now() - timedelta(1),
            ],
        }
    )
    realized_gains, unrealized_gains = calc_gains(trades)
    assert realized_gains == 66.67
    assert unrealized_gains == 89.47


def test_multiple_trades_sell_more_than_owned():
    trades = pd.DataFrame(
        {
            "Transaction": ["Purchase", "Purchase", "Sale"],
            "Amount": [1000, 1000, 2000],
            "trade_price": [100, 200, 50],
            "current_price": [300, 300, 300],
            "TransactionDate": [
                datetime.now() - timedelta(4),
                datetime.now() - timedelta(3),
                datetime.now() - timedelta(2),
            ],
        }
    )
    realized_gains, unrealized_gains = calc_gains(trades)
    assert realized_gains == -66.67
    assert unrealized_gains == None


def test_multiple_trades_sell_more_than_owned_w_buy():
    trades = pd.DataFrame(
        {
            "Transaction": ["Purchase", "Purchase", "Sale", "Purchase"],
            "Amount": [1000, 1000, 2000, 400],
            "trade_price": [100, 200, 50, 200],
            "current_price": [300, 300, 300, 300],
            "TransactionDate": [
                datetime.now() - timedelta(4),
                datetime.now() - timedelta(3),
                datetime.now() - timedelta(2),
                datetime.now() - timedelta(1),
            ],
        }
    )
    realized_gains, unrealized_gains = calc_gains(trades)
    assert realized_gains == -66.67
    assert unrealized_gains == 50


def test_multiple_trades_weighted_realized_gains_pos():
    trades = pd.DataFrame(
        {
            "Transaction": ["Purchase", "Sale", "Sale"],
            "Amount": [1000, 1000, 1000],
            "trade_price": [100, 200, 250],
            "current_price": [300, 300, 300],
            "TransactionDate": [
                datetime.now() - timedelta(4),
                datetime.now() - timedelta(3),
                datetime.now() - timedelta(2),
            ],
        }
    )
    realized_gains, unrealized_gains = calc_gains(trades)
    assert realized_gains == 122.22
    assert unrealized_gains == 200


def test_multiple_trades_weighted_realized_gains_neg():
    trades = pd.DataFrame(
        {
            "Transaction": ["Purchase", "Sale", "Sale"],
            "Amount": [10000, 1000, 1000],
            "trade_price": [100, 50, 25],
            "current_price": [300, 300, 300],
            "TransactionDate": [
                datetime.now() - timedelta(4),
                datetime.now() - timedelta(3),
                datetime.now() - timedelta(2),
            ],
        }
    )
    realized_gains, unrealized_gains = calc_gains(trades)
    assert realized_gains == -66.67
    assert unrealized_gains == 200
