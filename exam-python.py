#Variant 3

from datetime import datetime
from typing import List, Dict, Any
import json
from abc import ABC, abstractmethod

from datetime import datetime
from typing import List, Dict, Any
import json
from abc import ABC, abstractmethod


class Employee:
    def __init__(self, full_name: str, position: str, phone: str, email: str):
        self.full_name = full_name
        self.position = position
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"Employee(Name: {self.full_name}, Position: {self.position}, Phone: {self.phone}, Email: {self.email})"


class Book:
    def __init__(self, title: str, year: int, author: str, genre: str, cost_price: float, potential_sale_price: float):
        self.title = title
        self.year = year
        self.author = author
        self.genre = genre
        self.cost_price = cost_price
        self.potential_sale_price = potential_sale_price

    def __str__(self):
        return f"Book(Title: {self.title}, Year: {self.year}, Author: {self.author}, Genre: {self.genre}, Cost: {self.cost_price}, Sale Price: {self.potential_sale_price})"


class Sale:
    def __init__(self, employee: Employee, book: Book, sale_date: datetime, real_sale_price: float):
        self.employee = employee
        self.book = book
        self.sale_date = sale_date
        self.real_sale_price = real_sale_price

    def __str__(self):
        return f"Sale(Employee: {self.employee.full_name}, Book: {self.book.title}, Date: {self.sale_date}, Sale Price: {self.real_sale_price})"


class BookStore:
    def __init__(self):
        self.employees: List[Employee] = []
        self.books: List[Book] = []
        self.sales: List[Sale] = []

    def add_employee(self, employee: Employee):
        self.employees.append(employee)

    def remove_employee(self, employee: Employee):
        self.employees.remove(employee)

    def add_book(self, book: Book):
        self.books.append(book)

    def remove_book(self, book: Book):
        self.books.remove(book)

    def add_sale(self, sale: Sale):
        self.sales.append(sale)

    def remove_sale(self, sale: Sale):
        self.sales.remove(sale)

    def generate_report(self, report_type: str, params: Dict[str, Any]) -> str:
        if report_type == "employees":
            strategy = EmployeeReportStrategy()
            return strategy.generate(self.employees, params)
        elif report_type == "books":
            strategy = BookReportStrategy()
            return strategy.generate(self.books, params)
        elif report_type == "sales":
            strategy = SaleReportStrategy()
            return strategy.generate(self.sales, params)
        elif report_type == "sales_by_date":
            strategy = SalesByDateReportStrategy()
            return strategy.generate(self.sales, params)
        return "Unknown report type"

    def save_to_file(self, file_path: str):
        data = {
            "employees": [e.__dict__ for e in self.employees],
            "books": [b.__dict__ for b in self.books],
            "sales": [
                {
                    "employee": s.employee.__dict__,
                    "book": s.book.__dict__,
                    "sale_date": s.sale_date.isoformat(),
                    "real_sale_price": s.real_sale_price
                }
                for s in self.sales
            ]
        }
        with open(file_path, 'w') as file:
            json.dump(data, file)
        print("Data saved to file.")

    def load_from_file(self, file_path: str):
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.employees = [Employee(**e) for e in data['employees']]
            self.books = [Book(**b) for b in data['books']]
            self.sales = [
                Sale(
                    Employee(**s['employee']),
                    Book(**s['book']),
                    datetime.fromisoformat(s['sale_date']),
                    s['real_sale_price']
                )
                for s in data['sales']
            ]
        print("Data loaded from file.")


class BookStoreFactory:
    @staticmethod
    def create_employee(full_name: str, position: str, phone: str, email: str) -> Employee:
        return Employee(full_name, position, phone, email)

    @staticmethod
    def create_book(title: str, year: int, author: str, genre: str, cost_price: float,
                    potential_sale_price: float) -> Book:
        return Book(title, year, author, genre, cost_price, potential_sale_price)

    @staticmethod
    def create_sale(employee: Employee, book: Book, sale_date: datetime, real_sale_price: float) -> Sale:
        return Sale(employee, book, sale_date, real_sale_price)


class ReportStrategy(ABC):
    @abstractmethod
    def generate(self, data: Any, params: Dict[str, Any]) -> str:
        pass


class EmployeeReportStrategy(ReportStrategy):
    def generate(self, data: List[Employee], params: Dict[str, Any]) -> str:
        return "\n".join(str(employee) for employee in data)


class BookReportStrategy(ReportStrategy):
    def generate(self, data: List[Book], params: Dict[str, Any]) -> str:
        return "\n".join(str(book) for book in data)


class SaleReportStrategy(ReportStrategy):
    def generate(self, data: List[Sale], params: Dict[str, Any]) -> str:
        return "\n".join(str(sale) for sale in data)


class SalesByDateReportStrategy(ReportStrategy):
    def generate(self, data: List[Sale], params: Dict[str, Any]) -> str:
        date = params.get("date")
        return "\n".join(str(sale) for sale in data if sale.sale_date.date() == date)


class Menu:
    def __init__(self, bookstore: BookStore):
        self.bookstore = bookstore

    def display_options(self, options: List[str]):
        print("Меню:")
        for idx, option in enumerate(options, start=1):
            print(f"{idx}. {option}")

    def get_user_choice(self, options: List[str]) -> int:
        choice = -1
        while choice < 1 or choice > len(options):
            try:
                choice = int(input("Виберіть опцію: "))
            except ValueError:
                print("Будь ласка, введіть ціле число.")
            if choice < 1 or choice > len(options):
                print("Невірний вибір. Спробуйте ще раз.")
        return choice

    def run(self):
        options = [
            "Додати працівника",
            "Видалити працівника",
            "Додати книгу",
            "Видалити книгу",
            "Додати продаж",
            "Видалити продаж",
            "Згенерувати звіт",
            "Зберегти до файлу",
            "Завантажити з файлу",
            "Вихід"
        ]

        while True:
            self.display_options(options)
            choice = self.get_user_choice(options)

            if choice == 1:
                self.add_employee()
            elif choice == 2:
                self.remove_employee()
            elif choice == 3:
                self.add_book()
            elif choice == 4:
                self.remove_book()
            elif choice == 5:
                self.add_sale()
            elif choice == 6:
                self.remove_sale()
            elif choice == 7:
                self.generate_report()
            elif choice == 8:
                self.save_to_file()
            elif choice == 9:
                self.load_from_file()
            elif choice == 10:
                print("До побачення!")
                break

    def add_employee(self):
        full_name = input("Введіть П.І.Б.: ")
        position = input("Введіть посаду: ")
        phone = input("Введіть контактний телефон: ")
        email = input("Введіть email: ")
        employee = BookStoreFactory.create_employee(full_name, position, phone, email)
        self.bookstore.add_employee(employee)
        print("Працівника додано.")

    def remove_employee(self):
        full_name = input("Введіть П.І.Б. працівника, якого бажаєте видалити: ")
        employee = next((e for e in self.bookstore.employees if e.full_name == full_name), None)
        if employee:
            self.bookstore.remove_employee(employee)
            print("Працівника видалено.")
        else:
            print("Працівника не знайдено.")

    def add_book(self):
        title = input("Введіть назву книги: ")
        year = int(input("Введіть рік видання: "))
        author = input("Введіть автора: ")
        genre = input("Введіть жанр: ")
        cost_price = float(input("Введіть собівартість: "))
        potential_sale_price = float(input("Введіть потенційну ціну продажу: "))
        book = BookStoreFactory.create_book(title, year, author, genre, cost_price, potential_sale_price)
        self.bookstore.add_book(book)
        print("Книгу додано.")

    def remove_book(self):
        title = input("Введіть назву книги, яку бажаєте видалити: ")
        book = next((b for b in self.bookstore.books if b.title == title), None)
        if book:
            self.bookstore.remove_book(book)
            print("Книгу видалено.")
        else:
            print("Книгу не знайдено.")

    def add_sale(self):
        full_name = input("Введіть П.І.Б. працівника: ")
        employee = next((e for e in self.bookstore.employees if e.full_name == full_name), None)
        if not employee:
            print("Працівника не знайдено.")
            return

        title = input("Введіть назву книги: ")
        book = next((b for b in self.bookstore.books if b.title == title), None)
        if not book:
            print("Книгу не знайдено.")
            return

        sale_date = datetime.now()
        real_sale_price = float(input("Введіть реальну ціну продажу: "))
        sale = BookStoreFactory.create_sale(employee, book, sale_date, real_sale_price)
        self.bookstore.add_sale(sale)
        print("Продаж додано.")

    def remove_sale(self):
        title = input("Введіть назву книги, продаж якої бажаєте видалити: ")
        sale = next((s for s in self.bookstore.sales if s.book.title == title), None)
        if sale:
            self.bookstore.remove_sale(sale)
            print("Продаж видалено.")
        else:
            print("Продаж не знайдено.")

    def generate_report(self):
        report_type = input("Введіть тип звіту: ")
        params = {}
        report = self.bookstore.generate_report(report_type, params)
        print(report)

    def save_to_file(self):
        file_path = input("Введіть шлях до файлу для збереження: ")
        self.bookstore.save_to_file(file_path)
        print("Дані збережено.")

    def load_from_file(self):
        file_path = input("Введіть шлях до файлу для завантаження: ")
        self.bookstore.load_from_file(file_path)
        print("Дані завантажено.")


if __name__ == "__main__":
    bookstore = BookStore()
    menu = Menu(bookstore)
    menu.run()

