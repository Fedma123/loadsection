
def dumb_multiplication(a, b):
    # SECTION dumb BEGIN
    result = 0
    for i in range(b):
        result += a
    # SECTION dumb END
    
    return result
    

def multiplication(a, b):
    # SECTION normal BEGIN
    return a * b
    # SECTION normal END

if __name__ == "__main__":
    # SECTION init BEGIN
    a = 5
    b = 7
    # SECTION init END
    
    result = dumb_multiplication(a, b)
    print(result)