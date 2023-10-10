def CalculateKD(pastPriceVec, currentPrice, KDalpha):
  import numpy as np

  dataLen = len(pastPriceVec)
  if dataLen <= 8:
    maxPrice = np.max(np.append(pastPriceVec, currentPrice))
    minPrice = np.min(np.append(pastPriceVec, currentPrice))
    if maxPrice == minPrice:
      return 0.5, 0.5
    else:
      rsv = (currentPrice - minPrice) / (maxPrice - minPrice)
      return rsv, rsv
  else:
    maxPrice = np.max(pastPriceVec[0:9])
    minPrice = np.min(pastPriceVec[0:9])
    rsv = (pastPriceVec[8] - minPrice) / (maxPrice - minPrice)
    kValue = dValue = rsv

    for idx in range(9, dataLen):
      maxPrice = np.max(pastPriceVec[idx-8:idx+1])
      minPrice = np.min(pastPriceVec[idx-8:idx+1])
      rsv = (pastPriceVec[idx] - minPrice) / (maxPrice - minPrice)
      kValue = KDalpha * kValue + (1 - KDalpha) * rsv
      dValue = KDalpha * dValue + (1 - KDalpha) * kValue

    maxPrice = np.max(np.append(pastPriceVec[-8:], currentPrice))
    minPrice = np.min(np.append(pastPriceVec[-8:], currentPrice))
    rsv = (currentPrice - minPrice) / (maxPrice - minPrice)
    kValue = KDalpha * kValue + (1 - KDalpha) * rsv
    dValue = KDalpha * dValue + (1 - KDalpha) * kValue

    return kValue, dValue
