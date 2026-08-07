'''
Author: Angus Ashby
Student_ID: 33899940

Logic Overview:
The first condition rule is essentially taking a matched window of text and comparing the prefix to the sufffix for that window.
Where the suffix is of the pattern. This will present BaB as a window with the a being any text not appart of the prefix.
The second condition enforces Skips to be valid iff the following character of the suffix matches the mismatched text.
For any occurance of these conditions being met, the Left-Most occurance is used to ensure safe skips.

To make this table first we need to store for each possible search window what is the size of a prefix - suffix match and what is the character to the left,
and then additionally we point to another shorter prefix - suffix match with the char to the left continuing until |B| = 0. 
This is also an inverse of the LPS array of the KMP algorithm 

This will store a list with each index (k, char) where k is the index of the start of the prefix and char is the left char of the substring.
Then as we iterate over our txt and pattern we can do O(1) lookup based on txt[k] and txt[k-1]
'''

import sys

ALPHABET = (r""" % & ' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ """
            r""" A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ """
            r"""_ ` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~ """).split()
ALPHABET_OFFSET = ord('%')  # starts at %
ALPHABET_SIZE = len(ALPHABET)

# Helper function used to compute the LPS table 
def forward_prefix_function(pattern):
    """KMP lps on pat; lps[i] = length of longest proper border of pat[: i + 1]"""
    m = len(pattern)
    lps = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and pattern[i] != pattern[k]:
            k = lps[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        lps[i] = k
    return lps

# Map each charcter to its adjusted ord value 
def char_index(c):
    return ord(c) - ALPHABET_OFFSET

# The Algorithm
def Yet_another_pattern_matching_algorithm(txt: str, pat: str, run_log):
    """
    Right-to-left scan: compare pat[m-1]..pat[0] with txt[j+m-1]..txt[j] 

    Mismatch at pat[k]
    pat[k+1...k+m-p+1] == pat[p...m]. The character to the left of β in the pattern is pat[p-1];
    at the mismatch column, txt[j+k] must equal pat[p-1] 

    Shifty_table[row][c]: row = k+1, column c = ord(txt[j+k]); table stores ord(pat[p-1]) as c
    for the leftmost p > k+1 with matching β.
    """
    n = len(txt)
    m = len(pat)
    results = []
    print(txt)
    print(pat)

    alphabet = ALPHABET_SIZE
    forward_lps = forward_prefix_function(pat)

    # After a full match, we can align the next occurrence using the entire string as a border/search window
    shift_after_full_match = max(1, m - forward_lps[m - 1]) if m else 1
    p_after_full_match = (m - forward_lps[m - 1]) if m else 0               # p after a full match (m − border_len)

    # each row = k+1 after mismatch at pat[k]. Column c = ord(pat[p-1]) = ord(txt[j+k]) condition 2)
    Shifty_table = [[m+1] * alphabet for _ in range(m + 1)]

    # Compute KMP lps array on the reversed pattern
    # This gives us the border chains for every suffix of the pattern.
    rev_pat = "".join(reversed(pat))  # O(m) to reverse a pattern
    rev_lps = forward_prefix_function(rev_pat)

    # Populate the shift table 
    for r in range(m - 1, 0, -1):
        if r < m:
            # beta = pat[r:m], So its index in the reversed pattern is m - r - 1.
            idx = m - r - 1
                
            # Grab the length of the longest proper border of beta
            L = rev_lps[idx]
                
            # Traverse the border chain dynamically
            if L > 0:
                # O(|Σ|) copy — inherits all shifts from the border's already-computed row
                Shifty_table[r][:] = Shifty_table[m - L]

                # Overwrite with current border's shift, guaranteed smallest p
                p = m - L
                ckey = char_index(pat[p - 1])
                Shifty_table[r][ckey] = p
            else:
                # if no proper border, only the empty-border entry applies
                ckey = char_index(pat[m - 1])
                Shifty_table[r][ckey] = m

    j = n - m  # rightmost alignment start (0-based)
    galil_rule = 0

    while j >= 0:
        k = m - 1 - galil_rule              # pattern index of current comparison (right to left)
        match_index = j + k                 # aligned text index
        while match_index >= 0 and k >= 0 and txt[match_index] == pat[k]:
            k -= 1
            match_index -= 1

        if k == -1:  # entire pattern matched
            results.append(match_index + 1)
            shift = shift_after_full_match
            galil_rule = m - shift
            p_lookup = p_after_full_match
        else:
            c_idx = char_index(txt[j + k])
            row = k + 1
            p_lookup = Shifty_table[row][c_idx]
            
            if p_lookup == m + 1:
                # Character unmapped by Good Suffix rule. 
                # Shift by entire matched portion + 1.
                shift = m - k
                galil_rule = 0
            else:
                # Valid Good Suffix shift
                shift = p_lookup - k - 1
                galil_rule = max(0, m - 1 - k - shift)

        # Line: j, k+1 (0-based left end of α), p (right most β start index).
        run_log.append(f"{j} {k + 1} {p_lookup}")

        j -= shift

    return results

def main():
 
    text_file    = sys.argv[1]
    pattern_file = sys.argv[2]
 
    # WILL NOT WORK WITH UTF 8
    with open(text_file, 'r', encoding='utf-16') as f:
        txt = f.readline().rstrip('\n')

    with open(pattern_file, 'r', encoding='utf-16') as f:
        pat = f.readline().rstrip('\n')

 
    # Runs the algorithm 
    runlog_lines = []   
    matches_0based = Yet_another_pattern_matching_algorithm(txt, pat, runlog_lines)
 
    # Write matches to output_a1q1.txt (
    with open('output_a1q1.txt', 'w') as f:
        for pos in matches_0based:
            f.write(f"{pos + 1}\n")   # convert 0-based → 1-based
 
    # Write runlog to runlog_a1q1.txt 
    with open('runlog_a1q1.txt', 'w') as f:
        for line in runlog_lines:
            f.write(line + '\n')
 
 
if __name__ == '__main__':
    main()
 
