import open_AI, prompts, sys, sampling, time

def printHelp():
    print("Please enter the following command:\tpython3 main.py <language> <shots> <trainFilePath> <testFilePath>")

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
    morpheme_line = ""
    messages = []
    with open (f"{language}-output.txt", "w") as output:
        with open(testFilePath,"r") as testFile:
            testFileLines = testFile.readlines()
            for line in testFileLines:
                if line.startswith("\\m "):
                    morpheme_line = line.strip("\\m ")
                elif line.startswith("\\t "):
                    transcription = line.strip("\\t ")
                elif line.startswith("\\l "):
                    translation = line.strip("\\l ")
                    time.sleep(1)
                    fewshot_examples_list = sampling.n_highest_wordRecall_sentences(n,trainFilePath,transcription)
                    fewshot_examples = fewshots(n, fewshot_examples_list)
                    prompt = prompts.generate_prompt(language,"English", fewshot_examples,transcription,translation,morpheme_line)
                    response = open_AI.execute_prompt(prompt)
                    print(response)
                    if (response.startswith("Glosses: ")):
                        output.write("\\t\n")
                        output.write("\\m\n")
                        output.write("\\g " + response.strip("Glosses: ").rstrip() + "\n")
                        output.write("\\l\n")
                        output.write("\n")
                        output.flush()
    return messages


if len(sys.argv) != 5:
    printHelp()

language = sys.argv[1]
shots = sys.argv[2]
shots = int(shots)
trainFilePath = sys.argv[3]
testFilePath = sys.argv[4]

messages = generateMessages(trainFilePath,shots,testFilePath,language)

printFinished(language)