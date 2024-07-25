import unittest
from unittest.mock import patch

from dbclass import DBclass
from product import Product


class TestProduct(unittest.TestCase):
    def test_get_productName(self):
        with patch.object(Product, "__init__", lambda x, y: None):
            # pylint: disable = no-value-for-parameter
            testObject = Product(None)
            testObject.barcode = "4015533041525"
            self.assertEqual(testObject.get_productName(), "Haferdrink")

    def test_get_productCategory(self):
        with patch.object(Product, "__init__", lambda x, y: None):
            # pylint: disable = no-value-for-parameter
            testObject = Product(None)
            testObject.barcode = "4388810057817"
            list = "Getränke, Wasser, Quellwasser, Mineralwasser, Alkoholfreie Getränke, Natürliches Mineralwasser"
            self.assertEqual(testObject.get_productCategory(), list)

    @patch.object(DBclass, "select_query")
    def test_get_amount_from_DB(self, mock_select_query):
        with patch.object(Product, "__init__", lambda x, y: None):
            # pylint: disable = no-value-for-parameter
            testObject = Product(None)
            testObject.barcode = 100
        mock_select_query.return_value = [(5,)]
        self.assertEqual(testObject.get_amount_from_DB(), 5)

    @patch.object(DBclass, "select_query")
    def test_check_DB_contains_barcode(self, mock_select_query):
        with patch.object(Product, "__init__", lambda x, y: None):
            # pylint: disable = no-value-for-parameter
            testObject = Product(None)
            testObject.barcode = 200
        mock_select_query.return_value = []
        self.assertEqual(testObject.check_DB_contains_barcode(), "False")
        mock_select_query.return_value = 1234567
        self.assertEqual(testObject.check_DB_contains_barcode(), "True")

    @patch.object(DBclass, "insert_query")
    def test_add_product_to_DB(self, mock_insert_query):
        with patch.object(Product, "__init__", lambda x, y: None):
            # pylint: disable = no-value-for-parameter
            testObject = Product(None)
            testObject.barcode = 110
            testObject.amount = 1
            self.assertEqual(
                testObject.add_product_to_DB("Banana", "Testkategorie_3"), "True"
            )

    def test_check_delete(self):
        self.assertEqual(Product.check_delete(1, "true"), True)
        self.assertEqual(Product.check_delete(1, "false"), False)

    @patch.object(DBclass, "delete_query")
    @patch("product.Product.get_amount_from_DB")
    def test_delete_product_from_DB(self, mock_get_amount_from_DB, mock_delete_query):
        mock_get_amount_from_DB.return_value = 1
        with patch.object(Product, "__init__", lambda x, y: None):
            # pylint: disable = no-value-for-parameter
            testObject = Product(None)
            testObject.barcode = 815
            self.assertEqual(testObject.delete_product_from_DB(), "True")

    @patch.object(DBclass, "insert_query")
    @patch("product.Product.get_amount_from_DB")
    def test_raise_amount_of_product_in_DB(
        self, mock_get_amount_from_DB, mock_insert_query
    ):
        mock_get_amount_from_DB.return_value = 1
        with patch.object(Product, "__init__", lambda x, y: None):
            # pylint: disable = no-value-for-parameter
            testObject = Product(None)
            testObject.barcode = 200
            self.assertEqual(testObject.raise_amount_of_product_in_DB(), "True")

    @patch.object(DBclass, "insert_query")
    @patch("product.Product.get_amount_from_DB")
    def test_decrease_amount_of_product_in_DB(
        self, mock_get_amount_from_DB, mock_insert_query
    ):
        mock_get_amount_from_DB.return_value = 3
        with patch.object(Product, "__init__", lambda x, y: None):
            # pylint: disable = no-value-for-parameter
            testObject = Product(None)
            testObject.barcode = 200
            self.assertEqual(testObject.raise_amount_of_product_in_DB(), "True")


if __name__ == "__main__":
    unittest.main()
