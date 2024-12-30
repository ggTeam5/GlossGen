import string

def addPunctuationAtTheEnd(filePath):
    punctuation = string.punctuation + "»«()"
    with open(filePath,'r+',encoding='utf-8') as file:
        lines = file.readlines()

        for i in range(0,len(lines)):
            if lines[i].startswith('\\m') and (not lines[i].strip()[-1] in string.ascii_letters) and (lines[i].strip()[-1] != lines[i+1].strip()[-1]):
                addStr = ""
                for j in range(1,len(lines[i])):
                    if lines[i].strip()[-j] in punctuation and lines[i].strip()[-j] != lines[i+1].strip()[-1] or lines[i].strip()[-j] == " ":
                        addStr = lines[i][-j] + addStr
                    else : 
                        break
                lines[i+1] = lines[i+1].strip() + " " + addStr

        file.seek(0)
        for line in lines:
            line = line.strip() + "\n"
            file.write(line)

#TODO: Fehler bei Klammer