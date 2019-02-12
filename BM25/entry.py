import operator

from BM25.query import QueryProcessor
from BM25.parse import *
import os


def main_BM25(path_Query, path_Corpus, length_BM25):
	print(os.path.abspath('.'))
	# qp = QueryParser(filename='./text/queries.txt')
	qp = QueryParser(filename = path_Query)
	cp = CorpusParser(filename = path_Corpus)
	# cp = CorpusParser(filename='./data/test_scotus_corpus.txt')
	# cp = CorpusParser(filename='./data/all_scotus_corpus.txt')
	qp.parse()
	queries = qp.get_queries()
	cp.parse()
	corpus = cp.get_corpus()
	proc = QueryProcessor(queries, corpus)
	results = proc.run()
	qid = 0
	return_dict = {}
	BM25_score_result = {}

	# below is for showing on screen
	print('QID\tDocsID\tRank\tScore\t\t\t\tQuery')
	for result in results:
		sorted_x = sorted(result.items(), key=operator.itemgetter(1))
		sorted_x.reverse()
		index = 1
		temp_list = []
		score_temp_list = []
		for i in sorted_x[:length_BM25]:
			temp_list.append(i[0])
			score_temp_list.append([int(i[0]), i[1]])
			tmp = (qid+1, i[0], index, i[1], queries[qid])
			# below to print the result on screen
			print ('{}\t{}\t{}\t{}\t{}'.format(*tmp))
			index += 1
		return_dict[qid] = temp_list
		BM25_score_result[qid] = score_temp_list
		# return_dict[qid] = []
		# return_dict[qid].update(temp_list)
		qid += 1
		print('\n')

	return queries, return_dict, BM25_score_result
#
# if __name__ == '__main__':
# 	main()