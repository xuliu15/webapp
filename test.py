def factorial_calculation(num):
    factorial = 1
    if num < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif num == 0:
        factorial = 1 
    else:
        for i in range(1, num):
            factorial *= i
        return factorial
    
print(factorial_calculation(4))