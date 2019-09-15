from collections import defaultdict
import itertools
def anagram_substring(str):
    substr_list = []
    ans = []
    is_present = defaultdict(list)
    for i in xrange(len(str)):
            for j in xrange(i+2, len(str)+1):
                substr_list.append(str[i:j])
            substr_list = list(set(substr_list))        
    for substr in substr_list:
        if is_present[''.join(sorted(substr))]:
                    for anagram_str in is_present[''.join(sorted(substr))]:
                        ans.append([anagram_str,substr])
        is_present[''.join(sorted(substr))].append(substr)  
    return ans

str = raw_input().strip()
print anagram_substring(str)
