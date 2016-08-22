import math
import numpy

from bordr3 import bordr3

def rtp3d(fin, ra1, rb1):
    # GridRTP=rtp3d(GridTMI,incl_fld,decl_fld)
    # RTP3D  Reduce a magnetic field anomaly map to the pole 
    # using Fourier transform and specifying inclination and 
    # declination of the field and magnetization
    #  fin is input TMI grid
    #  fout is output array
    #
    #  PC-MATLAB
    #  Maurice A. Tivey March 16 1992/ June 1994

    rad = math.pi / 180  # conversion radians to degrees
    mu = 100      # units to nT

    if numpy.isscalar(ra1):
        ra1 = numpy.array([ra1])

    if numpy.isscalar(rb1):
        rb1 = numpy.array([rb1])

    ra1 = ra1 * rad
    rb1 = rb1 * rad
    ra2 = ra1
    rb2 = rb1

    # Expand the grid to avoid edge effects
    Nrow, Ncol = fin.shape
    fin = bordr3(fin, 800, 800)
    ny, nx = fin.shape

    ni = 1. / nx
    nx2 = nx / 2.
    nx2plus = nx2 + 1

    x = numpy.arange(-.5, .5, ni)
    ni = 1. / ny
    ny2 = ny / 2.
    ny2plus = ny2 + 1
    y = numpy.expand_dims(numpy.arange(-.5, .5, ni), 0)

    X = numpy.ones(y.shape).T * x
    Y = y.T * numpy.ones(x.shape)
    k = 2 * math.pi * numpy.sqrt(numpy.power(X, 2) + numpy.power(Y, 2))  # wavenumber array
    #
    #------ calculate geometric and amplitude factors
    Ob = (numpy.sin(ra1) + 1j * numpy.cos(ra1) * numpy.sin(numpy.arctan2(Y, X) + rb1))
    Om = (numpy.sin(ra2) + 1j * numpy.cos(ra2) * numpy.sin(numpy.arctan2(Y, X) + rb2))
    O = (Ob * Om)
    # alternate calculation
    # O=phase3d(ra1,rb1,ra2,rb2,nx,ny)
    #  O=O./abs(k.^2)

    # calculate northpole phase
    ra1 = 90 * rad
    rb1 = 0
    ONP = (numpy.sin(ra1) + 1j * numpy.cos(ra1) * numpy.sin(numpy.arctan2(Y, X) + rb1))
    ONP = (ONP * ONP)
    # alternate calculation
    # ONP=phase3d(90,0,90,0,nx,ny)
    # ONP=ONP./abs(k.^2)

    amp = numpy.absolute(O)       # amplitude factor
    phase = numpy.angle(O)   # phase angle 
    F = numpy.fft.fft2(fin)
    F = numpy.fft.fftshift(F) / O
    #------------------ INVERSE fft ----------------
    fout = numpy.fft.ifft2(numpy.fft.fftshift(F * ONP))

    fout = fout[0:Nrow, 0:Ncol]
    fout = numpy.real(fout)

    return fout
