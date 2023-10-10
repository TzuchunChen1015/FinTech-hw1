from src.ema import CalculateEMA
from src.ersi import CalculateERSI
from src.kd import CalculateKD

def myStrategy(pastPriceVec, currentPrice):
  # 1. EMA
  # 2. ERSI - Exponential RSI
  # 3. KD
  EMAwindowSizeShort = 5
  EMAwindowSizeLong = 10
  ERSIwindowSizeShort = 6
  ERSIwindowSizeLong = 14
  KDalpha = 2 / 3

  OverBuy = 0.75
  OverSell = 0.25

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
