import gensim

pretrained_embeddings_path = "../../word2vec/GoogleNews-vectors-negative300.bin"
# model = gensim.models.word2vec.Word2Vec.load(pretrained_embeddings_path)

# Load Google's pre-trained Word2Vec model.
model = gensim.models.Word2Vec.load_word2vec_format('./model/GoogleNews-vectors-negative300.bin', binary=True)











