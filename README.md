# Web-of-Law_Ranking-System
This Project focuses on processing legal court decisions and is part of on-going research at New York University. This code is in development and is not ready for public release. Initially, we are using github as a version-control and development tool.

## How To Run
To generate one document for 'BM25' algorithm to rank, you need first run `$ python generate_corpus.py` in BM25 folder. It will iterate all documents given in corpus and then, create one including all text data. After that, you can run `$ python main.py` to print the ranking result of 'BM25'. Using command `nohup python main.py &> ./result/RESULT_10query_allScotus.txt &` to save it in result folder.

## Feature Description
- BM25 retrieval
- Calculate individual scores
  - BM25 extracted score.
  - Word-level Query-Content relatedness (sum of word similarity with GoogleNews embedding)
  - Key Phrase overlap between Query and Docs (Single item in Query & conbination of query. Based on RAKE algorithm, decayed on each position with ratio 0.95)
  - Timestamp consideration (the most recent the higher. Decay rate 0.05 for now)
  - Direct cited with local citation graph (indegree and outdegree. Only consider those in extracted BM25 files)
  - Indirect cited on citation graph chain (Use first three chain only, each with 0.35 weight decay)
  
- Normalized the above score into range 1 and combined to generate new score.

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

## Six feature combined final score Example
- Query: ['adult', 'probation']

- Result: [Doc ID, Socre]
  <table>
    <tr>
      <td>[110117, 0.45648130703581674]</td>
      <td>[110585, 0.4285737737881382]</td>
      <td>[146790, 0.40441472797427647]</td>
      <td>[2959732, 0.34090307630334943]</td>
      <td>[107693, 0.3342951043682529]</td>
    </tr>
    <tr>
      <td>[146553, 0.32676667267588216]</td>
      <td>[108785, 0.3256834050257937]</td>
      <td>[109093, 0.32430868339245533]</td>
      <td>[109775, 0.3084585056242143]</td>
      <td>[111105, 0.2891431612767075]</td>
    </tr>
    <tr>
      <td>[150543, 0.2715544427348346]</td>
      <td>[110425, 0.26700141561834106]</td>
      <td>[110896, 0.2632105162435864]</td>
      <td>[107439, 0.2604221962354819]</td>
      <td>[111977, 0.2599154005857053]</td>
    </tr>
    <tr>
      <td>[101183, 0.25571265883711564]</td>
      <td>[111198, 0.25346496019722]</td>
      <td>[107191, 0.2297795760028584]</td>
      <td>[109258, 0.2238365716979934]</td>
      <td>[109842, 0.176073844381976]</td>
    </tr>
  </table>


## What's Next
Scoring part:
- Any suggestions? Or we may need to some annotation work first.

Annotation part:
- Brat or other annotation tool
