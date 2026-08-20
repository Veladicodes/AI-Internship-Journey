def reverse_string(s):
    return s[::-1]

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def count_vowels(s):
    count = 0
    for char in s.lower():
        if char in "aeiou":
            count += 1
    return count

def find_largest(lst):
    if not lst:
        return None
    largest = lst[0]
    for num in lst:
        if num > largest:
            largest = num
    return largest

print("Reversed 'hello':", reverse_string("hello"))
print("Is 11 prime?:", is_prime(11))
print("Is 15 prime?:", is_prime(15))
print("Factorial of 5:", factorial(5))
print("Vowels in 'python programming':", count_vowels("python programming"))
print("Largest in [4, 7, 1, 9, 3]:", find_largest([4, 7, 1, 9, 3]))
