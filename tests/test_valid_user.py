import random
import unittest
import logging
from main import create_new_user, generate_token, is_authorized, delete_user, add_book, get_books, get_book, remove_book_from_collection, get_user_info, replace_book_in_collection


class Test(unittest.TestCase):
    user_id = ""
    bearerToken = ""
    username = "validUser"
    password = "Password123!"
    isbn = "9781449325862"
    isbn_random1 = ""
    isbn_random2 = ""
    available_books = []

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="test_valid_user.log"
    )

    @classmethod
    def setUpClass(self):
        """
        Create new valid user
        Set userId and Bearer token
        """
        logging.info("SetUpClass: \n"
                     f"username:    {self.username} \n"
                     f"password:    {self.password} \n")

        response = create_new_user(self.username, self.password)
        message = response.json()

        self.user_id = message["userID"]

        logging.info("Valid User was registered \n"
                     f"userId:      {self.user_id}")

        """ 
        Generate Token
        """
        response = generate_token(self.username, self.password)
        message = response.json()

        self.bearerToken = message["token"]

        logging.info("Generate Token! \n"
                     f"token:    {self.bearerToken}")

        """
        Initialize book list
        """
        response = get_books()
        books = response.json()["books"]
        [self.available_books.append(book["isbn"]) for book in books]

        self.available_books.remove("9781449325862")

        """
        Choose random isbn
        """
        self.isbn_random1 = random.choice(self.available_books)
        self.available_books.remove(self.isbn_random1)

        self.isbn_random2 = random.choice(self.available_books)
        self.available_books.remove(self.isbn_random2)

        logging.info("Initializing book list and chosen isbns")
        logging.info('\n')

    @classmethod
    def tearDownClass(self):

        response = delete_user(self.user_id, self.username, self.password)
        status_code = response.status_code

        logging.info(f"TearDownClass: {status_code} "
                     f"Deleted user with: \n"
                     f"username     {self.username} \n"
                     f"password     {self.password} \n"
                     f"userId:      {self.user_id} \n")

    def test_user_registered(self):
        """
        Test new user was registered successfully
        """
        logging.info("Starting test - check if user is registered")
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code

            self.assertNotEqual(201, status_code)

            logging.info("Success, User exists!")
            logging.info('\n')
        except AssertionError:
            logging.error("Error, User does Not exist, but should!")
            logging.error('\n')
            raise

    def test_user_authorized(self):
        """
        Check if user was authorized successfully
        """
        logging.info("Starting test - check if user was authorized")

        try:
            response = is_authorized(self.username, self.password)
            status_code = response.status_code
            message = response.json()
            print(message)
            self.assertEqual(200, status_code)
            self.assertEqual(True, message)

            logging.info("Success, user is authorized!")
            logging.info('\n')
        except AssertionError:
            logging.error("Error, user is Not authorized!")
            logging.error('\n')
            raise

    def test_add_new_book(self):
        """
        Test adding a new book to user collection
        """
        logging.info("Starting test - adding book to collection")

        collection_isbns = [
            {
                "isbn": self.isbn
            }
        ]
        try:
            response = add_book(self.user_id, collection_isbns, self.bearerToken)
            status_code = response.status_code

            self.assertEqual(201, status_code)

        except AssertionError:
            logging.error("Error in test add valid book to collection")
            raise

        """
        Test book has been added
        """
        try:
            response = get_user_info(self.user_id, self.bearerToken)
            status_code = response.status_code

            message = response.json()

            self.assertEqual(200, status_code)

            books = message["books"]
            user_collection = []
            [user_collection.append(book["isbn"]) for book in books]

            self.assertEqual(True, self.isbn in user_collection)

            logging.info("Successfully added book with valid ISBN to collection!\n")
        except AssertionError:
            logging.error("Error, looking for book in user collection!")
            logging.error('\n')
            raise

        response = get_user_info(self.user_id, self.bearerToken)
        message = response.json()

        books = message["books"]
        user_collection = []
        [user_collection.append(book["isbn"]) for book in books]
        logging.info(f"\n"
                     f"username:    {self.username}\n"
                     f"books:       {user_collection}\n")

    def test_add_random_book(self):
        """
        Test adding a new book to user collection chosen randomly
        """
        logging.info("Starting test - add random book to collection")

        collection_isbns = [
            {
                "isbn": self.isbn_random1
            },
            {
                "isbn": self.isbn_random2
            }
        ]
        try:
            response = add_book(self.user_id, collection_isbns, self.bearerToken)

            self.assertEqual(response.status_code, 201)
        except AssertionError:
            logging.error("Error in test add valid book to collection")
            raise

        """
        Test book has been added
        """
        try:
            response = get_user_info(self.user_id, self.bearerToken)
            status_code = response.status_code

            message = response.json()

            self.assertEqual(200, status_code)

            books = message["books"]
            user_collection = []
            [user_collection.append(book["isbn"]) for book in books]

            self.assertEqual(True, self.isbn_random1 in user_collection)
            self.assertEqual(True, self.isbn_random2 in user_collection)

            logging.info("Successfully added book with valid ISBN to collection!\n")
        except AssertionError:
            logging.error("Error, looking for book in user collection!")
            logging.error('\n')
            raise

        response = get_user_info(self.user_id, self.bearerToken)
        message = response.json()

        books = message["books"]
        user_collection = []
        [user_collection.append(book["isbn"]) for book in books]
        logging.info(f"\n"
                     f"username:    {self.username}\n"
                     f"books:       {user_collection}\n")

    def test_switch_book(self):
        """
        Test changing the first book in collection with another one
        """
        logging.info("Starting test - switching the first book in collection with another one from the store")

        isbn_not_in_collection = random.choice(self.available_books)
        self.available_books.remove(isbn_not_in_collection)

        response = get_user_info(self.user_id, self.bearerToken)
        message = response.json()

        books = message["books"]
        user_collection = []
        [user_collection.append(book["isbn"]) for book in books]

        replace_isbn = user_collection[0]

        try:
            response = replace_book_in_collection(self.user_id, self.bearerToken, replace_isbn, isbn_not_in_collection)
            status_code = response.status_code

            self.assertEqual(200, status_code)

            message = response.json()
            books = message["books"]
            user_collection = []
            [user_collection.append(book["isbn"]) for book in books]

            self.assertEqual(True, isbn_not_in_collection in user_collection)
            self.assertEqual(False, replace_isbn in user_collection)

            self.available_books.append(replace_isbn)

            logging.info(f"Book with isbn: {replace_isbn} successfully replaced by book with isbn: {isbn_not_in_collection}")
            logging.info('\n')
        except AssertionError:
            logging.error("Book replacement failed!")
            logging.error('\n')
            raise

        response = get_user_info(self.user_id, self.bearerToken)
        message = response.json()

        books = message["books"]
        user_collection = []
        [user_collection.append(book["isbn"]) for book in books]
        logging.info(f"\n"
                     f"username:    {self.username}\n"
                     f"books:       {user_collection}\n")

    def test_add_new_non_existing_book(self):
        """
        Test adding with invalid isbn
        """
        logging.info("Starting test - try to add a non-existing book to collection")

        collection_isbns = [
            {
                "isbn": "1"
            }
        ]
        try:
            response = add_book(self.user_id, collection_isbns, self.bearerToken)

            self.assertEqual(response.status_code, 400)
            logging.info("Success, Invalid ISBN was not accepted!\n")

        except AssertionError:
            logging.error("Error, invalid isbn was accepted")
            logging.error('\n')
            raise

        response = get_user_info(self.user_id, self.bearerToken)
        message = response.json()

        books = message["books"]
        user_collection = []
        [user_collection.append(book["isbn"]) for book in books]
        logging.info(f"\n"
                     f"username:    {self.username}\n"
                     f"books:       {user_collection}\n")

    def test_book_exists_by_isbn(self):
        """
        Check if book with isbn: 9781491904244, has 278 pages
        """
        logging.info("Starting test - check if book with isbn: 9781491904244 has 278 pages")

        try:
            response = get_book('9781491904244')
            status_code = response.status_code

            self.assertEqual(status_code, 200)

            message = response.json()

            self.assertEqual(message['pages'], 278)

            logging.info("Success, Book with isbn: 9781491904244, has 278 pages!")
            logging.info('\n')
        except AssertionError:
            logging.error("Error - Book with isbn: 9781491904244, does Not have 278 pages!")
            logging.error('\n')
            raise

        response = get_user_info(self.user_id, self.bearerToken)
        message = response.json()

        books = message["books"]
        user_collection = []
        [user_collection.append(book["isbn"]) for book in books]
        logging.info(f"\n"
                     f"username:    {self.username}\n"
                     f"books:       {user_collection}\n")

    def test_remove_book_from_collection(self):
        """
        Remove Book from collection
        """
        logging.info("Starting test - remove book from collection")

        response = get_user_info(self.user_id, self.bearerToken)
        message = response.json()

        books = message["books"]
        user_collection = []
        [user_collection.append(book["isbn"]) for book in books]

        isbn_to_remove = random.choice(user_collection)

        try:
            response = remove_book_from_collection(self.user_id, isbn_to_remove, self.bearerToken)
            status_code = response.status_code

            self.assertEqual(204, status_code)

        except AssertionError:
            logging.error(f"Error - Book with isbn: {self.isbn} was Not removed from collection!")
            logging.error('\n')
            raise

        """
        Test book has been removed
        """
        try:
            response = get_user_info(self.user_id, self.bearerToken)
            status_code = response.status_code

            message = response.json()

            self.assertEqual(200, status_code)

            books = message["books"]
            user_collection = []
            [user_collection.append(book["isbn"]) for book in books]

            self.assertEqual(False, isbn_to_remove in user_collection)

            self.available_books.append(isbn_to_remove)

            logging.info(f"Book with isbn: {isbn_to_remove} was removed from collection")
            logging.info('\n')
        except AssertionError:
            logging.error(f"Error - Book with isbn: {isbn_to_remove} was Not removed from collection!")
            logging.error('\n')
            raise

        response = get_user_info(self.user_id, self.bearerToken)
        message = response.json()

        books = message["books"]
        user_collection = []
        [user_collection.append(book["isbn"]) for book in books]
        logging.info(f"\n"
                     f"username:    {self.username}\n"
                     f"books:       {user_collection}\n")

    def test_remove_book_not_in_collection_(self):
        """
        Remove Book not in collection
        """
        logging.info("Starting test - try to remove a book not in collection")

        isbn_not_in_collection = random.choice(self.available_books)

        try:
            response = remove_book_from_collection(self.user_id, isbn_not_in_collection, self.bearerToken)
            status_code = response.status_code

            self.assertEqual(400, status_code)

            logging.info(f"Success, Book with isbn: {isbn_not_in_collection} not in collection")
            logging.info('\n')
        except AssertionError:
            logging.error(f"Error - Book with isbn: {isbn_not_in_collection} should not be in collection!")
            logging.error('\n')
            raise

        response = get_user_info(self.user_id, self.bearerToken)
        message = response.json()

        books = message["books"]
        user_collection = []
        [user_collection.append(book["isbn"]) for book in books]
        logging.info(f"\n"
                     f"username:    {self.username}\n"
                     f"books:       {user_collection}\n")