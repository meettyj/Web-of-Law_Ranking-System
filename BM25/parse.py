import re


class CorpusParser:

	def __init__(self, filename):
		self.filename = filename
		self.regex = re.compile('^#\s*\d+')
		self.corpus = dict()

	def parse(self):
		with open(self.filename) as f:
			s = ''.join(f.readlines())
		# blobs = s.split('#')[1:]
		blobs = s.split('# ')[:]
		# print(blobs)
		print('length of blobs:', len(blobs))
		blobs.pop(0)
		for x in blobs:
			# print('length of x: ', len(x))
			text = x.split()
			# print('length of text', len(text))
			docid = text.pop(0)
			self.corpus[docid] = text

	def get_corpus(self):
		return self.corpus


class QueryParser:

	def __init__(self, filename):
		self.filename = filename
		self.queries = []

	def parse(self):
		with open(self.filename) as f:
			lines = ''.join(f.readlines())
		# self.queries = [x.rstrip().split() for x in lines.split('\n')[:-1]]
		self.queries = [x.rstrip().split() for x in lines.split('\n')]

	def get_queries(self):
		return self.queries


if __name__ == '__main__':
	qp = QueryParser('text/queries.txt')
	print(qp.get_queries())