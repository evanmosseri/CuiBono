from scripts.scraping import scrape_politican
import unittest

class TestScrapingFunctions(unittest.TestCase):
	def test_cookie_retrieval(self):
		self.assertIsNotNone(scrape_politican.get_simple_search_cookie())
	def test_politician_retrieval(self):
		self.assertEqual(
			scrape_politican.get_filer_info("kirk","watson"),
			[{'id': '00023391', 'type': 'COH', 'name': 'Kirk P. Watson', 'state': 'TX', 'city': 'Austin'}]
		)


if __name__ == '__main__':
    unittest.main()