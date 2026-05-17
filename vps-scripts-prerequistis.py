check if all dependencies are installed correctly or not
IST time is applied in the script or not ?
simulated everyday scenario with the script already ?
  give exception cases to solve
    is outcome desired ?

badha ma individually
  exchange == "NFO" , "MCX"
  ends with "CE" or "PE"
  starts with "NIFTY"

  kite na orders and postions ma badhe j apply karo

1 quantity trading for 1 expiry at least minimum


----------------------------------------------

kite.orders and kite.positions thi
every 5 seconds or every 10 seconds (as per your speed requirement)
script ni internal state sync karo


-------------------------
pending orders ma

PE and CE maate
position thi opposite ek j Sl order BUY or SELL hovo joiye


---------------------

system ma jyare pan
order place karvano thaay tyare
postions mathi net postions and orders mathi open orders 
check karine j order place karva

--------------------------

1 minute check ma
net positions and pending orders khaash check karva 

-----------------------------------

quantity vadhare occhi che ?
penging orders vadhare occha che ?



-----------------------------------


market prottection thi place karela order koi vaar limit ma rahi jaay che

suppose nifty 25000 ne trigger kare to postion levani che

to 25000 ne volume thi brake kare to , koi ek leg j aavshe
bijo leg occho bhaav thai jaashe ane nai aave


tyare limit ma rehelo order 
cancel karine , tarat j bijo order place karine position ne hedge karo

------------------------------------------

je script ma SL-M order available naa hoy ema
aapne haathe pan SL with LIMIT order place kari shakiye

[VISIT URL] (https://support.zerodha.com/category/trading-and-markets/charts-and-orders/order/articles/market-price-protection-on-the-order-window)


----------------------------------------

ek vaar AI ne pan pucho k 
aa script ma tane kaai error or missing case laage che ?

list of bugs/errors,
missing edge case / critical case to handle,
code quality improvements
entry - exit and SL all are defined or not?
Any gray part or any confusion has to be watched?

-----------------------------

check if there is any race condition is there in the code or not ?


-------------------------------

buy and sell pending orders can not in pending state for any leg
if the buy postion is sqaured off , related SL and Target orders should be also removed
dangling orders should be removed
prevent from placing duplicate orders and wrong quantity position
prevent from naked buy or sell position
