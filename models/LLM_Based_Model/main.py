# import open_AI
import prompts, sys, sampling, time, gemini_api
import google.generativeai as genai

def printHelp():
    print("Please enter the following command:\tpython3 main.py <language> <shots> <trainFilePath> <testFilePath>")

def printFinished(language:str):
    print("done")

def fewshots (shots: int, exampleTupleList: list):
    fewshots = ""
    shot = 0
    for line in exampleTupleList:
        if shot >= shots: break
        if line.startswith("\m "):
            fewshots += line.rstrip() + "\n"
            # fewshots += line
        elif line.startswith("\g "):
            fewshots += line.rstrip() +"\n"
            # fewshots += line 
            fewshots += "\n"
            shot += 1
    return fewshots.rstrip()

# generate prompt from the test file
def generateMessages(trainFilePath: str, n: int, testFilePath: str, language: str):
    transcription = ""
    translation = ""
    morpheme_line = ""
    messages = []
    with open (f"{language}-{n}-shots-Gemini-WordRecall.txt", "w") as output:
        with open(testFilePath,"r") as testFile:
            testFileLines = testFile.readlines()
            for line in testFileLines:
                if line.startswith("\\t "):
                    transcription = line.replace("\\t ","").rstrip()
                elif line.startswith("\m "):
                    morpheme_line = line.replace("\\m ","").rstrip()
                # elif line.startswith("\l "):
                    # translation = line.replace("\\l ","").rstrip()
                    time.sleep(4) # 15 sentences processed per minute (resource limit)
                    fewshot_examples_list = sampling.n_highest_wordRecall_sentences(n,trainFilePath,transcription)
                    # fewshot_examples_list = sampling.n_highest_chrF_sentences(n,trainFilePath,transcription)
                    fewshot_examples = fewshots(n, fewshot_examples_list)
                    prompt = prompts.generate_prompt_modified(language,"English", fewshot_examples,transcription,translation,morpheme_line)
                    print(prompt)
                    # print(prompt)
                    response = gemini_api.ask_gemini(prompt)
                    print(response)
                    # prompt = prompts.generate_prompt(language,"English", fewshot_examples,transcription,translation,morpheme_line)
                    # response = open_AI.execute_prompt(prompt)

                    # if (response.startswith("Glosses: ")):
                    if (response.startswith("\g")):
                        output.write("\\t\n")
                        output.write("\\m\n")
                        response = response.rstrip()
                        output.write(response + "\n")
                        output.write("\\l\n")
                        output.write("\n")
                        output.flush()
    return messages

def gemini_fine_tuned(trainFilePath: str, n: int, testFilePath: str, language: str):
    transcription = ""
    translation = ""
    morpheme_line = ""
    model = genai.GenerativeModel(model_name="projects/457153199170/locations/us-east1/endpoints/7571971542632890368")
    messages = []
    with open (f"{language}-{n}-shots-Gemini-WordRecall.txt", "w") as output:
        with open(testFilePath,"r") as testFile:
            testFileLines = testFile.readlines()
            for line in testFileLines:
                if line.startswith("\\t "):
                    transcription = line.replace("\\t ","").rstrip()
                elif line.startswith("\m "):
                    morpheme_line = line.replace("\\m ","").rstrip()
                    time.sleep(4) # 15 sentences processed per minute (resource limit)
                    prompt = prompts.generate_prompt_fine_tuned(language,"English", "",transcription,translation,morpheme_line)
                    response = model.generate_content(prompt)
                    print(response.text) 

                    # if (response.startswith("Glosses: ")):
                    if (response.startswith("\g")):
                        output.write("\\t\n")
                        output.write("\\m\n")
                        response = response.rstrip()
                        output.write(response + "\n")
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

messages = gemini_fine_tuned(trainFilePath,shots,testFilePath,language)

printFinished(language)