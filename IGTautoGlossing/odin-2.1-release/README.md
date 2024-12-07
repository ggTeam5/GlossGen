
# ODIN 2.1

<!--
NOTE: this is a MarkDown document. It is plain text, but is best viewed
      in a MarkDown viewer (see: https://en.wikipedia.org/wiki/Markdown).
-->

ODIN, the Online Database of INterlinear glossed text, is a collection of
IGT extracted from linguistics documents on the web.

This release encodes the data into the
[Xigt](http://depts.washington.edu/uwcl/xigt/)
format, which provides several benefits:

  * The XML data format is more explicit than plain text, so it's more
    interpretable
  * The Xigt data model is extensible, so additional layers of annotation can
    be provided on top of the existing data
  * The Xigt project provides tools for querying and processing the data,
    as well as an API for working with the data programmatically

In addition, this release improves the original ODIN text data in some ways:

  * The original sentences have been cleaned and noise/errors from the
    PDF extraction process have been reduced
  * Basic alignments between the language, gloss, and translation lines
    have been created where possible
  * Enrichments to the data (POS tags, phrase structure, bilingual alignments,
    and dependencies) are provided, where possible, via the
    [INTENT project](http://intent-project.info/)

This release contains:

  * 2026 source documents
  * 158,007 IGTs
  * 1496 languages by ISO-639-3 code
    - 157,363 IGTs (1494 languages) with an identified code
    - 637 IGTs for language varieties without a code (given code `???`)
    - 7 IGTs for artificial languages (given code `*xxx*`)

## License and Attribution

The ODIN data are released under the [Creative Commons Attribution 4.0
International License](http://creativecommons.org/licenses/by/4.0/)), requiring
only attribution. Users may fulfill the attribution requirement by linking to
the ODIN website, and/or by citing the ODIN publications.

When using individual IGT, such as in a linguistics paper, it is good practice
to also cite the original source. Each IGT in ODIN has a `doc-id` attribute,
which is an identifier for the document the IGT was extracted from. This
identifier can be looked up in the `citations.txt` file to find information
about the source document, such as the title, year, and author.

## Corpus Contents

The ODIN data exist under the `data/` subdirectory. There are six compressed
archives containing different levels of annotation and different views of the
data, as described below. The files are `tar` archives with `bzip` compression.
On machines with the `tar` command-line program, the files can be extracted with
the following commands (e.g., using `data/by-doc-id/txt.tbz2`):

    cd data/by-doc-id/
    tar xf txt.tbz2

Alternatively, or on Windows system, a program such as
[7Zip](http://www.7-zip.org/) can extract the files.

There are three levels of annotation: (1) the original text data, (2) the data
imported into the Xigt XML format, and (3) the Xigt XML data augmented with
inferred and enriched annotation tiers. There are then two views on the data,
where the views group IGTs into corpus files by (a) the document ID or (b) the
subject language (as determined by their assigned ISO-639-3 code). There are
thus two subdirectories under `data/`, `data/by-doc-id/` and `data/by-lang/`,
and a total of six corpus collections:

1. `data/by-doc-id/`
  * `txt`
  * `xigt`
  * `xigt-enriched`
2. `data/by-lang/`
  * `txt`
  * `xigt`
  * `xigt-enriched`

The corresponding collections across the views (e.g., `by-doc-id/txt` and
`by-lang/txt`) will contain the same data. The only difference is how the IGTs
are grouped into corpus files (by document ID or by ISO-639-3 code).

Under each view's subdirectory (`by-doc-id/` or `by-lang/`) there is a
`languages.txt` file that lists, for each file, the languages used and the
number of IGTs for those languages. For example, the entry for the `ben` corpora
(`ben.txt` or `ben.xml`) under the `by-lang/` view shows the following:

    ben:
    231    Bangla (ben)
    117    Bengali (ben)
    4      Bengalisch (ben)

In each Xigt collection (`xigt` or `xigt-enriched`), there is a `summary.txt`
file that gives an overview of the number of items, tier types, etc. found in
each corpus file. The abbreviated entry for the same `ben` corpora is as
follows:

    ben.xml:
       352   IGTs
        36   source documents
         3   languages (by name)
         1   languages (by ISO-693-3 language code)
       127   IGTs with tiers: odin, odin, odin, phrases, translations, words, words, glosses, glosses, morphemes, pos, pos, bilingual-alignments, phrase-structure, dependencies
        89   IGTs with tiers: odin, odin, odin, phrases, translations, words, words, glosses, glosses, morphemes, pos, pos, pos, bilingual-alignments, phrase-structure, phrase-structure, dependencies, dependencies
        36   IGTs with tiers: odin, odin, odin, phrases, words, glosses, glosses, morphemes, pos
       ...   ...
      1056   tiers of type: odin
       632   tiers of type: pos
       606   tiers of type: glosses
       ...   ...

The "IGTs with tiers" lines show how many IGTs exist with the specified
collection of tier types. The "tiers of type" lines show how many tiers of the
specified type exist across all IGTs in the corpus. Differences across IGTs are
due to the available data in the original representation and how well we were
able to infer and enrich the data (we are able to enrich clean data better than
noisy data). The accompanying `enrichment_flowchart.pdf` file illustrates this
process in more detail. Also note that some tier types are repeated (e.g.,
`odin`, `words`, etc.). For the `odin` tiers, these are for the `raw`,
`cleaned`, and `normalized` versions of the text data (a `state` attribute on
those tiers is used to indicate the level of cleaning done). For the other tier
types, it either represents an alternative analysis (as in `dependencies` or
`pos`), or when the same tier type is used on different data sources (as in
`words` for the language line or the translation line).

## Xigt format

The [Xigt project](http://depts.washington.edu/uwcl/xigt/) has documentation
about the structure of the XML, but we provide a brief explanation here.

The data contains only four levels of nesting: the root element,
`<xigt-corpus>`, contains a list of `<igt>` elements, which contain `<tier>`
elements, which in turn contain `<item>` elements. The actual IGT data is
expressed in the `<item>` elements, and `<tier>` elements group `<item>`
elements of the same type (e.g. all glosses). In addition, `<metadata>`
elements may appear at the `<xigt-corpus>`, `<igt>`, or `<tier>` levels,
before the other kinds of child elements.

Here's a selected (and simplified) example:

```xml
<xigt-corpus xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:ns1="http://www.language-archives.org/OLAC/1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <igt id="igt75841" doc-id="1591">
     <metadata>
       <meta id="meta1">
         <dc:subject ns1:code="cmn" xsi:type="olac:language">Mandarin</dc:subject>
         <dc:language ns1:code="en" xsi:type="olac:language">English</dc:language>
       </meta>
     </metadata>
     <tier id="p" type="phrases">
       <item id="p1">hua kaishi hong le</item>
     </tier>
     <tier id="w" type="words" segmentation="p">
       <item id="w1" segmentation="p1[0:3]"/>
       <item id="w2" segmentation="p1[4:10]"/>
       <item id="w3" segmentation="p1[11:15]"/>
       <item id="w4" segmentation="p1[16:18]"/>
     </tier>
     <tier id="g" type="glosses" alignment="w">
       <item id="g1" alignment="w1">flower</item>
       <item id="g1" alignment="w1">begin</item>
       <item id="g1" alignment="w1">red</item>
       <item id="g1" alignment="w1">Prc</item>
     </tier>
    <tier id="t" type="translations" alignment="p">
      <item id="t1" alignment="p1">Flowers started to turn red.</item>
    </tier>
  </igt>
</xigt-corpus>
```
> (This example is taken from Wu, Jiun-Shiung. *Modeling temporal progression
> in Mandarin: aspect markers and temporal relations*. Diss. Tex. Austin, 2008.)

As the Xigt-encoded ODIN corpus is automatically created from IGTs extracted
from PDFs, we try to avoid losing information during encoding by using a
pseudo-standoff annotation on the original extracted text. For instance, the
`phrases` tier in the above example would select its content from an `odin` text
tier like this:

```xml
...
  <tier id="n" type="odin" state="normalized" alignment="c">
    <item id="n1" line="2119" tag="L" alignment="c1">hua   kaishi hong    le</item>
    ...
  </tier>
  <tier id="p" type="phrases" content="n">
    <item id="p1" content="n1"/>
  </tier>
...
```

Note that this `odin` tier has its `state` attribute set to `normalized`. The
original text would be in a first `odin` tier with `state` set to `raw` (not
shown). Some corruptions of the text extracted from the PDF can be automatically
recovered, so a second `odin` tier with `state` set to `cleaned` (also not
shown) follows the `raw` tier. The text form of an IGT often have portions that
are not part of the language, gloss, or translation lines, such as item numbers,
author or language names, or extraneous whitespace. The normalized tier
attempts to remove these portions. Finally, the inferred structure tiers
(`phrases`, `glosses`, etc.) annotate the data in the normalized tier, and the
enrichment tiers (`pos`, `phrase-structure`, etc.) annotate these structure
tiers.

## Acknowledgments

Work on ODIN (and related projects) has been funded in part by the following
grants:

* National Science Foundation Grant Nos. BCS-1160274 and BCS-0748919. Any
  opinions, findings, and conclusions or recommendations expressed in this
  material are those of the author(s) and do not necessarily reflect the views
  of the National Science Foundation.
* Singapore Ministry of Education Tier 2 grant (grant number MOE2013-T2-1-016)

