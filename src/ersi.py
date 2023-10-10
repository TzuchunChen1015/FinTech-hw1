def CalculateERSI(pastPriceVec, currentPrice, windowSize):
  import numpy as np

  dataLen = len(pastPriceVec)
  if dataLen == 0:
    return 0.5
  diffPriceVec = np.zeros(dataLen)

  for idx in range(1, dataLen):
    diffPriceVec[idx - 1] = pastPriceVec[idx] - pastPriceVec[idx - 1]
  diffPriceVec[dataLen - 1] = currentPrice - pastPriceVec[dataLen - 1]

  rsiSize = min(dataLen, windowSize)
  pos = neg = 0
  for idx in range(rsiSize):
    if diffPriceVec[idx] > 0:
      pos += diffPriceVec[idx] 
    elif diffPriceVec[idx] < 0:
      neg -= diffPriceVec[idx] 
  pos /= rsiSize
  neg /= rsiSize
  rsi = pos / (pos + neg)

  if dataLen <= windowSize:
    return rsi
  else:
    for idx in range(windowSize, dataLen): 
      if diffPriceVec[idx] > 0:
        pos = (1 - 1 / windowSize) * pos + (1 / windowSize) * diffPriceVec[idx]
        neg = (1 - 1 / windowSize) * neg
      elif diffPriceVec[idx] < 0:
        neg = (1 - 1 / windowSize) * neg - (1 / windowSize) * diffPriceVec[idx]
        pos = (1 - 1 / windowSize) * pos
    ris = pos / (pos + neg)
    return rsi
