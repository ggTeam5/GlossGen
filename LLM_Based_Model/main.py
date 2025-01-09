import open_AI, prompts, sys

def printHelp():
    print("Please enter the following command:\tpython3 main.py <language> <trainFilePath> <testFilePath>")

# takes first fewshots from the training path
def fewshots (shots: int, trainFilepath: str):
    fewshots = ""
    with open (trainFilepath,"r") as f:
        lines = f.readlines()
        shot = 0
        for line in lines:
            if shot >= shots: break
            if line.startswith("\\m "):
                fewshots += "Transcription: " + line.strip("\\m ") + "\n"
            elif line.startswith("\\g "):
                fewshots += "Glosses: " + line.strip("\gm ") +"\n"
            elif line.startswith("\\l "):
                fewshots += "Translation: " + line.strip("\\l ") + "\n"
                fewshots += "\n"
                shot += 1
    return fewshots.rstrip()

# generate prompt from the test file
def generateMessages(testFilePath:str, language: str, fewshot_examples: str):
    transcription = ""
    translation = ""
    messages = []
    with open (f"{language}-output.txt", "w") as output:
        with open(testFilePath,"r") as testFile:
            testFileLines = testFile.readlines()
            for line in testFileLines:
                if line.startswith("\\m "):
                    transcription = line.strip("\\m ")
                elif line.startswith("\\l "):
                    translation = line.strip("\\l ")
                    prompt = prompts.generate_prompt(language,"English", fewshot_examples,transcription,translation)
                    response = open_AI.execute_prompt(prompt)
                    output.write(response + "\n")
                    print(response)
    return messages


if len(sys.argv) != 4:
    printHelp()

language = sys.argv[1]
trainFilePath = sys.argv[2]
testFilePath = sys.argv[3]

fewshot = fewshots(3,trainFilePath)
messages = generateMessages(testFilePath,language,fewshot_examples=fewshot)
print 


