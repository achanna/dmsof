def tradeoff(sample):

  for estimate in sample.estimates:
    if estimate.parameter.structure.domain.title=='Lens':
      if estimate.parameter.property.abv=='kappa': k1   = estimate.value
      if estimate.parameter.property.abv=='K':     K1   = estimate.value
      if estimate.parameter.property.abv=='Ks':    Ks1  = estimate.value
      if estimate.parameter.property.abv=='Kf':    Kf1  = estimate.value
      if estimate.parameter.property.abv=='phi':   phi1 = estimate.value
      if estimate.parameter.property.abv=='nu':    nu1  = estimate.value

      if estimate.parameter.property.abv=='cx':    cx   = estimate.value
      if estimate.parameter.property.abv=='cy':    cy   = estimate.value
      if estimate.parameter.property.abv=='lr':    lr   = estimate.value
    if estimate.parameter.structure.domain.title=='Formation':
      if estimate.parameter.property.abv=='kappa': k2   = estimate.value
      if estimate.parameter.property.abv=='K':     K2   = estimate.value
      if estimate.parameter.property.abv=='Ks':    Ks2  = estimate.value
      if estimate.parameter.property.abv=='Kf':    Kf2  = estimate.value
      if estimate.parameter.property.abv=='phi':   phi2 = estimate.value
      if estimate.parameter.property.abv=='nu':    nu2  = estimate.value
    if estimate.parameter.structure.domain.title=='Confining':
      if estimate.parameter.property.abv=='kappa': k3   = estimate.value
      if estimate.parameter.property.abv=='K':     K3   = estimate.value
      if estimate.parameter.property.abv=='Ks':    Ks3  = estimate.value
      if estimate.parameter.property.abv=='Kf':    Kf3  = estimate.value
      if estimate.parameter.property.abv=='phi':   phi3 = estimate.value
      if estimate.parameter.property.abv=='nu':    nu3  = estimate.value

  wx  = 0
  wy  = 0
  if ((cx-wx)**2+(cy-wy)**2)**0.5>lr: return False

  wx = -375.9
  wy = -5.4
  if ((cx-wx)**2+(cy-wy)**2)**0.5>lr: return False

  wx = -185.0
  wy = +28.7
  if ((cx-wx)**2+(cy-wy)**2)**0.5>lr: return False

  wx = -245.0
  wy = -111.7
  if ((cx-wx)**2+(cy-wy)**2)**0.5>lr: return False

  return True
