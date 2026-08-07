
import sys

''' 
    Author: Angus Ashby
    Student_ID: 33899940

    The following code is to compute the BWT array for any given string,
    The time complexity is in n^2 * log(n) as for each suffix in the string we sort it.
                There is n suffixes and sorting takes nlog(n) Time
 '''

def generate_bwt(text: str) -> str:
    """
    Constructs the Burrows-Wheeler Transform of a given text by computing 
    the suffix array via explicit sorting of all suffixes.
    """
    # terminal character
    text += '$'
        
    n = len(text)
    suffixes = [(text[i:], i) for i in range(n)]
    
    suffixes.sort(key=lambda item: item[0])
    suffix_array = [item[1] for item in suffixes]
    bwt = []
    for sa_idx in suffix_array:
        if sa_idx == 0:
            bwt.append(text[n - 1])
        else:
            bwt.append(text[sa_idx - 1])
            
    return "".join(bwt)


def build_occ(bwt):
    """
    Constructs the character totals and No of Occruances table.
    Time: O(n * size of alpabet) 
    Space: O(n * size of alphabet)  
    """
    n = len(bwt)
    
    # Compute total occurrences of each character
    rank = {}
    for ch in bwt:
        rank[ch] = rank.get(ch, 0) + 1
        
    # No_of_occ[c][i] stores the occurrences of character 'c' in bwt[0...i]
    No_of_occ = {ch: [0] * n for ch in rank}
    running = {ch: 0 for ch in rank}
    
    # Populate the No_of_occurance table in O(N * |Alphabet|) time
    for i, ch in enumerate(bwt):
        running[ch] += 1
        for unique_ch in rank:
            No_of_occ[unique_ch][i] = running[unique_ch]
            
    return rank, No_of_occ

def build_first_occurrence(tots):
    """
    Constructs the First Occurrence (C) table from character totals.
    Time complexity: O(N log n) Space O(N * size of alphabet)
    """
    first_occurrence = {}
    current_index = 0
    
    # Characters must be sorted lexicographically
    for ch in sorted(tots.keys()):
        first_occurrence[ch] = current_index
        current_index += tots[ch]
        
    return first_occurrence

def compute_suffix_array(bwt, no_of_occ, rank):
    """ 
    Time complexity: O(N), Space O(N)
    """
    n = len(bwt)
    SA = [0] * n
    # The terminal character '$' is always at row 0 in the first column
    curr_row = 0
    
    # Traverse backwards through the original text indices
    for text_pos in range(n - 1, -1, -1):
        SA[curr_row] = text_pos
        char = bwt[curr_row]
        
        # LF Mapping: Find where 'char' sits in the first column.
        # - rank[char] gives the starting block of 'char'
        # - no_of_occ[char][curr_row] gives the count of 'char' up to curr_row
        # - Subtract 1 to convert the count to a 0-based offset
        curr_row = rank[char] + no_of_occ[char][curr_row] - 1
        
    return SA

# Helper function/modulised version of the BWT search
# sp, ep mapping such that it can be repeatably called in the search function.

def backward_step(char, sp, ep, rank, No_of_occ):
    if char not in No_of_occ:
        return None
    if sp > 0:
       count_before_sp = No_of_occ[char][sp - 1] 
    else:
      count_before_sp = 0
       
    count_up_to_ep = No_of_occ[char][ep]
    new_sp = rank[char] + count_before_sp
    new_ep = rank[char] + count_up_to_ep - 1

    if new_sp > new_ep: # this means there is no valid substring for our pat 
        return None

    return new_sp, new_ep

def search_function(Bwt, pat):
    '''
    Methodolgy is written in the report 
    '''
    n = len(Bwt)
    m = len(pat)

    # Helper functions to generate No of occurances table, rank table, suffix array and the alphabet
    totals, No_of_occ = build_occ(Bwt)
    rank = build_first_occurrence(totals)
    SA = compute_suffix_array(Bwt, No_of_occ, rank)
    alphabet = [c for c in sorted(rank.keys()) if c != '$']

    # zero_edit: set containing (sp,ep) intervals matched with 0 match distance
    # one_edit:  set containing (sp,ep) intervals matched with 1 match distance
    zero_edit = {(0, n - 1)}   # sp = 0, ep = n-1
    one_edit  = set()
    pending = {} # Transposition dict to store future possible match_distance 1 BWT searchs

    for i in range(m - 1, -1, -1):
        # Transposition results computed two steps ago can be evaluated when the pat[i] index is the same
        # since transposition at step i+2 consumed pat[i+2] and pat[i+1], meaning the next character to match is pat[i]. 
        one_edit |= pending.pop(i, set())

        # Insertion: An insertion means match a txt char without touching i
        insert = set()
        for (sp, ep) in zero_edit:
            for c in alphabet:
                result = backward_step(c, sp, ep, rank, No_of_occ)
                if result:
                    insert.add(result)
        one_edit |= insert # Add the insertion result set O(size of alphabet)

        new_zero = set() 
        new_one  = set()
        # Match pat[i] against all currently stored intervals 
        for (sp, ep) in zero_edit:
            result = backward_step(pat[i], sp, ep, rank, No_of_occ)
            if result:
                new_zero.add(result)    

        for (sp, ep) in one_edit:       
            result = backward_step(pat[i], sp, ep, rank, No_of_occ)
            if result:
                new_one.add(result)   

        for (sp, ep) in zero_edit: # Then We explore match_distance 1 possibilites
            new_one.add((sp, ep)) # For deletion we can Skip pat[i] and keep sp, ep unchanged. 

            for c in alphabet: # For substitution test matching all alphabet chars
                if c == pat[i]:
                    continue
                result = backward_step(c, sp, ep, rank, No_of_occ)
                if result:
                    new_one.add(result)

            # for transposition we match pat[i-1] first (right), then pat[i] this is ahead of the current pat[i], the result belongs at i-2
            if i > 0 and pat[i] != pat[i - 1]:
                left = backward_step(pat[i - 1], sp, ep, rank, No_of_occ)
                if left:
                    right = backward_step(pat[i], left[0], left[1], rank, No_of_occ)
                    if right:
                        if (i - 2) in pending: # i-2 might mean the transposition elipsed the entire pattern
                            pending[i - 2].add(right)
                        else:
                            pending[i - 2] = {right}

        # Overwrite with matches
        zero_edit = new_zero
        one_edit  = new_one

    index_results = [-1] * (n + 2) # To maintain a sorted list without sorting to reduce complexity make "an array" with each index equating to an index in the text

    def record(sp, ep, matched_distance):
        for idx in range(sp, ep + 1):
            pos = SA[idx] + 1  # 1-based text position
            curr = index_results[pos]
            if curr == -1 or matched_distance < curr:
                index_results[pos] = matched_distance
            # Every exact match implies a distance-1 match at pos-1 
            # (As long as we are not at the start of the txt)
            if matched_distance == 0 and pos > 1:
                prev = index_results[pos - 1]
                if prev == -1 or 1 < prev:
                    index_results[pos - 1] = 1

    # Add all resulting intervals
    for (sp, ep) in zero_edit:
        record(sp, ep, 0)
    for (sp, ep) in one_edit:
        record(sp, ep, 1)
    for (sp, ep) in pending.get(-1, set()):
        record(sp, ep, 1)

    # sort resulst without sorting :D
    sorted_results = []
    for i in range(1, n+1):
        if index_results[i] != -1:
            sorted_results.append((i, index_results[i]))

    return sorted_results


def main():

    text_filename = sys.argv[1]
    pattern_filename = sys.argv[2]

    # strip whitespace/newline
    with open(text_filename, 'r') as f:
        text = f.read().rstrip('\n') 

    with open(pattern_filename, 'r') as f:
        pat = f.read().rstrip('\n')


    bwt_arr = generate_bwt(text)

    results = search_function(bwt_arr, pat)

    with open('output_a1q2.txt', 'w') as f:
        for pos, dist in results:
            f.write(f"{pos} {dist}\n")
                    

if __name__ == "__main__":
    main()
