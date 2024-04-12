# def factorial_calculation(num):
#     factorial = 1
#     if num < 0:
#         raise ValueError("Factorial is not defined for negative numbers")
#     elif num == 0:
#         factorial = 1 
#     else:
#         for i in range(1, num):
#             factorial *= i
#         return factorial
    
# print(factorial_calculation(4))

from datetime import datetime

# Get the current timestamp as a Unix timestamp
current_unix_timestamp = datetime.now()
from datetime import datetime

# Get the current timestamp with milliseconds
current_timestamp = datetime.now()

# Remove milliseconds by setting microseconds to zero
current_timestamp_without_ms = current_timestamp.replace(microsecond=0)

print(current_timestamp_without_ms)


# print(current_timestamp)
