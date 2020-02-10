# BlankSort
A Novel Unsupervised Approach to Keyword Extraction

## Sections

1. [Proposal](#Proposal)
1. [Definitions](#Definitions)
1. [Inspiration and Approach](#Inspiration-And-Approach)
1. [Algorithm](#Algorithm)
1. [Evaluation](#Evaluation)


## Proposal
* Keyword extraction is useful for web searching, article tagging, text categorization, and other text processing tasks.
* Current approaches can be categorized into three types:
    * Statistical – extremely fast but low accuracy
    * Graphs & Unsupervised Algorithms – high accuracy but poor efficiency and speed
    * Supervised learning – high accuracy and diversity but requires manually labeled datasets for training
* State-of-the-art algorithms:
    * TextRank (Unsupervised Graph)
    * TopicRank (Unsupervised Graph)
    * RAKE (Statistical Model)
    * MultipartiteRank (Unsupervised Graph)
* BlankSort – novel unsupervised approach
    * High efficiency and accuracy
    * Corpus independent, requires no additional data
    * Employs language comprehension for optimal keyword selection
* Results
    * Metrics: precision, recall, f1-score, execution time
    * Evaluation datasets:
        * Lemmatized variants of:
            * Inspec (research paper abstracts)
            * DUC (short articles)
            * NUS (full-length research papers)
    * Outperforms state of the art algorithms in most metrics


## Definitions
| Term              | Definition                         |
|-------------------|------------------------------------|
| Tokens            | An ordered list of filtered words. |
| Target word       | A word that is potentially a keyword. |
| Context           | A set of words that surround a target word that are within a constant number of tokens away. |
| Contexts          | The set of all pairs of target words and their contexts. |
| Word vector       | A pre-trained vector representation of a word. |
| Cosine similarity | A function that calculates the similarity of two word vectors. Values are in the range [-1,1], where 1 is the maximum similarity and -1 is the minimum. |

## Inspiration and Approach
* In most languages such as English, text is extremely sparse – the number of keywords is very small in comparison to the total number of words in the document.
* In sparse texts, words that are important to the entire document are also important in their paragraph and sentence.
    * For example, if the word “algorithm” is important in a document, the surrounding sentence or paragraph most likely discusses algorithms.
* Paragraphs and sentences can be broken down into “contexts”, with the word in the center of the window being the “target word”.
* Because the document is sparse, the contexts are also sparse – therefore, each small context likely contains at most one keyword.
* The most important word in each context can be determined by finding the most unique word.
* The uniqueness of a target word can be determined by measuring how much the word stands out from its surrounding words.
* If a word stands out from the rest, it must be difficult to “guess” when given the surrounding words.
* Therefore, the uniqueness of a word answers the question: “How difficult is it to guess the target word, given only its context words?”
* Every target word can be assigned a “uniqueness score”, which measures its uniqueness based on the average cosine similarity between the word and its context words.
* Sorting the words by uniqueness score in ascending order yields a list of words sorted by their importance.


## Algorithm
* Figure 1.1
    * The input document is passed to the algorithm.
* Figure 1.2
	* The text is filtered and tokenized into an array of individual words.
* Figure 1.3
	* The contexts for each target word are generated.
* Figure 1.4
	* Similarity scores are computed for each target word and context word using word vectors.
* Figure 1.5
	* The similarity scores are averaged for each target word, and the words are sorted by their scores in ascending order.
* Figure 1.6
	* The specified number of words with the lowest average similarity scores are selected.

## Evaluation
* Lemmatized variants of Inspec, DUC, and NUS datasets
    * Inspec: 2000 abstracts from scientific journals
        * Anette Hulth (2003)
    * DUC 2001: 308 medium articles
        * Xiaojun Wan and Jianguo Xiao (2008)
    * NUS: 211 full scientific conference papers
        * Thuy Dung Nguyen and Min-yen Kan (2007)
    * Comparison against:
        * MultipartiteRank
        * Rapid Automatic Keyword Extraction (RAKE)
        * TextRank
        * TopicRank

