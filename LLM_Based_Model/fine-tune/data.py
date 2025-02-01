import json
import sys

languageComplete = sys.argv[1] 
languageAbr = sys.argv[2]
with open(f"data/{languageComplete}/{languageAbr}-train-track2-uncovered","r") as f:
    with open(f"output/{languageAbr}-train-track2-uncovered.jsonl","w") as output:
        file_content = f.read().strip()
        blocks = file_content.split("\n\n")
        for block in blocks:
            lines = block.split("\n")
            morpheme_line,gloss_line = "",""
            for line in lines:
                if line.startswith("\\m"):
                    morpheme_line = line
                elif line.startswith("\\g"):
                    gloss_line = line
            if not morpheme_line or not gloss_line:
                exit ("morpheme or gloss line missing")
            prompt = f"""
Interlinear Glossing Text (IGT) line in {languageComplete} contains the lines:

\\m Morpheme line: Morpheme-segmented sentence
\\g Gloss line: Morpheme-by-morpheme glosses

### Formatting Details:
1. **Morpheme line**: The segmented into words by space. The Words are then segmented into morphemes using "-". Other characters are not used for morpheme segmentation.
2. **Gloss line**: Each morpheme is glossed with exactly one label using Leipzig Glossing Rules. 
   - Lexical morphemes in Morpheme line are glossed with a lexical label in English.
   - Functional morphemes are glossed with a functional label.
   - Unknown glosses are marked as "UNK".
3. **Alignment Rule**: Each gloss on the "\\g" line must directly correspond to the morpheme in the morpheme line it glosses, in the same order as the morpheme line. 

Provide the morpheme-by-morpheme glosses for this IGT line (start with "\\g") using Leipzip Glossing Rules:
{morpheme_line.strip()}"""

            output.write(json.dumps(
                {"contents": [
                    {
                        "role": "user",
                        "parts": [{
                            "text": prompt
                        }]
                    },
                    {
                        "role": "model",
                        "parts": [{
                            "text": gloss_line,
                        }]
                    }
                ]}
            ) + "\n")
        
    
