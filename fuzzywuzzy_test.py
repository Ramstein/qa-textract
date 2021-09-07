from fuzzywuzzy import fuzz, process

word_list =['fjadbbiu', 'jdbfag', 'nsfkubusi', 'bdjfh','gvhvh', 'nfd', 'njfd']

def get_matches(query, choices, limits=3):
    results = process.extract(query, choices, limit=limits)
    return results

print(get_matches('njfd', word_list, limits=5))