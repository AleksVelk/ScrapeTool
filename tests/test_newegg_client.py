import os
import unittest

from scrapingtool.neweggclient import NewEggClient


class TestNewEggClient(unittest.TestCase):

    def test_calculate_last_page_to_extract(self):
        # Test that the last page to extract is calculated correctly
        client = NewEggClient(no_of_products=100)
        last_page = client.calculate_last_page_to_extract()
        self.assertEqual(last_page, 2)

    def test_get_products(self):
        # Test that the get_products method returns a list of products
        client = NewEggClient(no_of_products=500)
        products = client.get_products()
        self.assertIsInstance(products, list)
        self.assertGreaterEqual(len(products), 500)

    def test_get_items_details(self):
        # Test that the get_items_details method returns a list of products with relevant data points
        client = NewEggClient(no_of_products=500)
        products = client.get_products()
        item_details = client.get_items_details(products)
        self.assertIsInstance(item_details, list)
        self.assertGreaterEqual(len(item_details), 500)

    def test_save_to_csv(self):
        # Test that the method saves data to a CSV file
        client = NewEggClient()
        products = [{'product_title': 'item1', 'line_description': 'item1_line_description',
                     'bullet_description': 'item1_bullet_description'},
                    {'product_title': 'item2', 'line_description': 'item2_line_description',
                     'bullet_description': 'item2_bullet_description'}]
        file_name = "test_products_100"
        path = f"src/scraping_tool/data_files/{file_name}.csv"
        client.save_to_csv(products, file_name)
        self.assertTrue(os.path.exists(path))
        os.remove(path)

    def test_extract_save_products(self):
        # Test that the method correctly extracts and saves products
        file_name = "test_extract_save_products100"
        path = f"src/scraping_tool/data_files/{file_name}.csv"
        client = NewEggClient(no_of_products=100, file_name=file_name)
        client.extract_save_products()
        self.assertTrue(os.path.exists(path))
        os.remove(path)
