import math
n = 1

def poisson(lam, r):
    return (math.exp(-lam)*lam**r)/math.factorial(r)


while True:
    print("------------------------------------")
    print(f"Iteration {n}")
    print("------------------------------------")
    lam = float(eval(input("Average: ")))
    r = int(input("Times? "))
    Iterate = bool(input("Iterate? "))
    Greater = bool(input("Greater than? "))
    if not Iterate:
        print(poisson(lam, r))
    else:
        total = [poisson(lam,x) for x in range(0,r+1)]
        summed_total = sum(total)
        if not Greater:
            print(summed_total)
        else:
            print(1-summed_total)
    n+=1
