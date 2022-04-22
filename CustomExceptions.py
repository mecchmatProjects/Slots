class SettingStateException(Exception):
    def __str__(self):
        return "invalid values for state massive: values in each row have to be distinct"


class SettingWinningCombinationsException(Exception):
    def __str__(self):
        return "invalid values for dict combinations:"


class CombinationLengthException(SettingWinningCombinationsException):
    def __str__(self):
        return super().__str__() + " key length of dict combinations have to equal number columns " \
                                   "of massive state in class OneHandBandit"


class CombinationValuesException(SettingWinningCombinationsException):
    def __str__(self):
        return super().__str__() + " key values of dict combinations have to be " \
                                   "lower than (picturesNumb - 1) in class OneHandBandit" \
                                   "and greater than 0"


class WinningMoneyException(SettingWinningCombinationsException):
    def __str__(self):
        return super().__str__() + " winning money have to be greater than 0"


class SettingProbabilities2PicturesException(Exception):
    def __str__(self):
        return "error when set the probabilities for pictures;"


class ProbabilitiesArrayLengthException(SettingProbabilities2PicturesException):
    def __str__(self):
        return super().__str__() + " probabilities array must be the same length as pictures array length"


class ProbabilitiesSumException(SettingProbabilities2PicturesException):
    def __str__(self):
        return super().__str__() + " probabilities array sum must equal 1"
