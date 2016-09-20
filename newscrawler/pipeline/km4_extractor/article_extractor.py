from newscrawler.pipeline.km4_extractor.cleaner import Cleaner
from newscrawler.pipeline.km4_extractor.comparer.comparer import Comparer


class Extractor:
    """This class initializes all extractors and saves the results of them. When adding a new extractor, it needs to
    be initialized here and added to list_extractor.
    """

    def __init__(self, extractor_list):
        """Initializes all the extractors, comparers and the cleaner.

        :param extractor_list: List of strings containing all extractors to be initialized.
        """

        self.extractor_list = []
        for extractor in extractor_list:
            self.extractor_list.append(getattr(extractor, None))

        self.cleaner = Cleaner()
        self.comparer = Comparer()

    def extract(self, item):
        """Runs the HTML-response trough a list of initialized extractors, a cleaner and compares the results.

        :param item: NewscrawlerItem to be processed.
        :return: An updated NewscrawlerItem including the results of the extraction
        """

        article_candidates = []

        for extractor in self.extractor_list:
            article_candidates.append(extractor.extract(item))

        article_candidates = self.cleaner.clean(article_candidates)
        article = self.comparer.compare(article_candidates)

        item['article_title'] = article.title
        item['article_description'] = article.description
        item['article_text'] = article.text
        item['article_image'] = article.topimage
        item['article_author'] = article.author
        item['article_publish_date'] = article.publish_date
        item['article_language'] = article.language

        return item
