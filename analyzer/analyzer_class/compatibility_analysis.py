from analyzer.analyzer_class.thesaurus import Thesaurus


class CalculateTheProbability(object):
    def __call__(self, one_keys, two_keys):
        common_keywords = []
        for word in two_keys:
            if word in one_keys:
                common_keywords.append(word)
        results = round(len(common_keywords) / len(two_keys)*100)
        return results


class CompatibilityAnalysis(object):
    def __init__(self):
        self.thesaurus = Thesaurus()
        self.calculate_the_probability = CalculateTheProbability()

    def __call__(self, one_text_area, two_text_area,
                 one_uploaded_file, two_uploaded_file):

        one_keys, one_data = self.get_thesaurus(one_uploaded_file, one_text_area)
        two_keys, two_data = self.get_thesaurus(two_uploaded_file, two_text_area)
        result = self.calculate_the_probability(one_keys, two_keys)

        return one_data, two_data, result

    def get_thesaurus(self, uploaded_file, text_field):
        if uploaded_file is not None:
            keys, zip_data = self.thesaurus(text=uploaded_file)
        else:
            keys, zip_data = self.thesaurus(text=text_field)
        return keys, zip_data
