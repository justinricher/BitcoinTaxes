BitcoinTaxes
=========================

This python script is currently capable of computing short term and long term capital gains based on a calendar year tax year and FIFO accounting.  The input file is based on the standard export file provided by Bitstamp with an additional optional column, `Description`.  Only a transaction with `Type == 2` (buy/sell) is considered when computing tax events because it is unknown if you own the sending or receiving account for depsoit and withdraw events.  Transferring money from one wallet to another is not a taxable event (although it may incur a mining fee, which I plan to account for as cost basis in later updates).

You are encouraged to enter your entire Bitcoin transactional history in a single `.CSV` file and the program will group purchase and sell events into their respective tax years.

**Usage**

```$ python BitcoinTaxes.py path_to_input_file.csv```

**Sample Output**

(fictional transaction history)
```
Processing File: C:/2013 Taxes/Bitcoin Transactions.csv
2012: bought: $303.95, sold: $0.00, short term gain: $0.00, long term gain: $0.00, btcDelta: 3.18453891, cumulativeBtc: 3.18453891
2013: bought: $8,631.22, sold: $9,660.83, short term gain: $949.39, long term gain: $46.44, btcDelta: -2.75453891, cumulativeBtc: 0.43
2014: bought: $4,864.60, sold: $4,568.55, short term gain: ($275.30), long term gain: $0.00, btcDelta: 0.22365609, cumulativeBtc: 0.65365609
```

**Sample Input**

```
Type,Date,BTC,USD,USD/BTC,Fee,Description
2,3/27/2013 17:27,3.18453891,-303.95,95.44,0,bit Instant purchase
2,4/3/2013 0:25,0.15,-20.4,136,0.35,coinbase buy
2,8/31/2013 5:08,0.4,-51.06,127.65,0.66,coinbase buy
2,9/4/2013 18:25,0.4,-47.15,117.88,0.62,coinbase buy
2,10/2/2013 14:39,0.4,-44.22,110.55,0.59,coinbase buy
```

`Type` is the type of transaction represented. `0 = Deposit`, `1 = Withdraw`, `2 = Buy/Sell`

`Date` is defined as `"%m/%d/%Y %H:%M"`, e.g. `11/19/2013 19:14` OR `"%Y-%m-%d %H:%M:%S"`, e.g. `2013-11-14 14:54:32`.  Bitstamp has used both formats in their export files in the recent past.

`BTC` is the amount of Bitcoin transacted.  `BTC > 0` is a purchase. `BTC < 0` is a sale.

`USD` is the amount of local currency transacted. `USD < 0` is a purchase of BTC.  `USD > 0` is a sale of BTC.

`USD/BTC` is the price of BTC at the moment of the sale.

`Fee` is the broker fee associated with the transaction and will count towards cost basis.  Optional and will default to $0.00 if omitted.

`Description` can be optionally supplied.

===

If you found this program to be useful and would like to donate, 1FkkWv8wQqJBWUcRCZkd73D8pAsykxCGNM

Thank you.
