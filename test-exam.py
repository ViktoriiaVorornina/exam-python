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


if __name__ == '__main__':
    unittest.main()

