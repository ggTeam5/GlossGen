
            

def generate_prompt (language: str, metalang: str, fewshot_examples: str, transcription: str, translation: str, morpheme_line: str):
    return f"""You are an expert documentary linguist, specializing in {language}. You are working on a documentation project for {language} text, where you are creating annotated text corpora using the interlinear glossed text (IGT) and following the Leipzig glossing conventions.

    Specifically, you will be provided with a line of morphologically segmented text in {language} as well as a translation of the text into {metalang}, in the following format.

    Transcription: some sentence in {language} 
    Morpheme line: the morphological segmented transcription line (Morphemes are seperated by dashes and words are seperated by spaces.)
    Translation: translation of the transcription line in {metalang}

    You are to output the gloss line of IGT.
    You should gloss each stem/lexical morphemes with its translation in {metalang}, and each gloss gram/functional morphemes with a label indicating its function. Please output the gloss line in the following format:

    Glosses: the gloss line for the transcribed text 
    
    Glosses should use all caps lettering for functional morphemes and standard lettering for stem translations. Glosses for morphemes in a word should be separated by dashes, and words should be separated by spaces.

    Here are some complete glossed examples:
    {fewshot_examples}

    Please gloss the following example in {metalang}.

    Transcription: {transcription}
    Morpheme line: {morpheme_line}
    Translation: {translation}
    """


def generate_prompt_modified (language: str, metalang: str, fewshot_examples: str, transcription: str, translation: str, morpheme_line: str):
    return f"""Interlinear Glossing Text (IGT) line in {language} contains the lines:

\m Morpheme line: Morpheme-segmented sentence
\g Gloss line: Morpheme-by-morpheme glosses

### Formatting Details:
1. **Morpheme line**: The segmented into words by space. The Words are then segmented into morphemes using "-". Other characters are not used for morpheme segmentation.
2. **Gloss line**: Each morpheme is glossed with exactly one label using Leipzig Glossing Rules. 
   - Lexical morphemes in Morpheme line are glossed with a lexical label in English.
   - Functional morphemes are glossed with a functional label.
   - Unknown glosses are marked as "UNK".
3. **Alignment Rule**: Each gloss on the "\g" line must directly correspond to the morpheme in the morpheme line it glosses, in the same order as the morpheme line. 

### Example:

{fewshot_examples}

---

Provide the morpheme-by-morpheme glosses for this IGT line (start with "\g") using Leipzip Glossing Rules:

\m {morpheme_line}"""

def generate_prompt_fine_tuned (language: str, metalang: str, fewshot_examples: str, transcription: str, translation: str, morpheme_line: str):
    return f"""Interlinear Glossing Text (IGT) line in {language} contains the lines:

\m Morpheme line: Morpheme-segmented sentence
\g Gloss line: Morpheme-by-morpheme glosses

### Formatting Details:
1. **Morpheme line**: The segmented into words by space. The Words are then segmented into morphemes using "-". Other characters are not used for morpheme segmentation.
2. **Gloss line**: Each morpheme is glossed with exactly one label using Leipzig Glossing Rules. 
   - Lexical morphemes in Morpheme line are glossed with a lexical label in English.
   - Functional morphemes are glossed with a functional label.
   - Unknown glosses are marked as "UNK".
3. **Alignment Rule**: Each gloss on the "\g" line must directly correspond to the morpheme in the morpheme line it glosses, in the same order as the morpheme line. 

Provide the morpheme-by-morpheme glosses for this IGT line (start with "\g") using Leipzip Glossing Rules:

\m {morpheme_line}"""

   