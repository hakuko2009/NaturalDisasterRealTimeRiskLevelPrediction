from nltk import NaiveBayesClassifier, classify
import DataLoader
import random
import model.CaseOfDisaster as Case
from datetime import datetime


def _case_features(caseFeatures):
    return {
        'year': caseFeatures[1],
        'subtype': caseFeatures[2],
        'country': caseFeatures[3],
        'region': caseFeatures[4],
        'startMonth': caseFeatures[5],
        'endMonth': caseFeatures[6]
    }


class LevelClassifier:
    def get_features(self):
        # classify into 4 level (0 -> 3)
        level_0, level_1, level_2, level_3 = DataLoader.get_case_list()

        feature_set = list()

        for cases in level_0:
            features = _case_features(cases)
            features['level_0'] = 1.0
            features['level_1'] = 0.0
            features['level_2'] = 0.0
            features['level_3'] = 0.0
            feature_set.append((features, 'L0'))

        for cases in level_1:
            features = _case_features(cases)
            features['level_0'] = 0.0
            features['level_1'] = 1.0
            features['level_2'] = 0.0
            features['level_3'] = 0.0
            feature_set.append((features, 'L1'))

        for cases in level_2:
            features = _case_features(cases)
            features['level_0'] = 0.0
            features['level_1'] = 0.0
            features['level_2'] = 1.0
            features['level_3'] = 0.0
            feature_set.append((features, 'L2'))

        for cases in level_3:
            features = _case_features(cases)
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
        features = _case_features(case)
        return self.classifier.classify(features)

    def train(self, train_set):
        self.classifier = NaiveBayesClassifier.train(train_set)
        return self.classifier

    def test(self, test_set):
        return classify.accuracy(self.classifier, test_set)

    def get_most_informative_features(self, n=5):
        return self.classifier.most_informative_features(n)


if __name__ == "__main__":
    gp = LevelClassifier()
    accuracy = gp.train_and_test()
    print('Accuracy: %f' % accuracy)
    print('Most Informative Features')
    feats = gp.get_most_informative_features(10)
    # get current datetime as index of case
    disNo = datetime.now().strftime("%m/%d/%Y-%H:%M:%S")

    print("Enter an instance of disaster case: ")
    year = int(input('Year: '))
    subtype = str(input('Subtype of disaster: '))
    country = str(input('Country: '))
    region = str(input('Region: '))
    startMonth = int(input('Start Month: '))
    endMonth = int(input('End Month (presumed): '))
    case = Case.CaseOfDisaster(disNo=disNo, year=year, subtype=subtype, country=country,
                               region=region, startMonth=startMonth, endMonth=endMonth)

    print('\n%s is classified as %s' % (case, gp.classify(case)))
