import numpy as np

def autocorrelation(samples, order):
    n = len(samples)
    r = np.zeros(order + 1)
    for i in range(order + 1):
        for j in range(n - i):
            r[i] += samples[j] * samples[j + i]
    return r

def levinson_durbin(r, order):
    a = np.zeros(order + 1)
    e = r[0]
    a[0] = 1
    a[1] = -r[1] / e
    e *= 1 - a[1] ** 2

    for i in range(2, order + 1):
        k = -np.sum(a[:i] * r[i:0:-1]) / e
        a[1:i] += k * a[i-1:0:-1]
        a[i] = k
        e *= 1 - k ** 2

    return a, e

def encode(samples, order):
    r = autocorrelation(samples, order)
    a, e = levinson_durbin(r, order)

    residuals = np.copy(samples)
    for i in range(order, len(samples)):
        pred = np.sum(a[1:] * samples[i-1:i-order-1:-1])
        residuals[i] -= int(pred)

    return residuals

def decode(residuals, order):
    samples = np.copy(residuals)
    for i in range(order, len(residuals)):
        pred = np.sum(a[1:] * samples[i-1:i-order-1:-1])
        samples[i] += int(pred)

    return samples
