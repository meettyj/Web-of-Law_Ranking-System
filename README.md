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
  - Key Phrase in cited paragraph information (indegree and outdegree. Only consider those in extracted BM25 files. Currently sum the calculation of each word in a query)
  
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

## Six Feature Combined Final Score Example
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

## Seven Feature Combined Final Score Example
- Query: ['adult', 'probation']

- Result: [Doc ID, Socre]
  <table>
    <tr>
      <td>[2959732, 0.7139687123798589]</td>
      <td>[146553, 0.6996682244009027]</td>
      <td>[146790, 0.5955299940227667]</td>
      <td>[110585, 0.5284526674835871]</td>
      <td>[110117, 0.5107971667420876]</td>
    </tr>
    <tr>
      <td>[150543, 0.4625262694688515]</td>
      <td>[108785, 0.4259980795587641]</td>
      <td>[109775, 0.3626328000562868]</td>
      <td>[107439, 0.36041351715460673]</td>
      <td>[111198, 0.35382553600583294]</td>
    </tr>
    <tr>
      <td>[111105, 0.3438249779394623]</td>
      <td>[107693, 0.3437423016784042]</td>
      <td>[109093, 0.33327570172525584]</td>
      <td>[107191, 0.3292890826772249]</td>
      <td>[110425, 0.3216467486776624]</td>
    </tr>
    <tr>
      <td>[110896, 0.3177370762025689]</td>
      <td>[109258, 0.27835855520777486]</td>
      <td>[111977, 0.2686333876944729]</td>
      <td>[101183, 0.2645319378239483]</td>
      <td>[109842, 0.185147263099679]</td>
    </tr>
  </table>

## Annotation
The annotation tool is available to work now. The link is below: https://annotation-scotus.herokuapp.com/. Currently we have 200 docs in total. Every 20 docs correspond to one query like 'mail fraud' and 'homicide'. We are trying to distinguish whether the query is relevant to the given doc. If anyone who'd like to help us with annotating work, please let me know, so I can set an account for him/her.

## Queries Collection
https://docs.google.com/forms/d/e/1FAIpQLScfhF0-PVyYCnbHuMJK0i7fWEnGlfI0HiRYO9ecOrQbB8CsEQ/viewform

## Log
4.18: adult_probation & mail_fraud

## Evaluation
Average precision (AP) and Mean average precision (MAP) based on top N (currently N range from 1 to 20, given extracted 20 docs under one specific query).

## What's Next
- Waiting for real queries and test the system performance on real queries.
- Evaluate the ranking result and fine-tune the system.
- Transfomer in legal domain. Visualize the distribution of attention by heatmap.


