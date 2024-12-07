
## Xigt + ODIN Schema and Validation

The contents of this directory form the validation schema with ODIN extensions.
The schema is in the [RelaxNG](http://relaxng.org) format. All `.rnc` files must
reside in the same directory, but only `odin-xigt.rnc` is used directly for
validation.

In order to validate a corpus, you will need a RelaxNG validator such as Jing:
(http://www.thaiopensource.com/relaxng/jing.html). The rest of this document
assumes you are using Jing for validation.

## Validating an ODIN Corpus

To validate a single corpus, do the following:

    jing -c odin-xigt.rnc CORPUS_PATH

where CORPUS_PATH is the filesystem path to a XigtXML corpus. For example:

    jing -c odin-xigt.rnc data/by-lang/xigt-enriched/deu.xml

You can also validate several corpora at once. For example:

    jing -c odin-xigt.rnc data/by-lang/xigt-enriched/*.xml

If validation succeeds, you will see no output, otherwise the errors will be
printed to the console.

## Structure-only Validation

Very basic schema validation can be performed with the "xigt-sructure.rnc"
schema, which only checks if the document is a structurally-sound Xigt corpus,
and doesn't do things like tier or item type checking.

    jing -c xigt-structure.rnc CORPUS_PATH

This validator could be useful if you extend the data and want to check that
a corpus is still valid without having to write your own schema.
