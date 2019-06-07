import cuboid_inclusion as ci

a = 400
b = 1000
c = 25
h = 1700
x = -300
y = 500
z = 150
delp = 118

alpha = 0.70
nu    = 0.25
E     = 1.0e10

a = a*0.3048
b = b*0.3048
c = c*0.3048
h = h*0.3048
x = x*0.3048
y = y*0.3048
z = z*0.3048
delp = delp*6894.76

cuboid = ci.Cuboid3d()

cuboid.set_a(a)
cuboid.set_b(b)
cuboid.set_c(c)
cuboid.set_h(h)

cuboid.set_alpha(alpha)
cuboid.set_nu(nu)
cuboid.set_E(E)
cuboid.set_delp(delp)

cuboid.set_d0()

print cuboid.u_x_inf_cuboid(x,y,z), -5.07886e-6
print cuboid.u_y_inf_cuboid(x,y,z), +6.53365e-6
print cuboid.u_z_inf_cuboid(x,y,z), -2.77194e-5

print cuboid.up_x_z_inf_cuboid(x,y,z), -2.59958e-8
print cuboid.up_y_z_inf_cuboid(x,y,z), +2.80107e-8
print cuboid.up_z_z_inf_cuboid(x,y,z), -8.88255e-8

print cuboid.u_x_inf_image_cuboid(x,y,z), -3.27602e-6
print cuboid.u_y_inf_image_cuboid(x,y,z), +4.48753e-6
print cuboid.u_z_inf_image_cuboid(x,y,z), -2.10287e-5

print cuboid.up_x_z_inf_image_cuboid(x,y,z), +1.47310e-8
print cuboid.up_y_z_inf_image_cuboid(x,y,z), -17.64929e-9
print cuboid.up_z_z_inf_image_cuboid(x,y,z), 5.99370e-8

print cuboid.eps_xx_inf_cuboid(x,y,z), +5.09677e-8
print cuboid.eps_yy_inf_cuboid(x,y,z), +3.78578e-8
print cuboid.eps_zz_inf_cuboid(x,y,z), -8.88255e-8
print cuboid.eps_xy_inf_cuboid(x,y,z), +5.02579e-9
print cuboid.eps_yz_inf_cuboid(x,y,z), +2.80107e-8
print cuboid.eps_xz_inf_cuboid(x,y,z), -2.59958e-8

print cuboid.epsp_xx_inf_z_cuboid(x,y,z), +2.46011e-10
print cuboid.epsp_yy_inf_z_cuboid(x,y,z), +1.58131e-10
print cuboid.epsp_zz_inf_z_cuboid(x,y,z), -4.04142e-10
print cuboid.epsp_xy_inf_z_cuboid(x,y,z), +3.56400e-11
print cuboid.epsp_yz_inf_z_cuboid(x,y,z), +1.46006e-10
print cuboid.epsp_xz_inf_z_cuboid(x,y,z), -1.72015e-10

print cuboid.eps_xx_inf_image_cuboid(x,y,z), +3.35970e-8
print cuboid.eps_yy_inf_image_cuboid(x,y,z), +2.63402e-8
print cuboid.eps_zz_inf_image_cuboid(x,y,z), -5.99370e-8
print cuboid.eps_xy_inf_image_cuboid(x,y,z), +2.70108e-9
print cuboid.eps_yz_inf_image_cuboid(x,y,z), +1.76493e-8
print cuboid.eps_xz_inf_image_cuboid(x,y,z), -1.47310e-8

print cuboid.epsp_xx_inf_image_z_cuboid(x,y,z), -1.44630e-10
print cuboid.epsp_yy_inf_image_z_cuboid(x,y,z), -9.94020e-11
print cuboid.epsp_zz_inf_image_z_cuboid(x,y,z), +2.44032e-10
print cuboid.epsp_xy_inf_image_z_cuboid(x,y,z), -1.75493e-11
print cuboid.epsp_yz_inf_image_z_cuboid(x,y,z), -8.62057e-11
print cuboid.epsp_xz_inf_image_z_cuboid(x,y,z), +8.59788e-11

print cuboid.u_x_cuboid(x,y,z), -1.02839e-5
print cuboid.u_y_cuboid(x,y,z), +1.38948e-5
print cuboid.u_z_cuboid(x,y,z), -7.52576e-5

print cuboid.omega_xy_cuboid(x,y,z), +2.54529e-9
print cuboid.omega_xz_cuboid(x,y,z), +2.50663e-8
print cuboid.omega_zx_cuboid(x,y,z), -6.33197e-8
print cuboid.omega_zy_cuboid(x,y,z), +7.11919e-8
print cuboid.omega_yz_cuboid(x,y,z), -3.47038e-8

print cuboid.eps_xx_cuboid(x,y,z), +1.04936e-7
print cuboid.eps_yy_cuboid(x,y,z), +8.14489e-8
print cuboid.eps_zz_cuboid(x,y,z), -6.65113e-8
print cuboid.eps_xy_cuboid(x,y,z), +2.54259e-9
print cuboid.eps_yz_cuboid(x,y,z), +1.82441e-8
print cuboid.eps_xz_cuboid(x,y,z), -1.91267e-8
