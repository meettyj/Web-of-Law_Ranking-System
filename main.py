from parse import *
from query import QueryProcessor
import operator


def main():
	# qp = QueryParser(filename='./text/queries.txt')
	qp = QueryParser(filename='./data/10_query_list.txt')
	# cp = CorpusParser(filename='./data/1K_scotus_corpus.txt')
	# cp = CorpusParser(filename='./data/test_scotus_corpus.txt')
	cp = CorpusParser(filename='./data/all_scotus_corpus.txt')
	qp.parse()
	queries = qp.get_queries()
	cp.parse()
	corpus = cp.get_corpus()
	proc = QueryProcessor(queries, corpus)
	results = proc.run()
	qid = 0
	print('QID\tDocsID\tRank\tScore\t\t\t\tQuery')
	for result in results:
		sorted_x = sorted(result.items(), key=operator.itemgetter(1))
		sorted_x.reverse()
		index = 1
		for i in sorted_x[:10]:
			tmp = (qid+1, i[0], index, i[1], queries[qid])
			print ('{}\t{}\t{}\t{}\t{}'.format(*tmp))
			# print ('{:>1}\tQ0\t{:>4}\t{:>2}\t{:>12}\tNH-BM25'.format(*tmp))
			index += 1
		qid += 1
		print('\n')


if __name__ == '__main__':
	main()