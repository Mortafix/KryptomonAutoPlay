# Kryptomon Autoplay
> *With great Kryptomons comes great responsibility* 

In order to setup your custom actions, you need to edit `static/instructions.txt` file.  
There are a few **settings** and 2 set of actions: **gameplay** and **other**.

## Settings
* **timeframe**: bot will run every base timeframe (defualt: `5 min`)
* **kryptomons**: number of kryptomon in every screen (separated by commas)
#### Example
```bash
timeframe 5  # it will run every 5 minutes
kryptomon 3, 1  # 4 kryptomons total: 3 on the first screen and 1 in the second one 
```

## Gameplay actions
> Usage: action **e**lement **k**ryptomon **t**imeframe  

* **action**: gameplay action to perform (`food`, `heal`, `play`, `train`)
* **element**: number of the element to give (left to right)
* **kryptomon**: number of kryptomon on the current screen
* **timeframe**: multiple of the base timeframe when it'll perform the action

#### Example
```bash
food e1 k2 t1  # give the 1st food to the 2nd kryptomon on the screen every 1 timeframe (5m)
play e4 k3 t3  # use the 4th play item with the 3rd kryptomon on the screen every 3 timeframes (15m)
train e2 k1 t4 # train the 1st kryptomon on the screen for the 2nd parameter every 4 timeframes (20m)
```

## Other actions
> Usage: action **p**arameter **t**imeframe

* **action**: other action to perform
	1. `screen`: change screen
	2. `box`: open a box
* **parameter**: parameter to specify for an action
	1. `screen N`: change screen the Nth one
	2. `box X`: X = 1: free, 2: bronze, 3: silver, 4: gold 
* **timeframe**: multiple of the base timeframe when it'll perform the action

#### Example
```bash
screen p2 t2  # switch to the 2nd screen every 2 timeframes (10m)
box p3 t288  # open a silver box every 288 timeframes (1440m -> 24h)
```
