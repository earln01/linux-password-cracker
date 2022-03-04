'''
Earl Navarro ewn7jtt

Description:
This tool takes 2 command line arguments, a file path to a shadow file and a file path to a word list, and tries to crack the user passwords in the shadow file
by matching the hash of the word to the hash stored in the shadow file. It also takes an optional parameter to mangle the word list to check extra potential 
passwords derived from the words in the wordlist. It tries changing the capitalization of the first letter, and amending special characters to the end of the word,
as well as both techiniques together.

Dependencies:
Python 3.9.10
python crypt module
python sys module

Execution:
python3 crack.py [SHADOW PATH] [WORDLIST PATH] -m(optional)
    SHADOW PATH = file path to shadow file to crack
    WORDLIST PATH = file path to list of words to try 
    -m = use mangling techniques if included
'''

import crypt
import sys

class User:
    algorithms = {'1':'MD5', '2a': 'Blowfish', '5':'SHA-256', '6':'SHA-512'}
    def __init__(self, userName: str, entry:str):
        self.userName = userName
        self.entry = entry
        self._setIdCryptSalt()
        self.algorithm = self.algorithms[self.id]
        self.broken = ""

    def __repr__(self):
        formatted = f'uname: {self.userName}\nalg: {self.algorithm}\npass: {self.broken}\n'
        divider = '\n------------------------------------------------------------\n'
        return(formatted+divider)

    def _setIdCryptSalt(self):
        entry = self.entry[1:].split('$')
        self.id, self.salt = entry[0], entry[1]
        self.cryptSalt = f'${self.id}${self.salt}$'

    def checkHash(self, word):
        cryptWord= crypt.crypt(word, self.cryptSalt)
        if (self.entry == cryptWord):
            self.broken = word
            print(self)
            return True
        return False


def getUserList(passPath):
    userList = []
    with open(passPath, 'r') as hashes:
        for line in hashes.readlines():
            line = line.strip().replace("/n", "").split(":")
            if not line[1] in ('*', 'x', '!'):
                userList.append(User(line[0], line[1]))
    return userList

    

def getMangleList(word):
    mangleList = {word}
    if word[0].isalpha():
        if word[0].islower():
            changedWord = word.capitalize()
        elif word[0].isupper():
            changedWord = word[0].lower() + word[1:]
        mangleList.add(changedWord)
    for i in range(33,48):
        mangleList.add(word + chr(i))
        if 'changedWord' in locals():
            mangleList.add(changedWord + chr(i))
    return mangleList


def checkWord(word, userList, mangle):
    mangledList = getMangleList(word) if mangle else {word}
    for word in mangledList:
        for user in userList:
            if user.checkHash(word):
                userList.remove(user)



def crackPass(wordPath, passPath, mangle):
    userList = getUserList(passPath)
    with open(wordPath, 'r') as wordList:
        for word in wordList.readlines():
            word = word.strip().strip('\n')
            if word != '':
                checkWord(word, userList, mangle)


def main():
    mangle = False

    if len(sys.argv) < 3:
        print("Not enough arguments entered")
        exit()

    for arg in sys.argv[1:]:
        if arg == "-m":
            mangle = True
            sys.argv.remove(arg)
            break

    passPath = sys.argv[1]
    wordPath = sys.argv[2]
    crackPass(wordPath, passPath, mangle)


if __name__ == '__main__':
    main()
    
