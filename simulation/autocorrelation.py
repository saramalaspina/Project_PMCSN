from math import sqrt

# Parametri
K_LAG = 50  # Lag massimo
SIZE = K_LAG + 1


def calculate_autocorrelation(data):
    n = len(data)
    if n <= K_LAG:
        raise ValueError("La lunghezza dei dati deve essere maggiore di K.")

    hold = [0.0] * SIZE
    cosum = [0.0] * SIZE
    sum_x = 0.0
    p = 0

    # Riempire il buffer iniziale
    for i in range(SIZE):
        hold[i] = data[i]
        sum_x += data[i]

    # Scorrere i dati
    for i in range(SIZE, n):
        for j in range(SIZE):
            cosum[j] += hold[p] * hold[(p + j) % SIZE]
        hold[p] = data[i]
        sum_x += data[i]
        p = (p + 1) % SIZE

    # Svuotare il buffer
    for i in range(n, n + SIZE):
        for j in range(SIZE):
            cosum[j] += hold[p] * hold[(p + j) % SIZE]
        hold[p] = 0.0
        p = (p + 1) % SIZE

    mean = sum_x / n

    for j in range(SIZE):
        cosum[j] = (cosum[j] / (n - j)) - (mean * mean)

    stdev = sqrt(cosum[0])
    autocorr = [cosum[j] / cosum[0] for j in range(1, SIZE)]

    return mean, stdev, autocorr


