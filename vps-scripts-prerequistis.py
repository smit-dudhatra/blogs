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

--------------------------


at any time script looses it's internal data state,
fetch it from kite.orders or kite.positions

----------------

best scenario to test 

give candle data for historical day
check on each candle what script thinks ?

optimize it according to your needs then deploy it to live with 1 lot and check


------------------
add this param DO_MOCK_TRADING = True

and if this is true
just log each and evry minute ce and pe state and check the observation on log
don't take trade

-----------------------------


microsoft visio or eraser ma diagram banavo
clarity aavshe and future reference maate kaam laagshe


------------------------

huge movement wala days nu mock trading karo
and unhandled or exception wala case ne handle karo

-----------------------

Badha interval checks ne merge karo

-----------------

repeted api calls remove karo

---------------

every decision ne ek condition aapo
ne decision leta pela possible hoy to 
condition kite.orders and kite.positions thi check karo

----------------

frequently
missing edge cases
potetntial bugs , 
unhandled casesfind karta ryo

sample prompt

read the script in depth

simulate the secenario
from start_date to end_date

and make flow chart of entry exit and sl

or any pictorial or sequential way to understand the script and it's internals

find any missing edge case , unhandled cases or potetntial bugs
i am new to the script and wants to understand how this script works
pls ask me queries if you have any

-----------------

for compile check
run this command

cd /home/path_to_you file && python3 -m py_compile <python_file_name.py> && echo "✓ Syntax OK"


---------------------

every market order should be placed with market protection only

------------------

make a flow chart or steps or precedure of your understanding
to clarify the things or trading process
----
demo prompt

scan this script extremely deeply,

find any execution flow, any race condition ,any missing implementation , or colliding condition or any confusing part , any expcetion case to handle about script

it should have clear entry , exit and re-entry rules defined

pls ask me queries
if you have any

--------------

10 second interval ma shu check karvanu ?

same expiry,
same strike (if straddle),
quantity of position and SL orders,
SL prices,
BUY or SELL direction,
option type

-------------

strike change par , webscoket na instruments change thaay che ?

jo nai thaay to
SL and re-entry old instrument according thaashe

strike change par subscribe instrument pan change karo

-------------

Check file encoding and UTF-8 validity
Find and verify all non-ASCII emoji sequences in the file
Compile-check all string literals including emoji

to solve the emoji encode error on console

------------

trading ma mean ne badle median use vadhare karo


----------

see this script carefully and deeply analyze this

do you find any flaw?
or missing implementation?
or missing edge case?
Potential bugs?
Any minor or major logic gap?

or any confusion to execute the script ?
or anything that is not handled correctly ?

pls list them all and ask me queries if you have any

------------------

