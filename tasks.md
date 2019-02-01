See: https://docs.google.com/document/d/1MkWhTZV8U9QH3WhPmY_0J3iY-KlUtBcKDcDdydaFGvU/edit

~~Step 1: Capture Buy/Sell Signals~~
- ~~Add 1 column: Signal~~
- ~~Put: "Buy" if: buySellRatio>1 && Sureness>0.5 && close > 5-EMA~~
- ~~Put: "Sell" if: buySellRatio<1 && Sureness>0.5 && close < 5-EMA~~
- ~~Put: "Neutral" otherwise~~

Step 1a: Capture Stop prices (long & short)
- Add 2 columns: Long_Stop, Short_Stop
- Put: min (Low of last 3 days including today) as Long_Stop
- Put: max (High of last 3 days including today) as Short_Stop

Step 2: Perform paper trades: 

Case 1: Long only
- Add 3 columns: Cash, Shares, Balance
- Start with Cash=10000, and shares=0, balance=10000
- Note: stop is a fixed stop
- Write program to execute simple buy, hold, sell and use LONG as the only strategy
   - If Signal=Buy and shares=0 -- previously no position, for next day, set
      - cash=0
      - shares=balance (day-1) / open
      - balance=cash+shares*close
   - If Signal=Buy and shares>0 -- previously LONG, continue to hold, for next day, set
      - cash=0; 
      - shares=shares (day-1); 
      - balance= cash+shares*closee
   - If Signal=Buy and shares<0 -- previously SHORT (this should not happen yet, since we are doing LONG only, but implement this anyway), for next day: buy with entire cash balance, cover the short, and keep the remaining, set
      - cash=0  
      - shares=balance(day-1)/open+shares (day-1); 
      - balance= cash+shares*close
   - If Signal="Neutral"

Case 2: Short only
- Use the same 3 columns: Cash, Shares, Balance
- Start with Cash=10000, and shares=0, balance=10000
- Note: stop is a fixed stop
- Write program to execute simple buy, hold, sell and use SHORT as the only strategy
   - If Signal=Sell and shares=0 -- previously no position, for next day, set
      - shares= -1 * (balance (day-1) / open) -- since we are shorting, this should be negative
      - cash=balance + (shares*open)
      - balance=cash+shares*close
   - If Signal=Sell and shares<0 -- previously SHORT, continue to hold, for next day, set
      - cash= cash (day-1); 
      - shares=shares (day-1); 
      - balance= cash+shares*close
   - If Signal=Sell and shares>0 -- previously LONG, for next day: sell all shares, and short with entire cash balance, set
      - cash= shares (day-1)*open + shares (day-1)*open
shares=balance(day-1)/open+shares (day-1); 
balance= cash+shares*close