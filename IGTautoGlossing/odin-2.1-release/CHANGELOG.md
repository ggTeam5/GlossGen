# Change Log

## [v2.1] - 2016.03.14

This release fixes the bugs from v2.0 and introduces enriched tiers
from the [INTENT](http://intent-project.info/) project.

### Added

Where possible, the following inferred tiers are added:

* phrases
* words
* morphemes
* glosses
* translations

And, where possible, the following enriched tiers are added:

* pos
* bilingual-alignment
* phrase-structure
* dependencies

Also, the `odin-xigt.rnc` RelaxNG schema is included under the `schema/`
directory for validating the XigtXML files.

### Changed

* IDs:
  - `iX` style IDs (e.g., `i2`) for `<igt>` elements are now `igtD-X` where `D`
    is the doc-id (document ID) and X is the IGT number for that document (e.g.,
    `igt1260-7`)
  - Some `<igt>` elements had `.txt` at the end of the ID, which came from
    errors in the original text corpus. This suffix has been removed
    from both the text corpus and the IDs in the XML. (also see "Filenames"
    below)
  - All IDs with integers now begin from 1 instead of 0
  - IDs on `<meta>` are now of the form `metaX` (e.g., `meta1`)
* Metadata
  - The `odin-source` metadata is deprecated in favor of attributes on
    the `<igt>` elements:
    ```xml
    <igt id="igt123" tag-types="L G T" line-range="234-238" doc-id="1">
    ```
  - The `language` meta type is deprecated in favor of OLAC-style
    metadata, such as:
    ```xml
    <metadata>
      <meta id="meta1">
        <dc:subject xsi:type="olac:language" olac:code="...">...</dc:subject>
        <dc:language xsi:type="olac:language" olac:code="...">...</dc:language>
      </meta>
    </metadata>
    ```
  - Namespaces for the OLAC-style metadata are placed on `<xigt-corpus>`
  - Metadata in the ODIN text format are simplified for release
* Tiers
  - The cleaning and normalizing of ODIN data is now done with separate
    tiers. Cleaning should only attempt to fix errors in the input, and
    normalization can alter text (e.g. remove example numbers, rejoin
    lines, etc.).
  - The ODIN tiers are unified and distinguished with a `state` attribute:
    - `type="odin-raw"` becomes `type="odin" state="raw"`
    - `type="odin-clean"` becomes `type="odin" state="cleaned"` and
       `type="odin" state="normalized"`
* Judgments in the text for `L` or `T` lines are extracted and a `judgment`
  attribute is added to the `<item>`. Judgments are only extracted when
  one or more of `*`, `?`, or `#` appear at the beginning of the line.
  Note that this won't be 100% accurate, nor does it attempt to extract
  judgments from the middle of sentences (e.g. for alternations).
* Translation lines
  - Attempts are made to separate multiple translations into individual
    items, with the secondary ones getting tags like `+AL` for "alternate"
    and `+LT` for "literal"
  - Notes on translations (like `intended:` or `literally:`) get moved to
    a `note` attribute on the `<item>`.
* Filenames
  - Data subdirectories are now collected under a `data/` directory
  - Corpus collections of the same view are placed in a common subdirectory
    (e.g., `data/by-doc-id/` and `data/by-lang/`), and the collections are
    named by their format:
    - `data/by-doc-id/txt`
    - `data/by-doc-id/xigt`
    - `data/by-doc-id/xigt-enriched`
    - `data/by-lang/txt`
    - `data/by-lang/xigt`
    - `data/by-lang/xigt-enriched`
  - The `languages.txt` files are now grouped under a view directory (e.g.,
    `data/by-doc-id/languages.txt`), since they apply to all collections under
    that directory.
  - Some files had two extensions (*.txt.txt); these now have one (*.txt).
    (Also see "IDs" above)
  - Colons are not valid characters in Windows filenames, so the "by-lang"
    filenames like "aer:are.txt" are now hyphen-separated ("aer-are.txt")

### Removed

* The `full/` directory is removed


## [v2.0] - 2014.07.05

The 2.0 release of ODIN provides both the textual ODIN corpus and the
Xigt-encoded version XML version.

### Overview

There are five subdirectories:

* `full/` - The whole corpus in one large XigtXML file
* `by-doc-id/` - A XigtXML file for each source document
* `by-lang/` - A XigtXML file for each language code
* `txt-by-doc-id/` - The original text corpus, split by source document
* `txt-by-lang/` - The original text corpus, split by language

The XigtXML subdirectories also contain two additional files:

* `summary.txt` - an overview of the counts of items, languages, etc.
   for each file
* `languages.txt` - a listing of the languages found in each XML file

### Known bugs

(fixed in [v2.1](#v21---20160314))

* Inferred "glosses" and "translations" tiers in the XigtXML files do
  not have the "alignment" reference attribute specified, even when
  their items do specify it
* Inferred "glosses" and "translations" tiers use the "content"
  reference attribute to refer to a non-existent "p1" item (when it
  should be "p0")


[v2.0]: http://depts.washington.edu/uwcl/odin/
[v2.1]: http://depts.washington.edu/uwcl/odin/

