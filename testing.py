def isAllVowels(word):
    result = False
    vowels = 'aeiou'
    if type(word) == str and word != "": #enter only if string with content
        word = word.lower()
        for letter in word:
            if letter in vowels:
                result = True
            else:
                result = False
                break # break out of loop, no need to keep checking
    return result

print "Expect True:"
print isAllVowels("EIEiO") #expect true
print isAllVowels("ooooOOaiuUU") #expect true

print "Expect False:"
print isAllVowels("oink") #expect false
print isAllVowels("foo") #expect false
print isAllVowels("") #expect false
print isAllVowels(None) #expect false