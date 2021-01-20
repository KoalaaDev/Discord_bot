from numpy.random import normal

while True:
    mean = float(input("Mean: "))
    standard_dev = float((input("Variance: ")))**0.5
    print(normal(mean,standard_dev))
