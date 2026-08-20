def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Cannot divide by zero"
    return x / y

print("Addition (10 + 5):", add(10, 5))
print("Subtraction (10 - 5):", subtract(10, 5))
print("Multiplication (10 * 5):", multiply(10, 5))
print("Division (10 / 5):", divide(10, 5))
print("Division by zero (10 / 0):", divide(10, 0))
