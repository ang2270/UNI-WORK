import sys
import random


# Read the first line of the text file and remove any trailing newlines
with open(sys.argv[1], 'r') as f:
    txt = f.readline().strip()
# Read the first line of the pattern file and remove any trailing newlines
with open(sys.argv[2], 'r') as f:
    pat = f.readline().strip()


# Modular function 
def modularExponentation(a,b,n):            # evaluates a^b mod n
    binary = bin(b)[2:]                         # get the binary
    lastj = len(binary) - 1
    LSB = binary[lastj]
    # Base case
    current = a % n                     # a mod n with no power (BASE)

    if LSB == '1':               # if the Least significant bit is 0, we know we can start at 1
        result = current
    else:
        result = 1
    # Iterate over remaining bits in the binary rep in reverse
    for bit in "".join(reversed(binary[:-1])):
        current = (current * current) % n               # Taking a^2^i 
        if bit == '1':
            # update result
            result = (result * current) % n             # Update result 'Column' with prev * new mod n, start at 1 *from above
    return result

# Miller-Rabin Primality test function
def primality_test(n, k):
    if n == 2 or n == 3:
        return "probably_prime"
    s = 0
    t = n-1
    while ((t % 2) == 0):
        s = s+1
        t = t//2                                         # integer floor to avoid float errors :[]
    for _ in range(k):
        candidate = random.randint(2, n-2)               # in 2.. n-2
        x_0 = modularExponentation(candidate,t,n)        # x = a^t (mod n)
        if (x_0 == 1):                                   # Probably prime // Case 4
            continue
        else:                                            # if not, we square x up to s-1 times looking for x to equal n-1
            x_prev = x_0
            x_i = x_0
            x_s = 0
            for _ in range(1, s+1):  
                x_prev = x_i              
                x_i = (x_prev * x_prev) % n              # x = x^2 (mod n)
                if x_i == 1:                             # Base Passes check previous
                    if x_prev != n-1:                    # Case 2
                        return "Composite"               
                    else:
                        x_s = 1                          # Case 3 (... -1, 1,)
                        break 
        if x_s != 1:
            return "Composite"
    return "probably_prime" 


# r function 
def r(text, p):
    index = []
    Z = 0
    # Take the ord/index of each character
    for c in text:
        index.append(ord(c))
    # Beta = 128 by default
    for i in range(len(index)):
        power_term = modularExponentation(Beta, len(index)-1-i, p)
        Z = (Z + index[i] * power_term) % p       # from formula
    return Z 

# Innitilastion of variables / values:

ALPHABET = [chr(i) for i in range(128)]
ALPHABET_SIZE = 128  # |Σ| = β = 128

Beta = ALPHABET_SIZE
m = len(pat)
n = len(txt)

# Test random t−bit candidates until prime p is found:

t = max(32, m)
while True:
    candidate = random.randint(2**(t-1), (2**t - 1))
    if primality_test(candidate, 32) == 'probably_prime':
        p = candidate
        break
pattern_r = r(pat, p)
Z_factor = modularExponentation(Beta,m-1,p)            # evaluates a^b mod n

found_positions = []
# Algorithm / Pattern matcher
txt_j_r = r(txt[0:m],p)                                 # First window of text // pattern
for j in range(0, n-m+1):
    if pattern_r == txt_j_r:
        if pat == txt[j:j+m]:
            found_positions.append(str(j+1))                 # 1-based run log
    if j < n - m:                                       # Not at the last window    i.e still txt to go
        # index of j + m - 2 character
        leaving_char = ord(txt[j])       
        
        # index of j + m - 1 character
        entering_char = ord(txt[j+m])    
        
        # O(1) update // optimisation
        txt_j_r = ((txt_j_r - leaving_char * Z_factor) * Beta + entering_char) % p

    
# Write out the results separated by newlines
with open("output_a2q2.txt", 'w') as out_file:
    out_file.write("\n".join(found_positions) + "\n")
    
