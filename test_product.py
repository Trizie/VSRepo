import unittest
from unittest.mock import patch

from mock_db import MockDB
from product import Product


class TestProduct(MockDB):
    def test_get_productName(self):
        with patch.object(Product, "__init__", lambda x, y: None):
            testObject = Product(None)
            testObject.barcode = "4015533041525"
            self.assertEqual(testObject.get_productName(), "Haferdrink")

    #def test_get_amount_from_DB(self):
    #with patch.object(Product, "__init__", lambda x, y: None):
    #testObject = Product(None)
    #testObject.barcode = 815
    # with self.mock_db_config:
    #self.assertEqual(testObject.get_amount_from_DB(), 7)

    def test_check_DB_contains_barcode(self):

        with patch.object(Product, "__init__", lambda x, y: None):
            testObject = Product(None)
            testObject.barcode = 815
        with self.mock_db_config:
            self.assertEqual(testObject.check_DB_contains_barcode(), "True")

    def test_add_product_to_DB(self):
        with patch.object(Product, "__init__", lambda x, y: None):
            testObject = Product(None)
            testObject.barcode = 150
            testObject.amount = 1
        with self.mock_db_config:
            self.assertEqual(testObject.add_product_to_DB("Banana"), "True")

    def test_check_delete(self):
        self.assertEqual(Product.check_delete(1, "true"), True)
        self.assertEqual(Product.check_delete(1, "false"), False)

    @patch("product.Product.get_amount_from_DB")
    def test_delete_product_from_DB(self, mock_get_amount_from_DB):
        mock_get_amount_from_DB.return_value = 1

        with patch.object(Product, "__init__", lambda x, y: None):
            testObject = Product(None)
            testObject.barcode = 815

        with self.mock_db_config:
            self.assertEqual(testObject.delete_product_from_DB(), "True")

    @patch("product.Product.get_amount_from_DB")
    def test_raise_amount_of_product_in_DB(self, mock_get_amount_from_DB):
        mock_get_amount_from_DB.return_value = 1

        with patch.object(Product, "__init__", lambda x, y: None):
            testObject = Product(None)
            testObject.barcode = 200

        with self.mock_db_config:
            self.assertEqual(testObject.raise_amount_of_product_in_DB(), "True")

    @patch("product.Product.get_amount_from_DB")
    def test_decrease_amount_of_product_in_DB(self, mock_get_amount_from_DB):
        mock_get_amount_from_DB.return_value = 1
        with patch.object(Product, "__init__", lambda x, y: None):
            testObject = Product(None)
            testObject.barcode = 200
        with self.mock_db_config:
            self.assertEqual(testObject.decrease_amount_of_product_in_DB(), "True")


if __name__ == "__main__":
    unittest.main()
