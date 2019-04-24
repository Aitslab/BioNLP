from sklearn import svm
from sklearn.model_selection import train_test_split


class RelationExtractorModel:

    def __init__(self):
        self.model = svm.SVC(gamma='scale')

    def train(self, features, targets):
        if len(features) != len(targets):
            raise ValueError('number of targets mismatch number of data sets')
        self.model.fit(features, targets)

    def reset_model(self):
        self.model = svm.SVC(gamma='scale')

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
