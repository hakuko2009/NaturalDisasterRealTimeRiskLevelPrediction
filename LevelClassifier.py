from nltk import NaiveBayesClassifier, classify
import DataLoader
import random


class LevelClassifier:
    def get_features(self):
        # classify into 4 level (0 -> 3)
        level_0, level_1, level_2, level_3 = self._load_cases()

        feature_set = list()

        for case in level_0:
            features = self._case_features(case)
            features['level_0'] = 1.0
            features['level_1'] = 0.0
            features['level_2'] = 0.0
            features['level_3'] = 0.0
            feature_set.append((features, 'L0'))

        for case in level_1:
            features = self._case_features(case)
            features['level_0'] = 0.0
            features['level_1'] = 1.0
            features['level_2'] = 0.0
            features['level_3'] = 0.0
            feature_set.append((features, 'L1'))

        for case in level_2:
            features = self._case_features(case)
            features['level_0'] = 0.0
            features['level_1'] = 0.0
            features['level_2'] = 1.0
            features['level_3'] = 0.0
            feature_set.append((features, 'L2'))

        for case in level_3:
            features = self._case_features(case)
            features['level_0'] = 0.0
            features['level_1'] = 0.0
            features['level_2'] = 0.0
            features['level_3'] = 1.0
            feature_set.append((features, 'L3'))

        return feature_set

    def train_and_test(self, training_percent=0.80):
        feature_set = self.get_features()
        random.shuffle(feature_set)

        case_count = len(feature_set)

        cut_point = int(case_count * training_percent)

        train_set = feature_set[:cut_point]
        test_set = feature_set[cut_point:]

        self.train(train_set)

        return self.test(test_set)

    def classify(self, case):
        feats = self._case_features(case)
        return self.classifier.classify(feats)

    def train(self, train_set):
        self.classifier = NaiveBayesClassifier.train(train_set)
        return self.classifier

    def test(self, test_set):
        return classify.accuracy(self.classifier, test_set)

    def get_most_informative_features(self, n=5):
        return self.classifier.most_informative_features(n)

    def _load_cases(self):
        return DataLoader.get_case_list()

    def _case_features(self, features):
        return {
            'year': features[0],
            'subtype': features[1],
            'country': features[2],
            'region': features[3],
            'startMonth': features[4],
            'endMonth': features[5]
        }


if __name__ == "__main__":
    gp = LevelClassifier()
    accuracy = gp.train_and_test()
    print('Accuracy: %f' % accuracy)
    print('Most Informative Features')
    feats = gp.get_most_informative_features(10)
    for feat in feats:
        print('\t%s = %s' % feat)
    case = input('Enter case to classify: ')
    print('\n%s is classified as %s' % (case, gp.classify(case)))


def classify_level(case):
    gp = LevelClassifier()
    acc = gp.train_and_test()
    print('Accuracy: %f' % acc)
    return gp.classify(case)
