# Automatic Interlinear Gloss Generation in Low-Resource Setting
In context of our Bachelor's Practical Course "Natural Language Processing", we compare three different models for automatic gloss generation of low-resource languages.

## Abstract
Interlinear glossing provides a description of
each morpheme in a sentence and is a crucial part of language documentation. We compare three different approaches of automatic
gloss generation, focusing on low-resource languages. The glossing line analyzes the grammatical structure as well as the meaning of a
sentence with respect to each morpheme. We compare a transformer-based, a CRF-based and a LLM-based model in terms of accuracy and output patterns to determine their strengths and weaknesses. We achieved considerable accuracy compared to Ginn et al. (2023), especially in Lezgi and Gitksan using Conditional Random Fields. In addition, we found that the transformer-based model improves with larger
training datasets.

## Data
The data we used originated from low-resource
language datasets provided by Ginn et al. (2023). 
Mainly, we used Gitksan, Lezgi and Tsez.

## Format
Interlinear Glossed Text (IGT) is a format used in language documentation. An IGT line (Figure 1) consists of a source sentence from a low-resource language "\t", its morphological segmentation "\m", the translation of that sentence "\l" into a matrix language (here, English)and the output "\g", which consists of the glosses for each source morpheme.

```
**Transcription** \t Way 'nithl wildiit.
**Morphemes**    \m way 'nit-hl wil-diit 
**Glossing**     \g so 3.III-CN LVB-3PL.II 
**Translation**  \t And that's what they did. 
```
**Figure 1**: Example IGT line for Gitksan language (Ginn et al., 2023).

## Models
The models used are based on transformers, Conditional Random Field (CRF) and the Large Language Model (LLM) Google Gemini (see: folder models). We executed the transformer-based trained models provided by Ginn (2023). Additionally, the transformer-based prediction was post-processed (for Lezgi language only), see: `models/transformers/`. We implemented the other two models (see: `models/`). The prediction of each model is provided in `predictions/`.

## Evaluation
We used the evaluation code provided by Ginn (2023).

## Paper
For more explanation, please refer to our paper (Link)