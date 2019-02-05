import os

def main():
	# out_dir = './data/test_scotus_corpus.txt'
	out_dir = '../data/1K_scotus_corpus.txt'
	corpus_dir = '../data/1K_scotus_text/'
	# out_dir = './data/all_scotus_corpus.txt'
	# corpus_dir = '../all_scotus_text/'
	# corpus_dir = './data/test_scotus_text/'
	corpus_files = os.listdir(corpus_dir)
	# id_corpus = 0
	with open(out_dir, 'a') as out_f:
		for file in corpus_files:
			# id_corpus += 1
			file_name = file.split('.')[0]
			# print(file.split('.')[0])
			# out_f.write('# '+ str(id_corpus) + '\n')
			out_f.write('# '+ file_name + '\n')
			# out_f.write(str(id_corpus))
			with open(corpus_dir + file, mode='r') as each_f:
				all_text = each_f.read()
				out_f.write(all_text)
	print('finished generated')


if __name__ == '__main__':
	main()