**This python script is no longer actively developed.  BitcoinTaxes can now be found at http://garypaduana.com/bitcoinTaxes**

BitcoinTaxes
=

This python script is currently capable of computing short term and long term capital gains based on a calendar year tax year and FIFO accounting.  The input file is based on the standard export file provided by Bitstamp with an additional optional column, `Description`.  Only a transaction with `Type == 2` (buy/sell) is considered when computing tax events because it is unknown if you own the sending or receiving account for depsoit and withdraw events.  Transferring money from one wallet to another is not a taxable event (although it may incur a mining fee, which I plan to account for as cost basis in later updates).

You are encouraged to enter your entire Bitcoin transactional history in a single `.csv` file and the program will group purchase and sell events into their respective tax years.

**Usage**

```
$ python BitcoinTaxes.py [-v] -f path_to_input_file.csv
```

```
$ python BitcoinTaxes.py --help
Usage: BitcoinTaxes.py [options]

Options:
  -h, --help            show this help message and exit
  -f FILENAME, --file=FILENAME
                        Input .csv file path
  -v, --verbose         verbose console output
```

**Sample Output**

The output below shows fictional transaction history.  Transactions with $0.00 basis were recorded as such in the .csv file because they were tips, donations, or fully taxable acquisitions of BTC with no basis.

```
Processing File: C:\Bitcoin Transactions.csv
2013-08-11 20:00:00 Selling 3.39907893 BTC
	3.39907893 BTC partially filled from 3.18453891 BTC purchased on 2013-03-27 13:27:00 (basis: $303.95 proceeds: $350.39)
	0.21454002 BTC partially filled from 0.0112759 BTC purchased on 2013-03-28 00:37:00 (basis: $0.00 proceeds: $1.24)
	0.20326412 BTC partially filled from 0.01326412 BTC purchased on 2013-03-28 01:00:00 (basis: $0.00 proceeds: $1.46)
	0.19 BTC partially filled from 0.15 BTC purchased on 2013-04-02 20:25:00 (basis: $20.75 proceeds: $16.50)
	0.04 BTC fully filled from 0.04 BTC purchased on 2013-04-12 05:55:00 (basis: $0.00 proceeds: $4.40)
2013-08-30 16:37:00 Selling 0.1130999 BTC
	0.1130999 BTC fully filled from 0.3 BTC purchased on 2013-08-29 00:22:00 (basis: $13.46 proceeds: $15.00)
```

**Sample Input**

```
Type,Date,BTC,USD,USD/BTC,Fee,Description
2,3/27/2013 17:27,3.18453891,-303.95,95.44,0,bit Instant purchase
2,3/28/2013 4:37,0.0112759,0,88,0,tip
2,3/28/2013 5:00,0.01326412,0,88,0,donation
2,4/3/2013 0:25,0.15,-20.4,136,0.35,coinbase buy/sell
2,4/12/2013 9:55,0.04,0,100,0,excel macro work
2,8/12/2013 0:00,-3.39907893,379,110.03,5,bitfloor USD refund
2,8/29/2013 4:22,0.3,-35.7,119,0.51,coinbase buy
2,8/30/2013 15:05,0.5,-56.93,113.86,0.72,coinbase buy
2,8/30/2013 19:51,0.8,-100.28,125.35,1.15,coinbase buy
2,8/30/2013 20:37,-0.1130999,15,132.63,0,online subscription purchase
```

`Type` is the type of transaction represented. `0 = Deposit`, `1 = Withdraw`, `2 = Buy/Sell`

`Date` is defined as `"%m/%d/%Y %H:%M"`, e.g. `11/19/2013 19:14` OR `"%Y-%m-%d %H:%M:%S"`, e.g. `2013-11-14 14:54:32`.  Bitstamp has used both formats in their export files in the recent past.

`BTC` is the amount of Bitcoin transacted.  `BTC > 0` is a purchase. `BTC < 0` is a sale.

`USD` is the amount of local currency transacted. `USD < 0` is a purchase of BTC.  `USD > 0` is a sale of BTC.

`USD/BTC` is the price of BTC at the moment of the sale.

`Fee` is the broker fee associated with the transaction and will count towards cost basis.  Optional and will default to $0.00 if omitted.

`Description` can be optionally supplied.

=

**Use case examples**

* I purchased a good or service with Bitcoin.

`2,8/30/2013 20:37,-0.1130999,15,132.63,0,purchased an online subscription`

Explanation: On 8/30/2013, I spent 0.1130999 BTC worth $15.00.  At the time of the transaction, 1 BTC was worth $132.63.  There was no broker fee associated with this sale.

* I received BTC as a gift or a tip.

`2,3/28/2013 5:00,0.01326412,0,88,0,reddit tip`

Explanation: On 3/28/2013, I received 0.01326412 BTC having spent $0 because it was a gift.  This means I have zero cost basis and the entire amount will be treated as gain.  At the time of the transaction, 1 BTC was worth $88.00.  There was no broker fee associated with this sale.

* I sold BTC on an exchange.

`2,10/19/2013 20:00,-2.051,334.87,163.35,3.5,coinbase sell`

Explanation: On 10/19/2013, I sold 2.051 BTC in exchange for $334.87.  At the time of the transaction, 1 BTC was worth $163.35.  There was a $3.50 broker fee associated with this sale.

* I bought BTC from a friend and paid cash.

`2,11/5/2013 5:07,0.5,-122.62,245.24,0,purchase from Joe`

Explanation: On 11/5/2013, I purchased 0.5 BTC worth $122.62.  At the time of the transaction, 1 BTC was worth 245.24.  There was no fee associated with this transaction.

=

If you found this program to be useful and would like to donate, 1FkkWv8wQqJBWUcRCZkd73D8pAsykxCGNM

Thank you.
