from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
import spacy


class RelationExtractorModel:

    def __init__(self):
        # self.model = Pipeline([('vect', DictVectorizer()), ('tfidf', TfidfTransformer()), (
        # 'clf-svm', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42))])
        self.model = Pipeline([('vect', DictVectorizer()), ('tfidf', TfidfTransformer()), (
            'clf-svm', svm.SVC(kernel='poly', gamma=1, C=1, degree=2))])

    def train(self, features, targets):
        print("training started")
        if len(features) != len(targets):
            raise ValueError('number of targets mismatch number of data sets')
        self.model.fit(features, targets)
        print("model trained!")

    def reset_model(self):
        self.model = Pipeline([
            ('vectorizer', DictVectorizer(sparse=False)),
            ('classifier', DecisionTreeClassifier(criterion='entropy'))
        ])

    def predict(self, features):
        return self.model.predict(features)

    def sklearn_test(self, features, targets):
        #  returns an accuracy score based on the fed features and the target predictions using
        #  the sklearn score function
        return self.model.score(features, targets)

    @staticmethod
    def split_data(features, targets, training_size):
        #  splits the data into a training and a test set based on the training_size float value between 0 and 1
        return train_test_split(features, targets, test_size=training_size)
