import sys
import numpy as np
import pandas as pd

from src.ema import CalculateEMA
from src.ersi import CalculateERSI
from src.kd import CalculateKD

def myStrategy(pastPriceVec, currentPrice, emaShort, emaLong, ersiShort, ersiLong, kdAlpha, overBuy, overSell):
  # 1. EMA
  # 2. ERSI - Exponential RSI
  # 3. KD
  EMAwindowSizeShort = emaShort
  EMAwindowSizeLong = emaLong
  ERSIwindowSizeShort = ersiShort
  ERSIwindowSizeLong = ersiLong
  KDalpha = kdAlpha

  OverBuy = overBuy
  OverSell = overSell

  action = 0

  EMAshort = CalculateEMA(pastPriceVec, currentPrice, EMAwindowSizeShort)
  EMAlong = CalculateEMA(pastPriceVec, currentPrice, EMAwindowSizeLong)
  ERSIshort = CalculateERSI(pastPriceVec, currentPrice, ERSIwindowSizeShort)
  ERSIlong = CalculateERSI(pastPriceVec, currentPrice, ERSIwindowSizeLong)
  Kvalue, Dvalue = CalculateKD(pastPriceVec, currentPrice, KDalpha)

  if EMAshort > EMAlong and ERSIshort > ERSIlong and Kvalue > Dvalue:
    action = 1
  elif EMAshort < EMAlong and ERSIshort < ERSIlong and Kvalue < Dvalue:
    action = -1
  elif ERSIshort > OverBuy and Kvalue > OverBuy:
    action = -1
  elif ERSIshort > 0.5 and Kvalue > 0.5:
    action = 1
  elif ERSIshort < OverSell and Kvalue < OverSell:
    action = 1
  elif ERSIshort < 0.5 and Kvalue < 0.5:
    action = -1

  return action

# Compute return rate over a given price vector, with 3 modifiable parameters
def computeReturnRate(priceVec, emaShort, emaLong, ersiShort, ersiLong, kdAlpha, overBuy, overSell):
	capital=1000	# Initial available capital
	capitalOrig=capital	 # original capital
	dataCount=len(priceVec)				# day size
	suggestedAction=np.zeros((dataCount,1))	# Vec of suggested actions
	stockHolding=np.zeros((dataCount,1))  	# Vec of stock holdings
	total=np.zeros((dataCount,1))	 	# Vec of total asset
	realAction=np.zeros((dataCount,1))	# Real action, which might be different from suggested action. For instance, when the suggested action is 1 (buy) but you don't have any capital, then the real action is 0 (hold, or do nothing). 
	# Run through each day
	for ic in range(dataCount):
		currentPrice=priceVec[ic]	# current price
		suggestedAction[ic]=myStrategy(priceVec[0:ic], currentPrice, emaShort, emaLong, ersiShort, ersiLong, kdAlpha, overBuy, overSell)		# Obtain the suggested action
		# get real action by suggested action
		if ic>0:
			stockHolding[ic]=stockHolding[ic-1]	# The stock holding from the previous day
		if suggestedAction[ic]==1:	# Suggested action is "buy"
			if stockHolding[ic]==0:		# "buy" only if you don't have stock holding
				stockHolding[ic]=capital/currentPrice # Buy stock using cash
				capital=0	# Cash
				realAction[ic]=1
		elif suggestedAction[ic]==-1:	# Suggested action is "sell"
			if stockHolding[ic]>0:		# "sell" only if you have stock holding
				capital=stockHolding[ic]*currentPrice # Sell stock to have cash
				stockHolding[ic]=0	# Stocking holding
				realAction[ic]=-1
		elif suggestedAction[ic]==0:	# No action
			realAction[ic]=0
		else:
			assert False
		total[ic]=capital+stockHolding[ic]*currentPrice	# Total asset, including stock holding and cash 
	returnRate=(total[-1]-capitalOrig)/capitalOrig		# Return rate of this run
	return returnRate

if __name__=='__main__':
  returnRateBest=-1.00	 # Initial best return rate
  df=pd.read_csv(sys.argv[1])	# read stock file
  adjClose=df["Adj Close"].values		# get adj close as the price vector

  for emaShort in range(4, 7):
    for emaLong in range(8, 13):
      for ersiShort in range(4, 7): # 4 ~ 6
        for ersiLong in range(8, 13): # 8 ~ 12
          for kdAlpha in range(0, 101):
            for overBuy in range(70, 85):
              for overSell in range(15, 30):
                returnRate = computeReturnRate(adjClose, emaShort, emaLong, ersiShort, ersiLong, kdAlpha / 100, overBuy / 100, overSell / 100)
                if returnRate > returnRateBest:
                  returnRateBest = returnRate
                  print("Best RR:%f" %(returnRateBest))
                  emaShortBest = emaShort
                  emaLongBest = emaLong
                  ersiShortBest = ersiShort
                  ersiLongBest = ersiLong
                  kdAlphaBest = kdAlpha / 100
                  overBuyBest = overBuy / 100
                  overSellBest = overSell / 100
  print("Best RR:%f" %(returnRateBest))
  print("Best Settings: emaShort=%d, emaLong=%d, ersiShort=%d, ersiLong=%d, kdAlpha=%f, overBuy=%f, overSell=%f" %(emaShortBest, emaLongBest, ersiShortBest, ersiLongBest, kdAlphaBest, overBuyBest, overSellBest))
