
            

def generate_prompt (language: str, metalang: str, fewshot_examples: str, transcription: str, translation: str):
    return f"""
    You are an expert documentary linguist, specializing in {language}. You are working on a documentation project for {language} text, where you are creating annotated text corpora using the interlinear glossed text (IGT) and following the Leipzig glossing conventions.

    Specifically, you will be provided with a line of morphologically segmented text in {language} as well as a translation of the text into {metalang}, in the following format.
    Morphemes are seperated by dashes and words are seperated by spaces.

    Transcription: some morphological segmented text in {language} 
    Translation: translation of the transcription line in {metalang}

    You are to output the gloss line of IGT.
    You should gloss each stem/lexical morphemes with its translation in {metalang}, and each gloss gram/functional morphemes with a label indicating its function. Please output the gloss line in the following format:

    Glosses: the gloss line for the transcribed text 

    Glosses should use all caps lettering for functional morphemes and standard lettering for stem translations. Glosses for morphemes in a word should be separated by dashes, and words should be separated by spaces.

    Here are some complete glossed examples:
    {fewshot_examples}

    Please gloss the following example in {metalang}.

    Transcription: {transcription}
    Translation: {translation}
    """
# TODO: change format so that it suits this of the baseline model