def tradeoff(sample):

  for estimate in sample.estimates:
    if estimate.parameter.property.abv=='cx': cx=estimate.value
    if estimate.parameter.property.abv=='cy': cy=estimate.value
    if estimate.parameter.property.abv=='lr': lr=estimate.value

  wx = 1960.34963229
  wy = 1922.50166667

  rc = ((cx-wx)**2+(cy-wy)**2)**0.5
  return rc<lr
