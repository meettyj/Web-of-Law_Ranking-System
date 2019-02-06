# Web-of-Law_Ranking-System
This Project focuses on processing legal court decisions and is part of on-going research at New York University. This code is in development and is not ready for public release. Initially, we are using github as a version-control and development tool.

## How To Run
To generate one document for 'BM25' algorithm to rank, you need first run `$ python generate_corpus.py` in BM25 folder. It will iterate all documents given in corpus and then, create one including all text data. After that, you can run `$ python main.py` to print the ranking result of 'BM25'. Using command `nohup python main.py &> ./result/RESULT_10query_allScotus.txt &` to save it in result folder.

## Feature Description
- BM25 retrieval
- Calculate individual scores
  - Word-level Query-Content relatedness (sum of word similarity with GoogleNews embedding)
  - Key Phrase overlap between Query and Docs (Single item in Query & conbination of query. Based on RAKE algorithm, decayed on each position with ratio 0.95.)

## Example Data
- Query List:   
  <table>
    <tr>
      <td>adult probation</td>
      <td>arson</td>
      <td>bankruptcy fraud</td>
      <td>capital crime</td>
      <td>civil rights</td>
    </tr>
    <tr>
      <td>corporate takeover</td>
      <td>ethical will</td>
      <td>divorce</td>
      <td>mail fraud</td>
      <td>homicide</td>
    </tr>
  </table>

- Corpus: all SCOTUS dataset text.

## BM25 Example Result
Given data described before, we can get ranking results for 10 queries. Here we only list some of them for tasting.  

<img src="https://github.com/meettyj/Web-of-Law_Ranking-System/raw/master/result/example_result.png" width="500" hegiht="313" align=center />
<!-- ![image](https://github.com/meettyj/Web-of-Law_Ranking-System/raw/master/BM25/result/example_result.png) -->


## What's Next
Scoring part:
- Query-Content entailment score
- Timestamp (the most recent the higher)
- Weighted on chain length, use first three scores only
- cited with local citation graph
