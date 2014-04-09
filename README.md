BitcoinTaxes
=========================

This python script is currently capable of computing short term capital gains.

**Usage**

```$ python BitcoinTaxes.py path_to_input_file.csv```

**Sample Output**

```
Processing File: C:/2013 Taxes/Bitcoin Transactions.csv
2013: bought: $3,423.84, sold: $4,247.73, gain: $1,123.08, btcDelta: 0.6322228, cumulativeBtc: 0.6322228
2014: bought: $3,759.34, sold: $3,079.28, gain: ($161.22), btcDelta: 0.65365609, cumulativeBtc: 1.28587889
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

`Type` is the type of transaction represented. 0 = Deposit, 1 = Withdraw, 2 = Buy/Sell

`Date` is defined as `"%m/%d/%Y %H:%M"`, e.g. `11/19/2013 19:14`

`BTC` is the amount of Bitcoin transacted.  `BTC > 0` is a purchase. `BTC < 0` is a sale.

`USD` is the amount of local currency transacted. `USD < 0` is a purchase of BTC.  `USD > 0` is a sale of BTC.

`USD/BTC` is the price of BTC at the moment of the sale.

`Fee` is the broker fee associated with the sale and will count towards cost basis.

`Description` can be optionally supplied.
