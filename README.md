# Bexy.app
 
Bexy is a automated trading bot which control Stoch RSI & MAC.D & Tillson T3 about coin. 

For now it checks 15 different crypto coin and make orders about them.

# Features
1. Automatic Trade
> Bexy checks all 15 coins in every 5 mins (candle closes) (customizable). If there any intersecitons on candle close it opens trade. The intersection data comes from checking the Stoch RSI & MAC.D & Tillson T3.

> Compare the directions and make the decision with datas which come from Tillson T3 & Stoch RSI & MAC.D direction control module. Then creates buy (long) and sell (short) orders if there is a success equality.

> With Telegram connection it informs the user about trades and intersections.

2. Telegram Connection
> The bot on Telegram makes the user control their settings like subscription to coin. Subscription is allow Bexy to watch selected coin or not watch selected coin.

> If user doesn't want to open short trades today he need just tell the bot to close short trades or open long trades.

> Also user can add their Binance api keys to his datas and add or drop to coin that key. Like if user don't want open trade on **ADA** with "key 1" but with "key 2" wants to allow trade.

> User or admins can control trades from Telegram. Users or admins can close all position trades from one command.

3. Threading
> Every process and functions firstly comes from thread handler.

> Threads isn't mix because thread ids is all unique. Timestamp using in thread ids.

4. Order and Position Checking
> All orders checking with interval in every 1 seconds with threading.

> When new order appears system checks it every seconds if it cancelled or going the position.

> If orders isn't goes position in 5 and half minutes system automaticly cancel the order because to not get too risk.

> When user manually canceled order in Binance system can figure it and removes the thread and inform user from Telegram.

> When order goes the position system change the order status inside and checks position and PNL (profit and loss)

> While position checking if money loss is too much than 1.5 dollars it informs the user should close position for not get risk of liquidity.

> If profit is higer than 1.5 dollars it informs the user should close the position to not get risk of losing profit.

> If user manually close position from Binance the system can figure it and remove the thread and remove the position from inside and inform the user.

# For Final Explaination

Bexy is a Trader Bot project to people who wants to Future trading on Binance. I'm making this project on my own for 2 months and it is working.

Bot is looking Stoch RSI & MAC.D & Tillson T3 datas for opening orders. Bot can create successful and correct orders.

This will be a platform that based on web. I'm continuing to develop this and this version is the working version of Beta version.

There is a logging system in here and when it starts, the bot every single process gives a log.

And also you can see sendLog() requests in function to understand which function what is work for.
