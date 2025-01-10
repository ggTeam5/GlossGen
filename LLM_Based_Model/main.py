import open_AI, prompts, sys, sampling

def printHelp():
    print("Please enter the following command:\tpython3 main.py <language> <trainFilePath> <testFilePath>")

def printFinished(language:str):
    print("output path: ./"+language+"-output.txt")

def fewshots (shots: int, exampleTupleList: list):
    fewshots = ""
    shot = 0
    for line in exampleTupleList:
        if shot >= shots: break
        if line.startswith("\\m "):
            fewshots += "Transcription: " + line.strip("\\m ") + "\n"
        elif line.startswith("\\g "):
            fewshots += "Glosses: " + line.strip("\\g ") +"\n"
        elif line.startswith("\\l "):
            fewshots += "Translation: " + line.strip("\\l ") + "\n"
            fewshots += "\n"
            shot += 1
    return fewshots.rstrip()

# generate prompt from the test file
def generateMessages(trainFilePath: str, n: int, testFilePath: str, language: str):
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
                    fewshot_examples_list = sampling.n_highest_wordRecall_sentences(n,trainFilePath,transcription)
                    fewshot_examples = fewshots(n, fewshot_examples_list)
                    prompt = prompts.generate_prompt(language,"English", fewshot_examples,transcription,translation)
                    response = open_AI.execute_prompt(prompt)
                    if (response.startswith("Glosses: ")):
                        output.write("\\t\n")
                        output.write("\\m\n")
                        output.write("\\g " + response.strip("Glosses: ").rstrip() + "\n")
                        output.write("\\l\n")
                        output.write("\n")
    return messages


if len(sys.argv) != 4:
    printHelp()

language = sys.argv[1]
trainFilePath = sys.argv[2]
testFilePath = sys.argv[3]

messages = generateMessages(trainFilePath,3,testFilePath,language)

printFinished(language)