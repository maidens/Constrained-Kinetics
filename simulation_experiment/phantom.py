import numpy

def sphere(x, y, z, radius, x0, y0, z0):
    return 1.0*((x-x0)**2 + (y-y0)**2 + (z-z0)**2 < (radius)**2)

def rectangle(x, y, z, Lx, Ly, Lz, x0, y0, z0):
    return ((numpy.abs(x-x0)<Lx/2*numpy.ones(x.shape))*(numpy.abs(y-y0)<Ly/2*numpy.ones(y.shape)) * (numpy.abs(y-y0)<Ly/2*numpy.ones(z.shape)))

def dynamic_phantom(nx, ny, nz, kTRANS_low, kTRANS_high, kPL_low, kPL_high, linear_kPL_gradient=False, linear_kTRANS_gradient=False):
    x = numpy.linspace(-1, 1, nx)
    y = numpy.linspace(-1, 1, ny)
    z = numpy.linspace(-1, 1, nz)

    X, Y, Z = numpy.meshgrid(x, y, z)

    kTRANS = numpy.zeros(X.shape)
    if linear_kTRANS_gradient:
        scale = scale = 0.5*(kTRANS_low - kTRANS_high)*X + 0.5*(kTRANS_low + kTRANS_high)
        kTRANS += scale*rectangle(X, Y, Z, 1.6, 1.6, 1.6, 0, 0, 0)
    else:
        kTRANS += kTRANS_low*rectangle(X, Y, Z, 0.8, 1.6, 1.6, 0.4, 0, 0)
        kTRANS += kTRANS_high*rectangle(X, Y, Z, 0.8, 1.6, 1.6, -0.4, 0, 0)

    kPL = numpy.zeros(X.shape)
    large_radius = 0.35
    small_radius = 0.10
    ball_center = 0.45
    if linear_kPL_gradient:
        scale = 0.5*(kPL_low - kPL_high)*Y + 0.5*(kPL_low + kPL_high)
        kPL += scale*sphere(X, Y, Z, large_radius,  ball_center,  ball_center, 0) + (kPL_high - scale)*sphere(X, Y, Z, small_radius,  ball_center,  ball_center, 0)
        kPL += scale*sphere(X, Y, Z, large_radius, -ball_center,  ball_center, 0) + (kPL_high - scale)*sphere(X, Y, Z, small_radius, -ball_center,  ball_center, 0)
        kPL += scale*sphere(X, Y, Z, large_radius,  ball_center, -ball_center, 0) + (kPL_low  - scale)*sphere(X, Y, Z, small_radius,  ball_center, -ball_center, 0)
        kPL += scale*sphere(X, Y, Z, large_radius, -ball_center, -ball_center, 0) + (kPL_low  - scale)*sphere(X, Y, Z, small_radius, -ball_center, -ball_center, 0)
    else:
        kPL += kPL_low *sphere(X, Y, Z, large_radius,  ball_center,  ball_center, 0) + (kPL_high - kPL_low)*sphere(X, Y, Z, small_radius,  ball_center,  ball_center, 0)
        kPL += kPL_low *sphere(X, Y, Z, large_radius, -ball_center,  ball_center, 0) + (kPL_high - kPL_low)*sphere(X, Y, Z, small_radius, -ball_center,  ball_center, 0)
        kPL += kPL_high*sphere(X, Y, Z, large_radius,  ball_center, -ball_center, 0) + (kPL_low - kPL_high)*sphere(X, Y, Z, small_radius,  ball_center, -ball_center, 0)
        kPL += kPL_high*sphere(X, Y, Z, large_radius, -ball_center, -ball_center, 0) + (kPL_low - kPL_high)*sphere(X, Y, Z, small_radius, -ball_center, -ball_center, 0)

    return kTRANS, kPL
