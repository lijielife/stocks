#!/usr/bin/env python

from . import actions

class Account(object):
    def __init__(self, initial_value=100000, commission=0.00):
        self.cash_value = initial_value
        self.commission = commission
        self.positions = {}
        self.transactions = []


    def account_value(self):
        securities_value = 0
        for k in self.positions.keys():
            securities_value += self.positions[k].value()
        return self.cash_value + securities_value

    def buy(self, security, n_shares, share_price):
        # Create transaction record
        transaction = {
            'action': actions.BUY_LONG,
            'security': security,
            'n_shares': n_shares,
            'share_price': share_price,
            'commission': self.commission
        }
        self.transactions.append(transaction)

        # Update positions
        if security in self.positions.keys():
            # Add to position if it exists
            self.positions[security].n_shares += n_shares
            self.positions[security].tick()
        else:
            # Otherwise create a new one
            position = Position(security, n_shares, share_price)
            self.positions[security] = position

        # Update account value
        self.cash_value -= position.cost_basis


    def sell(self, security, n_shares, share_price):
        # Create transaction record
        transaction = {
            'action': actions.SELL_LONG,
            'security': security,
            'n_shares': n_shares,
            'share_price': share_price,
            'commission': self.commission
        }
        self.transactions.append(transaction)

        # Update positions
        self.positions[security].tick(share_price)
        shares_held = self.positions[security].n_shares
        if shares_held >= n_shares:
            # Delete position if we sold all our shares
            self.positions.pop(security, None)
        else:
            self.positions[security].n_shares -= n_shares

        # Update account value
        self.cash_value += share_price * n_shares - self.commission



class Position(object):
    def __init__(self, security, n_shares, share_price):
        self.security = security
        self.n_shares = n_shares
        self.share_price = share_price

    def tick(self, share_price):
        self.share_price = share_price

    def value(self):
        return self.share_price * self.n_shares


