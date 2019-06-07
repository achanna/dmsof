import numpy as np
import math

class Cuboid3d:

  def __init__(self): pass

  def set_a(self,a): self.a = a
  def set_b(self,b): self.b = b
  def set_c(self,c): self.c = c
  def set_h(self,h): self.h = h

  def set_alpha(self,alpha): self.alpha = float(alpha)
  def set_nu(self,nu):       self.nu    = float(nu)
  def set_E(self,E):         self.E     = float(E)
  def set_delp(self,delp):   self.delp  = float(delp)

  def set_d0(self):          self.d0 = self.alpha * (1.0-2.0*self.nu) / self.E * self.delp

  def I_x_inf_cuboid(self,x,y,z):
    a = float(self.a)
    b = float(self.b)
    c = float(self.c)
    h = float(self.h)
    output = 0.0
    nh = 200
    delz1 = (2.0*c)/float(nh)
    for z1 in np.linspace(h-c,h+c,nh+1):
      term1 = float( ( (x+a)**2+(z-z1)**2+(y-b)**2)**0.5 + b - y )
      term2 = float( ( (x-a)**2+(z-z1)**2+(y-b)**2)**0.5 + b - y )
      term3 = float( ( (x-a)**2+(z-z1)**2+(y+b)**2)**0.5 - b - y )
      term4 = float( ( (x+a)**2+(z-z1)**2+(y+b)**2)**0.5 - b - y )
      output += np.log( (term1/term2) * (term3/term4) ) * delz1
    return output

  def I_y_inf_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    output = 0.0
    nh = 200
    for z1 in np.linspace(h-c,h+c,nh+1):
      term1 = float(((y+b)**2+(z-z1)**2+(x-a)**2)**0.5+a-x)
      term2 = float(((y-b)**2+(z-z1)**2+(x-a)**2)**0.5+a-x)
      term3 = float(((y-b)**2+(z-z1)**2+(x+a)**2)**0.5-a-x)
      term4 = float(((y+b)**2+(z-z1)**2+(x+a)**2)**0.5-a-x)
      output += np.log( (term1/term2) * (term3/term4) ) * (2*c/float(nh))
    return output

  def I_z_inf_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    output = 0.0
    na = 200
    for x1 in np.linspace(-a,a,na+1):
      term1 = ((z-(h-c))**2+(x-x1)**2+(y-b)**2)**0.5+b-y
      term2 = ((z-(h+c))**2+(x-x1)**2+(y-b)**2)**0.5+b-y
      term3 = ((z-(h+c))**2+(x-x1)**2+(y+b)**2)**0.5-b-y
      term4 = ((z-(h-c))**2+(x-x1)**2+(y+b)**2)**0.5-b-y
      output += np.log( (term1/term2) * (term3/term4) ) * (2*a/float(na))
    return output

  def Ip_x_z_inf_1_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    output = 0.0
    nh = 200
    for z1 in np.linspace(h-c,h+c,nh+1):
      term1 = z-z1
      term2 = ((a+x)**2+(b-y)**2+(z-z1)**2)**0.5
      term3 = b-y+term2
      term4 = z1-z
      term5 = ((a-x)**2+(b-y)**2+(z-z1)**2)**0.5
      term6 = b-y+term5
      output += ( (term1/(term2*term3)+term4/(term5*term6)) * (2.0*c/float(nh)) )
    return output

  def Ip_x_z_inf_2_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    output = 0.0
    nh = 200
    for z1 in np.linspace(h-c,h+c,nh+1):
      term1 = z1-z
      term2 = ((a+x)**2+(b+y)**2+(z-z1)**2)**0.5
      term3 = b+y-term2
      term4 = z-z1
      term5 = ((a-x)**2+(b+y)**2+(z-z1)**2)**0.5
      term6 = b+y-term5
      output += ( (term1/(term2*term3)+term4/(term5*term6)) * (2.0*c/float(nh)) )
    return output

  def Ip_y_z_inf_1_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    output = 0.0
    nh = 200
    for z1 in np.linspace(h-c,h+c,nh+1):
      term1 = z-z1
      term2 = ((a-x)**2+(b+y)**2+(z-z1)**2)**0.5
      term3 = a-x+term2
      term4 = z1-z
      term5 = ((a-x)**2+(b-y)**2+(z-z1)**2)**0.5
      term6 = a-x+term5
      output += (term1/(term2*term3)+term4/(term5*term6)) * (2.0*c/float(nh))
    return output

  def Ip_y_z_inf_2_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    output = 0.0
    nh = 200
    for z1 in np.linspace(h-c,h+c,nh+1):
      term1 = z1-z
      term2 = ((a+x)**2+(b+y)**2+(z-z1)**2)**0.5
      term3 = a+x-term2
      term4 = z-z1
      term5 = ((a+x)**2+(b-y)**2+(z-z1)**2)**0.5
      term6 = a+x-term5
      output += (term1/(term2*term3)+term4/(term5*term6)) * (2.0*c/float(nh))
    return output

  def Ip_z_z_inf_1_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    output = 0.0
    na = 200
    for x1 in np.linspace(-a,+a,na+1):
      term1 = c-h+z
      term2 = ((c-h+z)**2+(b-y)**2+(x-x1)**2)**0.5
      term3 = b-y+term2
      term4 = c+h-z
      term5 = ((c+h-z)**2+(b-y)**2+(x-x1)**2)**0.5
      term6 = b-y+term5
      output += (term1/(term2*term3)+term4/(term5*term6)) * (2.0*a/float(na))
    return output

  def Ip_z_z_inf_2_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    output = 0.0
    na = 200
    for x1 in np.linspace(-a,+a,na+1):
      term1 = c+h-z
      term2 = ((c+h-z)**2+(b+y)**2+(x-x1)**2)**0.5
      term3 = b+y-term2
      term4 = c-h+z
      term5 = ((c-h+z)**2+(b+y)**2+(x-x1)**2)**0.5
      term6 = b+y-term5
      output += (term1/(term2*term3)+term4/(term5*term6)) * (2.0*a/float(na))
    return -output

  def Ip_x_z_inf_cuboid(self,x,y,z): return self.Ip_x_z_inf_1_cuboid(x,y,z)-self.Ip_x_z_inf_2_cuboid(x,y,z)
  def Ip_y_z_inf_cuboid(self,x,y,z): return self.Ip_y_z_inf_1_cuboid(x,y,z)-self.Ip_y_z_inf_2_cuboid(x,y,z)
  def Ip_z_z_inf_cuboid(self,x,y,z): return self.Ip_z_z_inf_1_cuboid(x,y,z)-self.Ip_z_z_inf_2_cuboid(x,y,z)

  def u_x_inf_cuboid(self,x,y,z):
    nu = float(self.nu)
    d0 = float(self.d0)
    I  = self.I_x_inf_cuboid(x,y,z)
    term1 = (-1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu)
    return term1*term2*d0*I

  def u_y_inf_cuboid(self,x,y,z):
    nu = self.nu
    d0 = self.d0
    I = self.I_y_inf_cuboid(x,y,z)
    term1 = - (1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu) * d0
    return term1*term2*I

  def u_z_inf_cuboid(self,x,y,z):
    nu = self.nu
    d0 = self.d0
    I = self.I_z_inf_cuboid(x,y,z)
    term1 = - (1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu) * d0
    return term1*term2*I

  def up_x_z_inf_cuboid(self,x,y,z):
    nu = self.nu
    d0 = self.d0
    I = self.Ip_x_z_inf_cuboid(x,y,z)
    term1 = - (1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu) * d0
    return term1*term2*I

  def up_y_z_inf_cuboid(self,x,y,z):
    nu = self.nu
    d0 = self.d0
    I = self.Ip_y_z_inf_cuboid(x,y,z)
    term1 = - (1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu) * d0
    return term1*term2*I

  def up_z_z_inf_cuboid(self,x,y,z):
    nu = self.nu
    d0 = self.d0
    I = self.Ip_z_z_inf_cuboid(x,y,z)
    term1 = - (1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu) * d0
    return term1*term2*I

  def u_x_inf_image_cuboid(self,x,y,z): return self.u_x_inf_cuboid(x,y,-z)
  def u_y_inf_image_cuboid(self,x,y,z): return self.u_y_inf_cuboid(x,y,-z)
  def u_z_inf_image_cuboid(self,x,y,z): return self.u_z_inf_cuboid(x,y,-z)

  def up_x_z_inf_image_cuboid(self,x,y,z): return -self.up_x_z_inf_cuboid(x,y,-z)
  def up_y_z_inf_image_cuboid(self,x,y,z): return -self.up_y_z_inf_cuboid(x,y,-z)
  def up_z_z_inf_image_cuboid(self,x,y,z): return -self.up_z_z_inf_cuboid(x,y,-z)

  def u_x_cuboid(self,x,y,z):
    nu    = self.nu
    term1 = self.u_x_inf_cuboid(x,y,z)
    term2 = self.u_x_inf_image_cuboid(x,y,z)
    term3 = self.up_x_z_inf_image_cuboid(x,y,z)
    return term1+(3-4*nu)*term2+2*z*term3

  def u_y_cuboid(self,x,y,z):
    nu    = self.nu
    term1 = self.u_y_inf_cuboid(x,y,z)
    term2 = self.u_y_inf_image_cuboid(x,y,z)
    term3 = self.up_y_z_inf_image_cuboid(x,y,z)
    return term1+(3-4*nu)*term2+2*z*term3

  def u_z_cuboid(self,x,y,z):
    nu    = self.nu
    term1 = self.u_z_inf_cuboid(x,y,z)
    term2 = self.u_z_inf_image_cuboid(x,y,z)
    term3 = self.up_z_z_inf_image_cuboid(x,y,z)
    return term1+(3-4*nu)*term2-2*z*term3

  def u_x_inf_image_cuboid(self,x,y,z): return self.u_x_inf_cuboid(x,y,-z)
  def u_y_inf_image_cuboid(self,x,y,z): return self.u_y_inf_cuboid(x,y,-z)
  def u_z_inf_image_cuboid(self,x,y,z): return self.u_z_inf_cuboid(x,y,-z)

  def up_x_z_inf_image_cuboid(self,x,y,z): return -self.up_x_z_inf_cuboid(x,y,-z)
  def up_y_z_inf_image_cuboid(self,x,y,z): return -self.up_y_z_inf_cuboid(x,y,-z)
  def up_z_z_inf_image_cuboid(self,x,y,z): return -self.up_z_z_inf_cuboid(x,y,-z)

  def comp_sign(self,input):
    if input==0:         return 0
    if np.real(input)>0: return 1
    else: return -1

  def J_xx_cuboid(self,x,y,z,z1,a,b):
    if x==-a or y==-b: return 0
    term1 = self.comp_sign(x+a) * self.comp_sign(y+b)
    term2 = (z-z1)*((y+b)**2)**0.5
    term3 = ((x+a)**2)**0.5 * ( (x+a)**2 + (y+b)**2 + (z-z1)**2 )**0.5
    return term1 * math.atan( - term2 / term3 )

  def J_yy_cuboid(self,x,y,z,z1,a,b):
    if x==-a or y==-b: return 0
    term1 = self.comp_sign(x+a) * self.comp_sign(y+b)
    term2 = (z-z1)*((x+a)**2)**0.5
    term3 = ((y+b)**2)**0.5 * ( (x+a)**2 + (y+b)**2 + (z-z1)**2 )**0.5
    return term1 * math.atan( - term2 / term3 )

  def J_zz_cuboid(self,x,y,z,y1,d,a):
    if x==-a or z==d: return 0
    term1 = self.comp_sign(x+a) * self.comp_sign(z-d)
    term2 = ((x+a)**2)**0.5 * (y-y1)
    term3 = ((z-d)**2)**0.5 * ( (x+a)**2 + (z-d)**2 + (y-y1)**2 )**0.5
    return term1 * math.atan( - term2 / term3 )

  def I_xx_inf_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    term1 = self.J_xx_cuboid(x,y,z,h+c,+a,-b)
    term2 = self.J_xx_cuboid(x,y,z,h-c,+a,-b)
    term3 = self.J_xx_cuboid(x,y,z,h+c,-a,-b)
    term4 = self.J_xx_cuboid(x,y,z,h-c,-a,-b)
    term5 = self.J_xx_cuboid(x,y,z,h+c,-a,+b)
    term6 = self.J_xx_cuboid(x,y,z,h-c,-a,+b)
    term7 = self.J_xx_cuboid(x,y,z,h+c,+a,+b)
    term8 = self.J_xx_cuboid(x,y,z,h-c,+a,+b)
    return term1-term2-term3+term4+term5-term6-term7+term8

  def I_yy_inf_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    term1 = self.J_yy_cuboid(x,y,z,h+c,+a,-b)
    term2 = self.J_yy_cuboid(x,y,z,h-c,+a,-b)
    term3 = self.J_yy_cuboid(x,y,z,h+c,-a,-b)
    term4 = self.J_yy_cuboid(x,y,z,h-c,-a,-b)
    term5 = self.J_yy_cuboid(x,y,z,h+c,-a,+b)
    term6 = self.J_yy_cuboid(x,y,z,h-c,-a,+b)
    term7 = self.J_yy_cuboid(x,y,z,h+c,+a,+b)
    term8 = self.J_yy_cuboid(x,y,z,h-c,+a,+b)
    return term1-term2-term3+term4+term5-term6-term7+term8

  def I_zz_inf_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    term1 = self.J_zz_cuboid(x,y,z,+b,h+c,+a)
    term2 = self.J_zz_cuboid(x,y,z,-b,h+c,+a)
    term3 = self.J_zz_cuboid(x,y,z,+b,h+c,-a)
    term4 = self.J_zz_cuboid(x,y,z,-b,h+c,-a)
    term5 = self.J_zz_cuboid(x,y,z,+b,h-c,-a)
    term6 = self.J_zz_cuboid(x,y,z,-b,h-c,-a)
    term7 = self.J_zz_cuboid(x,y,z,+b,h-c,+a)
    term8 = self.J_zz_cuboid(x,y,z,-b,h-c,+a)
    return term1-term2-term3+term4+term5-term6-term7+term8

  def eps_xx_inf_cuboid(self,x,y,z):
    nu = self.nu
    d0 = self.d0
    I = self.I_xx_inf_cuboid(x,y,z)
    term1 = -(1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu) * d0
    return term1*term2*I

  def eps_yy_inf_cuboid(self,x,y,z):
    nu = self.nu
    d0 = self.d0
    I = self.I_yy_inf_cuboid(x,y,z)
    term1 = -(1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu) * d0
    return term1*term2*I

  def eps_zz_inf_cuboid(self,x,y,z):
    nu = self.nu
    d0 = self.d0
    I = self.I_zz_inf_cuboid(x,y,z)
    term1 = -(1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu) * d0
    return term1*term2*I

  def XY_cuboid(self,x,y,z,a,b,d):
    term1 = d-z+( (x-a)**2+(y-b)**2+(z-d)**2 )**0.5
    term2 = d-z+( (x+a)**2+(y-b)**2+(z-d)**2 )**0.5
    return np.log(term1/term2)

  def YZ_cuboid(self,x,y,z,a,b,c,h):
    term1 = a-x+( (x-a)**2+(y-b)**2+(z-(h+c))**2 )**0.5
    term2 = a-x+( (x-a)**2+(y-b)**2+(z-(h-c))**2 )**0.5
    return np.log(term1/term2)

  def XZ_cuboid(self,x,y,z,a,b,c,h):
    term1 = b-y+( (x-a)**2+(y-b)**2+(z-(h+c))**2 )**0.5
    term2 = b-y+( (x-a)**2+(y-b)**2+(z-(h-c))**2 )**0.5
    return np.log(term1/term2)

  def I_xy_inf_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    term1 = self.XY_cuboid(x,y,z,+a,+b,h+c)
    term2 = self.XY_cuboid(x,y,z,+a,+b,h-c)
    term3 = self.XY_cuboid(x,y,z,-a,-b,h+c)
    term4 = self.XY_cuboid(x,y,z,-a,-b,h-c)
    return term1-term2+term3-term4

  def I_yz_inf_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    term1 = self.YZ_cuboid(x,y,z,+a,+b,+c,+h)
    term2 = self.YZ_cuboid(x,y,z,-a,+b,+c,+h)
    term3 = self.YZ_cuboid(x,y,z,+a,-b,-c,+h)
    term4 = self.YZ_cuboid(x,y,z,-a,-b,-c,+h)
    return term1-term2+term3-term4

  def I_xz_inf_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    term1 = self.XZ_cuboid(x,y,z,+a,+b,+c,+h)
    term2 = self.XZ_cuboid(x,y,z,+a,-b,+c,+h)
    term3 = self.XZ_cuboid(x,y,z,-a,+b,-c,+h)
    term4 = self.XZ_cuboid(x,y,z,-a,-b,-c,+h)
    return term1-term2+term3-term4

  def eps_xy_inf_cuboid(self,x,y,z):
    nu = self.nu
    d0 = self.d0
    I = self.I_xy_inf_cuboid(x,y,z)
    term1 = -(1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu) * d0
    return term1*term2*I

  def eps_yz_inf_cuboid(self,x,y,z):
    nu = self.nu
    d0 = self.d0
    I = self.I_yz_inf_cuboid(x,y,z)
    term1 = -(1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu) * d0
    return term1*term2*I

  def eps_xz_inf_cuboid(self,x,y,z):
    nu = self.nu
    d0 = self.d0
    I = self.I_xz_inf_cuboid(x,y,z)
    term1 = -(1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu) * d0
    return term1*term2*I

  def Jp_xx_z_cuboid(self,x,y,z,z1,a,b):
    if x==-a or y==-b: return 0
    term1 = (x+a) * (y+b) * ( (x+a)**2 + (y+b)**2 )
    term2 = ((z-z1)**2 * (y+b)**2) + (x+a)**2 * ( (x+a)**2 + (y+b)**2 + (z-z1)**2 )
    term3 = ( (x+a)**2 + (y+b)**2 + (z-z1)**2 )**0.5
    return - term1 / ( term2 * term3 )

  def Jp_yy_z_cuboid(self,x,y,z,z1,a,b):
    if x==-a or y==-b: return 0
    term1 = (x+a) * (y+b) * ( (x+a)**2 + (y+b)**2 )
    term2 = ((z-z1)**2 * (x+a)**2) + (y+b)**2 * ( (x+a)**2 + (y+b)**2 + (z-z1)**2 )
    term3 = ( (x+a)**2 + (y+b)**2 + (z-z1)**2 )**0.5
    return - term1 / ( term2 * term3 )

  def Jp_zz_z_cuboid(self,x,y,z,y1,d,a):
    if x==-a or z==d: return 0
    term1 = (x+a)**2+(y-y1)**2+2.0*(z-d)**2
    term2 = ( (x+a)**2 + (y-y1)**2 + (z-d)**2 )**0.5
    term3 = (y-y1)*(x+a)
    term4 = ( (y-y1)**2 * (x+a)**2 ) + ( (d-z)**2 * ( (x+a)**2 + (y-y1)**2 + (z-d)**2 ) )
    return ( term1 / term2 ) * ( term3 / term4 )

  def Ip_xx_inf_z_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    term1 = self.Jp_xx_z_cuboid(x,y,z,+h+c,+a,-b)
    term2 = self.Jp_xx_z_cuboid(x,y,z,+h-c,+a,-b)
    term3 = self.Jp_xx_z_cuboid(x,y,z,+h-c,-a,-b)
    term4 = self.Jp_xx_z_cuboid(x,y,z,+h+c,-a,-b)
    term5 = self.Jp_xx_z_cuboid(x,y,z,+h+c,-a,+b)
    term6 = self.Jp_xx_z_cuboid(x,y,z,+h-c,-a,+b)
    term7 = self.Jp_xx_z_cuboid(x,y,z,+h-c,+a,+b)
    term8 = self.Jp_xx_z_cuboid(x,y,z,+h+c,+a,+b)
    return term1-term2+term3-term4+term5-term6+term7-term8

  def Ip_yy_inf_z_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    term1 = self.Jp_yy_z_cuboid(x,y,z,+h+c,+a,-b)
    term2 = self.Jp_yy_z_cuboid(x,y,z,+h-c,+a,-b)
    term3 = self.Jp_yy_z_cuboid(x,y,z,+h-c,-a,-b)
    term4 = self.Jp_yy_z_cuboid(x,y,z,+h+c,-a,-b)
    term5 = self.Jp_yy_z_cuboid(x,y,z,+h+c,-a,+b)
    term6 = self.Jp_yy_z_cuboid(x,y,z,+h-c,-a,+b)
    term7 = self.Jp_yy_z_cuboid(x,y,z,+h-c,+a,+b)
    term8 = self.Jp_yy_z_cuboid(x,y,z,+h+c,+a,+b)
    return term1-term2+term3-term4+term5-term6+term7-term8

  def Ip_zz_inf_z_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    term1 = self.Jp_zz_z_cuboid(x,y,z,+b,+h+c,+a)
    term2 = self.Jp_zz_z_cuboid(x,y,z,-b,+h+c,+a)
    term3 = self.Jp_zz_z_cuboid(x,y,z,-b,+h+c,-a)
    term4 = self.Jp_zz_z_cuboid(x,y,z,+b,+h+c,-a)
    term5 = self.Jp_zz_z_cuboid(x,y,z,+b,+h-c,-a)
    term6 = self.Jp_zz_z_cuboid(x,y,z,-b,+h-c,-a)
    term7 = self.Jp_zz_z_cuboid(x,y,z,-b,+h-c,+a)
    term8 = self.Jp_zz_z_cuboid(x,y,z,+b,+h-c,+a)
    return term1-term2+term3-term4+term5-term6+term7-term8

  def epsp_xx_inf_z_cuboid(self,x,y,z):
    nu = self.nu
    d0 = self.d0
    I = self.Ip_xx_inf_z_cuboid(x,y,z)
    term1 = -(1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu) * d0
    return term1*term2*I

  def epsp_yy_inf_z_cuboid(self,x,y,z):
    nu = self.nu
    d0 = self.d0
    I = self.Ip_yy_inf_z_cuboid(x,y,z)
    term1 = -(1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu) * d0
    return term1*term2*I

  def epsp_zz_inf_z_cuboid(self,x,y,z):
    nu = self.nu
    d0 = self.d0
    I = self.Ip_zz_inf_z_cuboid(x,y,z)
    term1 = -(1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu) * d0
    return term1*term2*I

  def XY_z_cuboid(self,x,y,z,a,b,d):
    term1 = ( (x-a)**2+(y-b)**2+(z-d)**2 )**0.5
    return 1.0 / term1

  def Y_z_cuboid(self,x,y,z,a,b,d):
    term1 = ( (x-a)**2+(y-b)**2+(z-d)**2 )**0.5
    term2 = (d-z) / ( (a-x + term1) * term1 )
    return term2

  def X_z_cuboid(self,x,y,z,a,b,d):
    term1 = ( (x-a)**2+(y-b)**2+(z-d)**2 )**0.5
    term2 = (d-z) / ( (b-y + term1) * term1 )
    return term2

  def Ip_xy_inf_z_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    term1 = self.XY_z_cuboid(x,y,z,-a,+b,h+c)
    term2 = self.XY_z_cuboid(x,y,z,+a,+b,h+c)
    term3 = self.XY_z_cuboid(x,y,z,+a,+b,h-c)
    term4 = self.XY_z_cuboid(x,y,z,-a,+b,h-c)
    term5 = self.XY_z_cuboid(x,y,z,+a,-b,h+c)
    term6 = self.XY_z_cuboid(x,y,z,-a,-b,h+c)
    term7 = self.XY_z_cuboid(x,y,z,-a,-b,h-c)
    term8 = self.XY_z_cuboid(x,y,z,+a,-b,h-c)
    return term1-term2+term3-term4+term5-term6+term7-term8

  def Ip_yz_inf_z_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    term1 = self.Y_z_cuboid(x,y,z,+a,+b,h+c)
    term2 = self.Y_z_cuboid(x,y,z,+a,+b,h-c)
    term3 = self.Y_z_cuboid(x,y,z,-a,+b,h+c)
    term4 = self.Y_z_cuboid(x,y,z,-a,+b,h-c)
    term5 = self.Y_z_cuboid(x,y,z,+a,-b,h+c)
    term6 = self.Y_z_cuboid(x,y,z,+a,-b,h-c)
    term7 = self.Y_z_cuboid(x,y,z,-a,-b,h-c)
    term8 = self.Y_z_cuboid(x,y,z,-a,-b,h+c)
    return -term1+term2+term3-term4+term5-term6+term7-term8

  def Ip_xz_inf_z_cuboid(self,x,y,z):
    a = self.a
    b = self.b
    c = self.c
    h = self.h
    term1 = self.X_z_cuboid(x,y,z,+a,+b,h+c)
    term2 = self.X_z_cuboid(x,y,z,+a,+b,h-c)
    term3 = self.X_z_cuboid(x,y,z,+a,-b,h+c)
    term4 = self.X_z_cuboid(x,y,z,+a,-b,h-c)
    term5 = self.X_z_cuboid(x,y,z,-a,+b,h+c)
    term6 = self.X_z_cuboid(x,y,z,-a,+b,h-c)
    term7 = self.X_z_cuboid(x,y,z,-a,-b,h-c)
    term8 = self.X_z_cuboid(x,y,z,-a,-b,h+c)
    return -term1+term2+term3-term4+term5-term6+term7-term8

  def epsp_xy_inf_z_cuboid(self,x,y,z):
    nu = self.nu
    d0 = self.d0
    I = self.Ip_xy_inf_z_cuboid(x,y,z)
    term1 = -(1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu) * d0
    return term1*term2*I

  def epsp_yz_inf_z_cuboid(self,x,y,z):
    nu = self.nu
    d0 = self.d0
    I = self.Ip_yz_inf_z_cuboid(x,y,z)
    term1 = -(1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu) * d0
    return term1*term2*I

  def epsp_xz_inf_z_cuboid(self,x,y,z):
    nu = self.nu
    d0 = self.d0
    I = self.Ip_xz_inf_z_cuboid(x,y,z)
    term1 = -(1.0)/(4.0*math.pi)
    term2 = (1+nu)/(1-nu) * d0
    return term1*term2*I

  def eps_xx_inf_image_cuboid(self,x,y,z): return self.eps_xx_inf_cuboid(x,y,-z)
  def eps_yy_inf_image_cuboid(self,x,y,z): return self.eps_yy_inf_cuboid(x,y,-z)
  def eps_zz_inf_image_cuboid(self,x,y,z): return self.eps_zz_inf_cuboid(x,y,-z)
  def eps_xy_inf_image_cuboid(self,x,y,z): return self.eps_xy_inf_cuboid(x,y,-z)
  def eps_yz_inf_image_cuboid(self,x,y,z): return self.eps_yz_inf_cuboid(x,y,-z)
  def eps_xz_inf_image_cuboid(self,x,y,z): return self.eps_xz_inf_cuboid(x,y,-z)

  def epsp_xx_inf_image_z_cuboid(self,x,y,z): return -self.epsp_xx_inf_z_cuboid(x,y,-z)
  def epsp_yy_inf_image_z_cuboid(self,x,y,z): return -self.epsp_yy_inf_z_cuboid(x,y,-z)
  def epsp_zz_inf_image_z_cuboid(self,x,y,z): return -self.epsp_zz_inf_z_cuboid(x,y,-z)
  def epsp_xy_inf_image_z_cuboid(self,x,y,z): return -self.epsp_xy_inf_z_cuboid(x,y,-z)
  def epsp_yz_inf_image_z_cuboid(self,x,y,z): return -self.epsp_yz_inf_z_cuboid(x,y,-z)
  def epsp_xz_inf_image_z_cuboid(self,x,y,z): return -self.epsp_xz_inf_z_cuboid(x,y,-z)

  def omega_xy_cuboid(self,x,y,z):
    nu = self.nu
    term1 = self.eps_xy_inf_cuboid(x,y,z)
    term2 = (3-4*nu) * self.eps_xy_inf_image_cuboid(x,y,z)
    term3 = 2*z*self.epsp_yz_inf_image_z_cuboid(x,y,z)
    return term1+term2+term3

  def omega_xz_cuboid(self,x,y,z):
    nu = self.nu
    term1 = self.eps_xz_inf_cuboid(x,y,z)
    term2 = (3-4*nu) * self.eps_xz_inf_image_cuboid(x,y,z)
    term3 = -2*self.eps_xz_inf_image_cuboid(x,y,z)
    term4 = -2*z*self.epsp_xz_inf_image_z_cuboid(x,y,z)
    return term1-term2+term3+term4

  def omega_zx_cuboid(self,x,y,z):
    nu = self.nu
    term1 = self.eps_xz_inf_cuboid(x,y,z)
    term2 = (3-4*nu) * self.eps_xz_inf_image_cuboid(x,y,z)
    term3 = -2*z*self.epsp_xz_inf_image_z_cuboid(x,y,z)
    return term1+term2+term3

  def omega_yz_cuboid(self,x,y,z):
    nu = self.nu
    term1 = self.eps_yz_inf_cuboid(x,y,z)
    term2 = (3-4*nu) * self.eps_yz_inf_image_cuboid(x,y,z)
    term3 = -2*self.eps_yz_inf_image_cuboid(x,y,z)
    term4 = -2*z*self.epsp_yz_inf_image_z_cuboid(x,y,z)
    return term1-term2+term3+term4

  def omega_zy_cuboid(self,x,y,z):
    nu = self.nu
    term1 = self.eps_yz_inf_cuboid(x,y,z)
    term2 = (3-4*nu) * self.eps_yz_inf_image_cuboid(x,y,z)
    term3 = -2*z*self.epsp_yz_inf_image_z_cuboid(x,y,z)
    return term1+term2+term3

  def eps_xx_cuboid(self,x,y,z):
    nu = self.nu
    term1 = self.eps_xx_inf_cuboid(x,y,z)
    term2 = (3-4*nu) * self.eps_xx_inf_image_cuboid(x,y,z)
    term3 = 2*z*self.epsp_xx_inf_image_z_cuboid(x,y,z)
    return term1+term2+term3

  def eps_yy_cuboid(self,x,y,z):
    nu = self.nu
    term1 = self.eps_yy_inf_cuboid(x,y,z)
    term2 = (3-4*nu) * self.eps_yy_inf_image_cuboid(x,y,z)
    term3 = 2*z*self.epsp_yy_inf_image_z_cuboid(x,y,z)
    return term1+term2+term3

  def eps_zz_cuboid(self,x,y,z):
    nu = self.nu
    term1 = self.eps_zz_inf_cuboid(x,y,z)
    term2 = (1-4*nu) * self.eps_zz_inf_image_cuboid(x,y,z)
    term3 = 2*z*self.epsp_zz_inf_image_z_cuboid(x,y,z)
    return term1+term2+term3

  def eps_xy_cuboid(self,x,y,z): return self.omega_xy_cuboid(x,y,z)
  def eps_xz_cuboid(self,x,y,z): return ( self.omega_xz_cuboid(x,y,z)+self.omega_zx_cuboid(x,y,z) ) / 2.0
  def eps_yz_cuboid(self,x,y,z): return ( self.omega_yz_cuboid(x,y,z)+self.omega_zy_cuboid(x,y,z) ) / 2.0
