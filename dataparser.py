language = 'german'
for i in range(1, 5):
    file_path = f"language_articles/{language}{i}.txt"
    characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'á', 'é', 'í', 'ó', 'ú', 'ñ', 'à', 'è', 'ò', 'ù', 'ç', 'â', 'ê', 'î', 'ô', 'û', 'ä', 'ë', 'ï', 'ö', 'ü', 'å', 'ø', 'æ', 'č', 'ď', 'ě', 'ň', 'ř', 'š', 'ť', 'ů', 'ž', 'ý', 'ĺ', 'ľ', 'ŕ', 'ą', 'ć', 'ę', 'ł', 'ń', 'ś', 'ź', 'ż', 'ð', 'þ', 'ğ', 'ş', 'ı', 'ã', 'õ', 'ő', 'ű', 'ß', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Á', 'É', 'Í', 'Ñ', 'Ó', 'Ú', 'Ü', 'Â', 'À', 'Ä', 'Ç', 'È', 'Ê', 'Ë', 'Î', 'Ï', 'Ô', 'Ù', 'Û', 'Ü', 'Å', 'Ø', 'Æ', 'Č', 'Ď', 'Ě', 'Ň', 'Ř', 'Š', 'Ť', 'Ů', 'Ž', 'Ý', 'Ĺ', 'Ľ', 'Ŕ', 'Ą', 'Ę', 'Ł', 'Ń', 'Ś', 'Ź', 'Ż', 'Ć', 'Ö', 'Ð', 'Þ', 'Ğ', 'Ş', 'İ', 'Ã', 'Õ', 'Ő', 'Ű', 'ẞ']
    sentences = []

    try:

        with open(file_path, 'r', encoding='utf8') as file:

            #read in the file
            file_content = file.read()
            file_content = file_content.replace('\n', ' ')

            while len(file_content) > 0:
                
                #find index to splice next sentence
                splitIndex = 0
                periodIndex= len(file_content) - 1 
                exclamationIndex = len(file_content) - 1
                questionIndex = len(file_content) - 1
                if '.' in file_content:
                    periodIndex = file_content.find('.')
                    if file_content[periodIndex - 2] == ' ':
                        file_content = file_content.replace(file_content[periodIndex], '', 1)
                        continue
                if '!' in file_content:
                    exclamationIndex = file_content.find('!')
                if '?' in file_content:
                    questionIndex = file_content.find('?')
                splitIndex = min(periodIndex, exclamationIndex, questionIndex)

                #splice next sentence
                sentence = file_content[:splitIndex+1]
                file_content = file_content[splitIndex+2:]
                
                #delete any characters that do not appear in character list (keep spaces to parse words later)
                for char in sentence:
                    if char not in characters and char != ' ':
                        sentence = sentence.replace(char, '')

                #add sentence to sentences list
                sentences.append(sentence)
                print(sentence)

    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


    for s in sentences:
        chars = dict()
        arffRow = []
        words = s.split() # Split on spaces
        numWords = len(words)
        if numWords == 0:
            continue
        
        #initialize all character counts to 0
        for c in characters:
            chars[c] = 0
        
        #count occurrences of each character
        for word in words:
            for c in word:
                chars[c] += 1

        
        #add the percentage of each character occurrence to the arff row
        for c in characters:
            arffRow.append(chars[c] / len(s))
        
        #add word length average to the arff row
        arffRow.append(sum([len(word) for word in words]) / numWords)
        
        #add the number of words to the arff row
        arffRow.append(numWords)

        #add the current language being trained to the arff row
        arffRow.append(language.capitalize())
        
        #create string from arff row
        rowString = ''
        for val in arffRow:
            rowString += str(val) + ', '

        #write arff row to arff.txt file (we will convert this later to a real .arff file)
        with open('arff.txt', 'a') as file:
            # Write a new line of text to the file
            file.write(str(rowString[:-2]) + "\n")
