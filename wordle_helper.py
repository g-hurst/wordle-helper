import re

def output_matches(matches):
    print('Possible Words: ')
    for num, word in enumerate(matches):
        print('\t{:>3d}: {}'.format(num + 1, word))

def filter_guess(guess, key, words):
    not_in_word  = []  # letters not in the word
    in_word      = []  # letters in the word
    match        = ['.', '.', '.', '.', '.'] # letters in correct pos
    anti_matches = [] # expressions for letters in wrong pos
    
    # update the contained, not contained, match, anti-match
    for i, letter in enumerate(key):
        if letter == 'g':
            match[i] = guess[i]
        elif letter == 'y':
            anti_match  = ['.', '.', '.', '.', '.'] 
            anti_match[i] = guess[i]
            anti_matches.append(anti_match)
            in_word.append(guess[i])
        else:
            if guess.count(guess[i]) == 1:
                not_in_word.append(guess[i])
    
    
    # define the filter
    match_exp       = re.compile(''.join(match))
    anti_matchs_exp = [re.compile(''.join(exp)) for exp in anti_matches]
    def is_match(w): 
        # match the position of the letters
        yes = bool(match_exp.match(w))
        # filter out words with yellow letters in the wrong position
        if anti_match != ['.', '.', '.', '.', '.']:
            yes &= all([not bool(exp.match(w)) for exp in anti_matchs_exp])
        # filter words that only contain the yellow letters
        if len(in_word) > 0:
            yes &= all([(letter in w) for letter in in_word])
        # filter out words that contain grey letters
        if len(not_in_word) > 0:
            yes &= all([(letter not in w) for letter in not_in_word])
        return yes
    
    # filter the words based off the guess
    matches = [word for word in words if is_match(word)]
    return matches

prompt = \
'''
Welcome to the Wordle Helper

A brief description of how to use the tool:
guess:         the word you entered
wordle output: the response that wordle gave to your guess
    \033[92m green  letter: g \033[00m
    \033[93m yellow letter: y \033[00m
     black  letter: b
    
example:          \033[92mw\033[00mea\033[93mry\033[00m
guess is:         weary
wordle output is: gbbyy
'''

if __name__ == '__main__':
    # filter words to only 5 letters and alphabetical
    is_valid    = lambda w: (len(w) == 6) and w[:-1].isalpha()
    valid_words = [word.strip().lower() for word in open('words_all.txt', 'r') if is_valid(word)]
    
    n = 1
    print(prompt)
    # go through guesses until an answer has been reached
    while len(valid_words) > 1 or n == 6:
        guess = input('enter guess # {}     -> '.format(n)).lower()
        key   = input('enter wordle output -> '            ).lower()
        valid_words = filter_guess(guess, key, valid_words)
        output_matches(valid_words)
        n += 1
