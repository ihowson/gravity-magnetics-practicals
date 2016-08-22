import numpy

from bordr3 import bordr3
from kvalue2 import kvalue2


def verder2(Grid, dx, order):
    # [VerDerGrid] = verder2(Grid,dx,z)
    #  Function to calculate the vertical gradient of a potential field grid
    #  Inputs: Grid =   2D array of gravity/magnetic values
    #                   dx = spacing of grid points in x direction
    #                   order = order of vertical derivative (e.g. 1,2,....)
    # Outputs: VerDerGrid = 2D array of calculated gradient
    #

    dy = dx   # data spacing assumed to be the same in both directions

    # Expand the grid to avoid edge effects
    Nrow, Ncol = Grid.shape
    Grid = bordr3(Grid, 800, 800)

    # Step 1
    # Forward FFT, retrieving grid of Wavenumber domain coordinates
    Spec = numpy.fft.fftshift(numpy.fft.fft2(Grid))
    ny, nx = Spec.shape
    kx, ky = kvalue2(nx, ny, dx, dy)

    # Step 2
    # Upward continuation operator for chosen height
    VerDerOp = numpy.power(numpy.absolute(numpy.sqrt(numpy.power(kx, 2) + numpy.power(ky, 2))), order);
    # Multiply Spectrum of the data by coninuation operator
    VerDerSpec = Spec * VerDerOp

    # Step 3
    # Inverse FFT
    VerDerGrid = numpy.real(numpy.fft.ifft2(numpy.fft.ifftshift(VerDerSpec)))

    # Trim the grid back to it's original dimensions
    VerDerGrid = VerDerGrid[0:Nrow, 0:Ncol]

    return VerDerGrid
