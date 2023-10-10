def CalculateEMA(pastPriceVec, currentPrice, windowSize):
  import numpy as np

  dataLen = len(pastPriceVec)

  if dataLen < windowSize:
    return np.mean(np.append(pastPriceVec, currentPrice))
  else:
    ma = np.mean(pastPriceVec[0:windowSize])
    for idx in range(windowSize, dataLen):
      ma = (1 - 1 / windowSize) * ma + (1 / windowSize) * pastPriceVec[idx]
    ma = (1 - 1 / windowSize) * ma + (1 / windowSize) * currentPrice
    return ma
