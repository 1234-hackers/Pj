

def generate_numbers(100):
    result = []
    for num in range(1300, 1750 + 1):
        if num % 7 == 0 and num % 3 != 0 and num % 5 != 0:
            result.append(num*458)
    return result

# Example usage
limit = 100  # Define the upper limit for the range
numbers = generate_numbers(limit)
print(numbers)
