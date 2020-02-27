import unittest
from util.attributes_retrieval import *

class TestSum(unittest.TestCase):

    def test_get_max_page_for_letter(self):
        self.assertEqual(get_max_page_for_letter('a'), 24) # test case 1

        self.assertEqual(get_max_page_for_letter('x'), 1) # test case 2 (no total # pages displayed)

    def test_get_geo_coord(self):
        self.assertEqual(get_geo_coord("https://www.world-airport-codes.com/united-states/x-bar-1-ranch-lower-58940.html"), "35.3483009338379,-113.689002990723") # test case 1

        self.assertEqual(get_geo_coord("http://www.google.com"), None) # test case 2 (geolocation cannot be found)

    def test_get_zip_code_by_geopy(self):
        self.assertEqual(get_zip_code_by_geopy("35.3483009, -113.689003"), "86411") # test case 1

        self.assertEqual(get_zip_code_by_geopy("30.7271004, -91.1485977"), None) # test case 2 (cannot be found)

    def test_get_zip_code(self):
        self.assertEqual(get_zip_code("35.3483009, -113.689003"), "86411") # test case 1

        self.assertEqual(get_zip_code("68.7218018, -52.7846985"), "3950") # test case 2 (can only be found through geopy)

        self.assertEqual(get_zip_code("60.1483571, -44.2869186"), None) # test case 3 (cannot be found anyway)

    def test_get_attrs(self):
        self.assertEqual(get_attrs("https://www.world-airport-codes.com/alphabetical/airport-name/a.html?page=24"), [['Azua', 'Azua', 'Dominican Republic', '71000'],
                          ['Azul', 'Azul', 'Argentina', 'B7300'],
                          ['Azur', 'Dax', 'France', '40550']]) # test case 1

if __name__ == '__main__':
    unittest.main()
