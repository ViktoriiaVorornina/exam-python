import unittest
from datetime import datetime
from exampython import Employee, Book, Sale, BookStore, BookStoreFactory

class TestBookStore(unittest.TestCase):
    def setUp(self):
        self.bookstore = BookStore()

        self.employee1 = BookStoreFactory.create_employee("Вікторія Вороніна", "Менеджер", "987654321", "voorninaw@gmail.com")

        self.book2 = BookStoreFactory.create_book("Кобзар", 1840, "Тарас Шевченко", "Поезія", 150.0, 250.0)
        self.book3 = BookStoreFactory.create_book("Тіні забутих предків", 1911, "Михайло Коцюбинський", "Повість",
                                                  120.0, 180.0)
        self.book4 = BookStoreFactory.create_book("Собор", 1968, "Олесь Гончар", "Роман", 170.0, 270.0)
        self.book5 = BookStoreFactory.create_book("Чорний Ворон", 2009, "Василь Шкляр", "Роман", 200.0, 350.0)

        self.sale1 = BookStoreFactory.create_sale(self.employee1, self.book2, datetime.now(), 290.0)
        self.sale2 = BookStoreFactory.create_sale(self.employee1, self.book2, datetime.now(), 240.0)
        self.sale3 = BookStoreFactory.create_sale(self.employee1, self.book3, datetime.now(), 170.0)
        self.sale4 = BookStoreFactory.create_sale(self.employee1, self.book4, datetime.now(), 260.0)
        self.sale5 = BookStoreFactory.create_sale(self.employee1, self.book5, datetime.now(), 340.0)

    def test_add_employee(self):
        self.bookstore.add_employee(self.employee1)
        self.assertIn(self.employee1, self.bookstore.employees)

    def test_remove_employee(self):
        self.bookstore.add_employee(self.employee1)
        self.bookstore.remove_employee(self.employee1)
        self.assertNotIn(self.employee1, self.bookstore.employees)

    def test_add_book(self):
        self.bookstore.add_book(self.book2)
        self.assertIn(self.book2, self.bookstore.books)

    def test_remove_book(self):
        self.bookstore.add_book(self.book2)
        self.bookstore.remove_book(self.book2)
        self.assertNotIn(self.book2, self.bookstore.books)

    def test_add_sale(self):
        self.bookstore.add_sale(self.sale1)
        self.assertIn(self.sale1, self.bookstore.sales)

    def test_remove_sale(self):
        self.bookstore.add_sale(self.sale1)
        self.bookstore.remove_sale(self.sale1)
        self.assertNotIn(self.sale1, self.bookstore.sales)

    def test_generate_employee_report(self):
        self.bookstore.add_employee(self.employee1)
        report = self.bookstore.generate_report("employees", {})
        self.assertIn("Вікторія Вороніна", report)

    def test_generate_book_report(self):
        self.bookstore.add_book(self.book3)
        report = self.bookstore.generate_report("books", {})
        self.assertIn("Тіні забутих предків", report)

    def test_generate_sale_report(self):
        self.bookstore.add_sale(self.sale3)
        report = self.bookstore.generate_report("sales", {})
        self.assertIn("Тіні забутих предків", report)

    def test_generate_sales_by_date_report(self):
        self.bookstore.add_sale(self.sale3)
        report = self.bookstore.generate_report("sales_by_date", {"date": datetime.now().date()})
        self.assertIn("Тіні забутих предків", report)


if __name__ == '__main__':
    unittest.main()

