import numpy


def gridpeak(t, X=None):
    # GP = GRIDPEAK(...)
    #   gp = gridpeak(t)    return gridpeaks based on Blakely
    #                       and Simpson method
    #   gp = gridpeak(t,X)  optionally remove peak values scoring less than X,
    #   where X can be between 1 and 4.

    print 'shape ', t.shape
    m, n = t.shape
    p = 1

    gp = numpy.zeros((m, n))
    for i in numpy.arange(p, m - p):
        for j in numpy.arange(p, n - p):
            data = numpy.zeros(4)
            data[0] = t[i - p, j] < t[i, j] and t[i, j] > t[i + p, j]
            data[1] = t[i, j - p] < t[i, j] and t[i, j] > t[i, j + p]
            data[2] = t[i + p, j - p] < t[i, j] and t[i, j] > t[i - p, j + p]
            data[3] = t[i - p, j - p] < t[i, j] and t[i, j] > t[i + p, j + p]
            gp[i, j] = numpy.sum(data)

    if X:
        gp[gp < X] = numpy.nan

    gp = gp / gp

    return gp
