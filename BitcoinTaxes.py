'''
    BitcoinTaxes
    Capital Gains calculator
    Copyright (C) 2014, Gary Paduana, gary.paduana@gmail.com
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import calendar
import copy
from datetime import *
from dateutil.relativedelta import relativedelta
import locale
import string
import sys
from time import strftime, strptime

def main():
    try:
        locale.setlocale(locale.LC_ALL, '')
        print "Processing File:", sys.argv[1]
        data = getData(sys.argv[1])
        transactions = []
        workingCopy = []
        yearlyValues = {}
        
        # skip first line, it's the header.  parse csv input as Transaction objects
        for transaction in data[1:]:
            args = [string.replace(x, '\n', '') for x in transaction.split(',')]
            transactions.append(Transaction(*args))
    
        transactions.sort(key = lambda x: x.time, reverse = False)
        
        # create a working copy of the transactions used for modification while
        # iterating through the original collection.
        workingCopy = copy.deepcopy(transactions)
        
        for trans in transactions:
            # store aggregate data for the year allowing all transactions to appear
            # in one large file while keeping tax values separated.
            year = trans.time.year
            if year not in yearlyValues:
                yearlyValues[year] = YearlyValues()
            
            # For both deposit and withdraw it is assumed that the you own both the
            # sending and receiving accounts, thus not producing a taxable event.
            # You will need to change the trans type in the csv for this transaction
            # to 2 to effectively produce a 'buy' or 'sell' event if it should be taxed.
            # Hypothetically, if a standard bitstamp deposit log event were counted 
            # for tax purposes, it would appear to have no basis.    
            if trans.type == 0:
                # Deposit
                pass
            if trans.type == 1:
                # Withdraw
                pass
            if trans.type == 2:
                if trans.btc < 0:
                    # Sale
                    shortGain, longGain, basis, proceeds, workingCopy = saleAction(trans, workingCopy)
                    yearlyValues[year].shortGain += shortGain
                    yearlyValues[year].longGain += longGain
                    yearlyValues[year].sold += trans.usd
                    yearlyValues[year].basis += basis
                    yearlyValues[year].proceeds += proceeds
                    # uncomment to print sale date and present gain. useful to chart gain over time.
                    #print str(trans.time) + "," + str(yearlyValues[year].shortGain) + "," + str(yearlyValues[year].longGain)
                else:
                    # Purchase
                    yearlyValues[year].bought += trans.usd * -1.0 + trans.fee
    
                yearlyValues[year].endingBtc += trans.btc
        
        # endingBtc is known for each year, use this value to compute
        # running total btc balance known as cumulativeBtc
        for year in yearlyValues:
            for year2 in yearlyValues:
                if year2 >= year:
                    yearlyValues[year2].cumulativeBtc += yearlyValues[year].endingBtc
            print (str(year) + ":"), yearlyValues[year]
                
    except Exception:
        print "Unexpected error:", sys.exc_info() 

def saleAction(bTrans, workingCopy):
    shortGain = 0.0
    longGain = 0.0
    basis = 0.0
    proceeds = 0.0
    complete = False
    
    for aTrans in workingCopy:
        if(aTrans.presentBalance > 0 and aTrans.type == 2):
            thisProceeds = 0.0
            thisBasis = 0.0
            # the sell volume can be filled from this single past purchase
            if(aTrans.presentBalance >= (bTrans.presentBalance * -1.0)):   
                # mark a portion of this past purchase as sold by reducing current quantity
                aTrans.presentBalance += bTrans.presentBalance
                thisBasis = (aTrans.usd / aTrans.btc) * bTrans.presentBalance
                thisProceeds = (bTrans.presentBalance / bTrans.btc) * (bTrans.usd - bTrans.fee)
                basis += thisBasis
                proceeds += thisProceeds
                complete = True
            
            # current sale is greater than this last purchase, take only as much as
            # is currently available and then proceed to the next btc purchase event
            else:
                thisBasis = (aTrans.presentBalance / aTrans.btc) * (aTrans.usd * -1 + aTrans.fee)
                thisProceeds = aTrans.presentBalance * ((bTrans.usd - bTrans.fee) / bTrans.btc * -1)
                basis += thisBasis
                proceeds += thisProceeds
                bTrans.presentBalance += aTrans.presentBalance
                aTrans.presentBalance = 0
            
            if(relativedelta(bTrans.time, aTrans.time).years >= 1):
                longGain += (thisProceeds - thisBasis)
            else:
                shortGain += (thisProceeds - thisBasis)
                    
            if complete:
                return shortGain, longGain, basis, proceeds, workingCopy
                            
    return shortGain, longGain, basis, proceeds, workingCopy                   
    
def getData(arg):
    with open(arg, 'r') as f:
        return f.readlines()

class YearlyValues:
    """
        Holds aggregate values for a tax year. Values include:
            - amount bought in local currency
            - amount sold in local currency
            - gain in local currency
            - net bitcoin balance for this year (btc purchased - btc sold)
            - cumulative bitcoin balance through the end of this year (including all prior years)
    """
    def __init__(self):
        self.bought = 0.0
        self.sold = 0.0
        self.basis = 0.0
        self.proceeds = 0.0
        self.shortGain = 0.0
        self.longGain = 0.0
        self.endingBtc = 0.0
        self.cumulativeBtc = 0.0
    
    def __str__(self):
        return "bought: " + locale.currency(self.bought, grouping=True) + \
            ", sold: " + locale.currency(self.sold, grouping=True) + \
            ", basis: " + locale.currency(self.basis, grouping=True) + \
            ", proceeds: " + locale.currency(self.proceeds, grouping=True) +\
            ", short term gain: " + locale.currency(self.shortGain, grouping=True) +\
            ", long term gain: " + locale.currency(self.longGain, grouping=True) +\
            ", btcDelta: " + str(round(self.endingBtc, 8)) +\
            ", cumulativeBtc: " + str(round(self.cumulativeBtc, 8))
    def __repr__(self):
        return "bought: " + locale.currency(self.bought, grouping=True) + \
            ", sold: " + locale.currency(self.sold, grouping=True) + \
            ", basis: " + locale.currency(self.basis, grouping=True) + \
            ", proceeds: " + locale.currency(self.proceeds, grouping=True) +\
            ", short term gain: " + locale.currency(self.shortGain, grouping=True) +\
            ", long term gain: " + locale.currency(self.longGain, grouping=True) +\
            ", btcDelta: " + str(round(self.endingBtc, 8)) +\
            ", cumulativeBtc: " + str(round(self.cumulativeBtc, 8))
    
class Transaction:
    """
        A BTC transaction.
        type: 0:deposit, 1:withdrawal, 2:buy/sell, 
    """
    def __init__(self, type, eventTimestamp, btc, usd, btc_price, fee='', description=''):
        self.type = int(type)
        self.datetime = eventTimestamp
        
        # There are two different formats recently used by Bitstamp in their export feature, try to accept either one
        try:
            self.time = datetime.fromtimestamp(calendar.timegm(strptime(eventTimestamp, "%m/%d/%Y %H:%M")))  # 11/19/2013 19:14
        except Exception:
            self.time = datetime.fromtimestamp(calendar.timegm(strptime(eventTimestamp, "%Y-%m-%d %H:%M:%S")))  # 2013-11-14 14:54:32
            
        self.btc = float(btc)
        self.usd = float(usd)
        self.btc_price = float(btc_price)
        
        if(len(fee) == 0):
            self.fee = 0.0
        else:
            self.fee = float(fee)
        
        self.description = description
        # present balance is used to keep track of whether or not this was sold
        # for FIFO accounting
        self.presentBalance = float(btc)
       
    def __str__(self):
        return str(self.type) + ',' + str(self.datetime) + ',' +\
            str(self.btc) + ',' + str(self.usd) + ',' + str(self.btc_price) + "," +\
            str(self.fee) + "," + str(self.description) + "," + str(self.presentBalance)
    def __repr__(self):
        return str(self.type) + ',' + str(self.datetime) + ',' +\
            str(self.btc) + ',' + str(self.usd) + ',' + str(self.btc_price) + "," +\
            str(self.fee) + "," + str(self.description) + "," + str(self.presentBalance)
    
if __name__ == "__main__":
    main()