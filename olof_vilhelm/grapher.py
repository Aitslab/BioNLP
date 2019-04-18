import read_bioinfer as rb
import numpy as np

from keras.models import Model
from keras import layers
from keras import Input
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
from sklearn.feature_extraction import DictVectorizer
from sklearn import linear_model
from sklearn import metrics

## adjacency matrix mellan orden för att representera grafen!
## dock kräver detta tf_serialize_tensor och sedan tf.parse_tensor


SENTENCE_NR = 0
bioinfer = rb.BioInfer("corpus/BioInfer_corpus_1.1.1.xml")
final_tokens = []
final_adjacencies = []
final_relations = []
final_formulas = []
sentences = bioinfer.sentences()
for sentence in sentences:
    # sentence = bioinfer.sentences()[SENTENCE_NR] ## hämtar bara sentence 2
    entities = bioinfer.entities(sentence["id"])
    id_tokens = bioinfer.tokens(sentence["id"])
    dependencies = bioinfer.dependencies(sentence["id"])
    ## spara enbart tokens i en vektor
    tokens = []
    for token in id_tokens:
        tokens.append(token["text"])

    # skapa matris med nollor (adjacency)
    # fyll matrisen för varje dependency åt båda hållen (sätt 1 typ)
    length = len(tokens)  # + 1 pga root
    adj_mat = np.zeros(shape=(length, length), dtype=bool)
    relations = [""]*length  # spara även alla deprels i en vektor
    for dep in dependencies:
        adj_mat[dep["head"]][dep["word"]] = 1
        adj_mat[dep["word"]][dep["head"]] = 1
        relations[dep["word"]] = dep["deprel"]
    # print(tokens)
    # print(adj_mat)
    # print(relations)
    final_tokens.append(tokens)
    final_adjacencies.append(adj_mat)
    final_relations.append(relations)
# multi-input med tokens, adj_mat och relations
print(final_tokens)

formulas = np.random.randint(0, 2, len(final_relations))

final_formulas = to_categorical(formulas)


token_vocabulary_size = len(final_tokens) + 2  # +2?
token_input = Input(shape=(None,), dtype='int32', name='token')  # varför int32?
embedded_token = layers.Embedding(token_vocabulary_size, 64, mask_zero=True)(token_input)
encoded_token = layers.LSTM(32, return_sequences=True)(embedded_token)

adj_mat_vocabulary_size = len(final_adjacencies) + 2
adj_mat_input = Input(shape=(None,), dtype='int32', name='adj_mat')  # borde nog också specifiera att det här är matris
embedded_adj_mat = layers.Embedding(adj_mat_vocabulary_size, 32, mask_zero=True)(adj_mat_input)
encoded_adj_mat = layers.LSTM(16, return_sequences=True)(embedded_adj_mat)

relation_vocabulary_size = len(final_relations) + 2
relation_input = Input(shape=(None,), dtype='int32', name='relation')
embedded_relation = layers.Embedding(relation_vocabulary_size, 32, mask_zero=True)(relation_input)
encoded_relation = layers.LSTM(16, return_sequences=True)(embedded_relation)

concatenated = layers.concatenate([encoded_token, encoded_adj_mat, encoded_relation], axis=-1)

formula_size = len(final_formulas) + 2
formula = layers.Dense(formula_size, activation='softmax')(encoded_token) # concatenated

model = Model([token_input, adj_mat_input, relation_input], formula) #
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['acc'])
model.fit({'token': final_tokens, 'adj_mat': final_adjacencies, 'relation': final_relations}, final_formulas,
          epochs=3, batch_size=128)