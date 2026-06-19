# Natural Language Processing (NLP) Functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- NLP
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/nlp-functions.md)# Natural Language Processing (NLP) functions


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)
Not supported in ClickHouse Cloud
## detectCharset[​](#detectCharset "Direct link to detectCharset")


Introduced in: v22\.2\.0


Detects the character set of a non\-UTF8\-encoded input string.


NoteThis function is experimental and may change in unpredictable backwards\-incompatible ways in future releases.
Set `allow_experimental_nlp_functions = 1` to enable it.


**Syntax**



```
detectCharset(s)

```

**Arguments**


- `s` — The text to analyze. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string containing the code of the detected character set [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Basic usage**



```
SELECT detectCharset('Ich bleibe für ein paar Tage.')

```


```
WINDOWS-1252

```

## detectLanguage[​](#detectLanguage "Direct link to detectLanguage")


Introduced in: v22\.2\.0


Detects the language of the UTF8\-encoded input string.
The function uses the [CLD2 library](https://github.com/CLD2Owners/cld2) for detection and returns the 2\-letter ISO language code.


The longer the input, the more precise the language detection will be.


NoteThis function is experimental and may change in unpredictable backwards\-incompatible ways in future releases.
Set `allow_experimental_nlp_functions = 1` to enable it.


**Syntax**



```
detectLanguage(s)

```

**Arguments**


- `text_to_be_analyzed` — The text to analyze. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the 2\-letter ISO code of the detected language. Other possible results: `un` \= unknown, can not detect any language, `other` \= the detected language does not have 2 letter code. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Mixed language text**



```
SELECT detectLanguage('Je pense que je ne parviendrai jamais à parler français comme un natif. Where there\'s a will, there\'s a way.')

```


```
fr

```

## detectLanguageMixed[​](#detectLanguageMixed "Direct link to detectLanguageMixed")


Introduced in: v22\.2\.0


Similar to the [`detectLanguage`](#detectLanguage) function, but `detectLanguageMixed` returns a `Map` of 2\-letter language codes that are mapped to the percentage of the certain language in the text.


NoteThis function is experimental and may change in unpredictable backwards\-incompatible ways in future releases.
Set `allow_experimental_nlp_functions = 1` to enable it.


**Syntax**



```
detectLanguageMixed(s)

```

**Arguments**


- `s` — The text to analyze [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a map with keys which are 2\-letter ISO codes and corresponding values which are a percentage of the text found for that language [`Map(String, Float32)`](/docs/sql-reference/data-types/map)


**Examples**


**Mixed languages**



```
SELECT detectLanguageMixed('二兎を追う者は一兎をも得ず二兎を追う者は一兎をも得ず A vaincre sans peril, on triomphe sans gloire.')

```


```
{'ja':0.62,'fr':0.36}

```

## detectLanguageUnknown[​](#detectLanguageUnknown "Direct link to detectLanguageUnknown")


Introduced in: v22\.2\.0


Similar to the [`detectLanguage`](#detectLanguage) function, except the detectLanguageUnknown function works with non\-UTF8\-encoded strings.
Prefer this version when your character set is UTF\-16 or UTF\-32\.


NoteThis function is experimental and may change in unpredictable backwards\-incompatible ways in future releases.
Set `allow_experimental_nlp_functions = 1` to enable it.


**Syntax**



```
detectLanguageUnknown('s')

```

**Arguments**


- `s` — The text to analyze. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the 2\-letter ISO code of the detected language. Other possible results: `un` \= unknown, can not detect any language, `other` \= the detected language does not have 2 letter code. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Basic usage**



```
SELECT detectLanguageUnknown('Ich bleibe für ein paar Tage.')

```


```
de

```

## detectTonality[​](#detectTonality "Direct link to detectTonality")


Introduced in: v22\.2\.0


Determines the sentiment of the provided text data.


LimitationThis function is limited in its current form in that it makes use of the embedded emotional dictionary and only works for the Russian language.


NoteThis function is experimental and may change in unpredictable backwards\-incompatible ways in future releases.
Set `allow_experimental_nlp_functions = 1` to enable it.


**Syntax**



```
detectTonality(s)

```

**Arguments**


- `s` — The text to be analyzed. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the average sentiment value of the words in text [`Float32`](/docs/sql-reference/data-types/float)


**Examples**


**Russian sentiment analysis**



```
SELECT
    detectTonality('Шарик - хороший пёс'),
    detectTonality('Шарик - пёс'),
    detectTonality('Шарик - плохой пёс')

```


```
0.44445, 0, -0.3

```

## lemmatize[​](#lemmatize "Direct link to lemmatize")


Introduced in: v21\.9\.0


Performs lemmatization on a given word.
This function needs dictionaries to operate, which can be obtained from [github](https://github.com/vpodpecan/lemmagen3/tree/master/src/lemmagen3/models).
For more details on loading a dictionary from a local file see page ["Defining Dictionaries"](/docs/sql-reference/statements/create/dictionary/sources/local-file).


NoteThis function is experimental and may change in unpredictable backwards\-incompatible ways in future releases.
Set `allow_experimental_nlp_functions = 1` to enable it.


**Syntax**



```
lemmatize(lang, word)

```

**Arguments**


- `lang` — Language which rules will be applied. [`String`](/docs/sql-reference/data-types/string)
- `word` — Lowercase word that needs to be lemmatized. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the lemmatized form of the word [`String`](/docs/sql-reference/data-types/string)


**Examples**


**English lemmatization**



```
SELECT lemmatize('en', 'wolves')

```


```
wolf

```

## stem[​](#stem "Direct link to stem")


Introduced in: v21\.9\.0


Performs stemming on a word or an array of words using the Snowball algorithms.
Each input string must be a single, lowercase word — strings containing whitespace cause an exception.
Passing uppercase characters produces undefined results.
Returns String for scalar inputs (including FixedString) and Array(String) for array inputs.
Nullable and LowCardinality variants of String and FixedString are supported.


**Syntax**



```
stem(word, language)

```

**Arguments**


- `word` — A single lowercase word (or array of words) to stem. Must be lowercase — uppercase characters produce undefined results. Accepts String, FixedString, Array(String), Array(FixedString), Array(Nullable(String)), or Array(Nullable(FixedString)). [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring) or [`Array(String)`](/docs/sql-reference/data-types/array) or [`Array(FixedString)`](/docs/sql-reference/data-types/array)
- `language` — Language whose stemming rules will be applied. Use the two\-letter ISO 639\-1 code (e.g. 'en', 'de', 'fr'), see <https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes>. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


The stemmed form of the word (String), or an array of stemmed words (Array(String)). [`String`](/docs/sql-reference/data-types/string) or [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**Stemming a single word**



```
SELECT stem('blessing', 'en') AS res

```


```
bless

```

**Stemming an array of words**



```
SELECT stem(['blessing', 'disguise'], 'en') AS res

```


```
['bless','disguis']

```

**Stemming a FixedString**



```
SELECT stem(toFixedString('blessing', 10), 'en') AS res

```


```
bless

```

**Stemming a Nullable word**



```
SELECT stem(toNullable('blessing'), 'en') AS res

```


```
bless

```

## synonyms[​](#synonyms "Direct link to synonyms")


Introduced in: v21\.9\.0


Finds synonyms of a given word.


There are two types of synonym extensions:


- `plain`
- `wordnet`


With the `plain` extension type you need to provide a path to a simple text file, where each line corresponds to a certain synonym set.
Words in this line must be separated with space or tab characters.


With the `wordnet` extension type you need to provide a path to a directory with the WordNet thesaurus in it.
The thesaurus must contain a WordNet sense index.


NoteThis function is experimental and may change in unpredictable backwards\-incompatible ways in future releases.
Set `allow_experimental_nlp_functions = 1` to enable it.


**Syntax**



```
synonyms(ext_name, word)

```

**Arguments**


- `ext_name` — Name of the extension in which search will be performed. [`String`](/docs/sql-reference/data-types/string)
- `word` — Word that will be searched in extension. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns array of synonyms for the given word. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**Find synonyms**



```
SELECT synonyms('list', 'important')

```


```
['important','big','critical','crucial']

```
[PreviousMathematical](/docs/sql-reference/functions/math-functions)[NextNumericIndexedVector](/docs/sql-reference/functions/numeric-indexed-vector-functions)- [detectCharset](#detectCharset)- [detectLanguage](#detectLanguage)- [detectLanguageMixed](#detectLanguageMixed)- [detectLanguageUnknown](#detectLanguageUnknown)- [detectTonality](#detectTonality)- [lemmatize](#lemmatize)- [stem](#stem)- [synonyms](#synonyms)
Was this page helpful?
