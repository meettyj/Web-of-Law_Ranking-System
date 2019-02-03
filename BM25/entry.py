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
	return_list = []

	# below is for showing on screen
	print('QID\tDocsID\tRank\tScore\t\t\t\tQuery')
	for result in results:
		sorted_x = sorted(result.items(), key=operator.itemgetter(1))
		sorted_x.reverse()
		index = 1
		temp_list = []
		for i in sorted_x[:length_BM25]:
			temp_list.append(i[0])
			tmp = (qid+1, i[0], index, i[1], queries[qid])
			print ('{}\t{}\t{}\t{}\t{}'.format(*tmp))
			# print ('{:>1}\tQ0\t{:>4}\t{:>2}\t{:>12}\tNH-BM25'.format(*tmp))
			index += 1
		qid += 1
		print('\n')

	return return_list
#
# if __name__ == '__main__':
# 	main()