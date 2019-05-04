import read_bioinfer as rb
import numpy as np

from keras.models import Model
from keras import layers
from keras import Input
from keras.utils.np_utils import to_categorical


SENTENCE_NR = 0
bioinfer = rb.BioInfer("corpus/BioInfer_corpus_1.1.1.xml")
final_tokens = []
final_adjacencies = []
final_relations = []
final_classes = []
final_sources = []
final_targets = []
sentences = bioinfer.sentences()
for sentence in sentences:
    # sentence = bioinfer.sentences()[SENTENCE_NR] ## hämtar bara sentence 2
    entities = bioinfer.entities(sentence["id"])
    id_tokens = bioinfer.tokens(sentence["id"])
    dependencies = bioinfer.dependencies(sentence["id"])
    id_classes = bioinfer.relationships(sentence["id"])

    ## spara enbart tokens i en vektor
    tokens = []
    for token in id_tokens:
        tokens.append(token["text"])

    length = len(tokens)
    adj_mat = np.zeros(shape=(length, length), dtype=bool)
    # skapa matris med nollor (adjacency)
    # fyll matrisen för varje dependency åt båda hållen (sätt 1 typ)
    relations = [""] * length  # spara även alla deprels i en vektor
    for dep in dependencies:
        adj_mat[dep["head"]][dep["word"]] = 1
        adj_mat[dep["word"]][dep["head"]] = 1
        relations[dep["word"]] = dep["deprel"]

    for c in id_classes:
        if c["class"] == 'NEGATIVE':
            final_classes.append(0)
        if c["class"] == 'POSITIVE':
            final_classes.append(1)
        if c["class"] == 'OTHER':
            final_classes.append(2)
        final_sources.append(c["source"])
        final_targets.append(c["target"])


        # print(tokens)
        # print(adj_mat)
        # print(relations)
        final_tokens.append(tokens)
        final_adjacencies.append(adj_mat)
        final_relations.append(relations)

# multi-input med tokens, adj_mat, relations, source och target.
# följt pierres notebook 5.3, men finns en hel del frågetecken.
# pierre gör ett set med unika ord/ner/pos, sedan använder han bara index till dessa i inlärning.
# Borde vi också kanske göra? 

token_vocabulary_size = len(final_tokens) + 2  # +2?
token_input = Input(shape=(None,), dtype='int32', name='token')  # Borde vara annan dtype?
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

target_vocabulary_size = len(final_targets) + 2
target_input = Input(shape=(None,), dtype='int32', name='target')
embedded_target = layers.Embedding(target_vocabulary_size, 32, mask_zero=True)(target_input)
encoded_target = layers.LSTM(16, return_sequences=True)(embedded_target)

source_vocabulary_size = len(final_sources) + 2
source_input = Input(shape=(None,), dtype='int32', name='source')
embedded_source = layers.Embedding(source_vocabulary_size, 32, mask_zero=True)(source_input)
encoded_source = layers.LSTM(16, return_sequences=True)(embedded_source)


concatenated = layers.concatenate([encoded_token, encoded_adj_mat, encoded_relation, encoded_source, encoded_target], axis=-1)
final_classes = to_categorical(final_classes)
class_size = len(final_classes) + 2
c = layers.Dense(class_size, activation='softmax')(concatenated)

model = Model([token_input, adj_mat_input, relation_input, source_input, target_input], c)
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['acc'])
model.fit({'token': final_tokens, 'adj_mat': final_adjacencies, 'relation': final_relations, 'source': final_sources,
           'target': final_targets}, final_classes, epochs=3, batch_size=128)
