import unittest
import logging
from main import create_new_user, delete_user


class Test(unittest.TestCase):
    username = ""
    password = ""
    user_id = ""
    bearerToken = ""

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.FileHandler(filename="test_registration.log", encoding='utf-8')]
    )

    def tearDown(self):
        """
        Deleting successful registrations
        """
        logging.info(f"TearDown")

        """
        Check if the user you want to delete exists
        """
        response = delete_user(self.user_id, self.username, self.password)
        status_code = response.status_code

        if status_code == 204:
            logging.info(f"Response: {status_code} \n"
                         f"Deleted user with: \n"
                         f"username     {self.username} \n"
                         f"password     {self.password} \n"
                         f"userId:      {self.user_id} \n")

        else:
            logging.info("No need to delete an account \n")

    def test_user_exists(self):
        """
        Test registration with existing credentials
        """
        logging.info("Starting test registration with existing credentials")

        username = "existingUser"
        password = "ExistingUserPassword123!"

        logging.info(f"Testing with:\n"
                     f"username:     {self.username} \n"
                     f"password:     {self.password} \n")
        try:
            response = create_new_user(username, password)
            status_code = response.status_code

            self.assertNotEqual(201, status_code)

            logging.info("Success, couldn't register a new user with existing credentials!")
            logging.info('\n')
        except AssertionError:
            logging.error("Error in test with existing credentials! User does Not exist, but should!")
            logging.error('\n')
            raise

    def test_existing_username(self):
        """
        Test registration with existing username
        """
        logging.info("Starting test registration with existing username")

        self.username = "existingUser"
        self.password = "ExistingUser123!"

        logging.info(f"Testing with:\n"
                     f"username:     {self.username} \n"
                     f"password:     {self.password} \n")
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code
            message = response.json()

            self.assertEqual(201, status_code)

            self.user_id = message["userID"]

            logging.info("Success, repeat usernames are not restricted!")
            logging.info('\n')
        except AssertionError:
            logging.error("Error in test with existing username!")
            logging.error('\n')
            raise

    """ 
    Test registration with invalid password
    1.  Password without digits
    2.  Password too short
    3.  Password no uppercase
    4.  Password no lowercase
    5.  Password no special characters
    6.  Empty Password
    7.  Password other special characters
    """

    def test_password_no_digits(self):
        """
        1.  Password without digits
        """
        logging.info("Starting test registration with Password without digits")

        self.username = "invalidNewUser"
        self.password = "Password!"

        logging.info(f"Testing with:\n"
                     f"username:     {self.username} \n"
                     f"password:     {self.password} \n")
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code

            self.assertNotEqual(201, status_code)

            logging.info("Test successful. User was Not registered. Password has no digit!")
            logging.info('\n')
        except AssertionError:
            message = response.json()
            self.user_id = message["userId"]

            logging.error("Error in testing registration with a password with no digit!")
            logging.error('\n')
            raise

    def test_password_too_short(self):
        """
        2.  Password too short
        """
        logging.info("Starting test registration with short password")

        self.username = "invalidNewUser"
        self.password = "Pass12!"

        logging.info(f"Testing with:\n"
                     f"username:     {self.username} \n"
                     f"password:     {self.password} \n")
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code

            self.assertNotEqual(201, status_code)

            logging.info("Test successful. User was Not registered. Password is too short!")
            logging.info('\n')
        except AssertionError:
            message = response.json()
            self.user_id = message["userId"]

            logging.error("Error in testing registration with a short password!")
            logging.error('\n')
            raise

    def test_password_no_uppercase(self):
        """
        3.  Password no uppercase
        """
        logging.info("Starting test registration with password without uppercase letters")

        self.username = "invalidNewUser"
        self.password = "password123!"

        logging.info(f"Testing with:\n"
                     f"username:     {self.username} \n"
                     f"password:     {self.password} \n")
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code

            self.assertNotEqual(201, status_code)

            logging.info("Test successful. User was Not registered. Password with no uppercase letters!")
            logging.info('\n')
        except AssertionError:
            message = response.json()
            self.user_id = message["userId"]

            logging.error("Error in testing registration with a password with no uppercase letters!")
            logging.error('\n')
            raise

    def test_password_no_lowercase(self):
        """
        4.  Password no lowercase
        """
        logging.info("Starting test registration with password without lowercase letters")

        self.username = "invalidNewUser"
        self.password = "PASSWORD123!"

        logging.info(f"Testing with:\n"
                     f"username:     {self.username} \n"
                     f"password:     {self.password} \n")
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code

            self.assertNotEqual(201, status_code)

            logging.info("Test successful. User was Not registered. Password with no lowercase letters!")
            logging.info('\n')
        except AssertionError:
            message = response.json()
            self.user_id = message["userId"]

            logging.error("Error in testing registration with a password with no lowercase letters!")
            logging.error('\n')
            raise

    def test_password_no_special_char(self):
        """
        5.  Password no special characters
        """
        logging.info("Starting test registration with password without special characters")

        self.username = "invalidNewUser"
        self.password = "Password123"

        logging.info(f"Testing with:\n"
                     f"username:     {self.username} \n"
                     f"password:     {self.password} \n")
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code

            self.assertNotEqual(201, status_code)

            logging.info("Test successful. User was Not registered. Password with no special character!")
            logging.info('\n')
        except AssertionError:
            message = response.json()
            self.user_id = message["userId"]

            logging.error("Error in testing registration with a password with no special character!")
            logging.error('\n')
            raise

    def test_password_empty(self):
        """
        6.  Empty Password
        """
        logging.info("Starting test registration with empty password")

        self.username = "invalidNewUser"
        self.password = ""

        logging.info(f"Testing with:\n"
                     f"username:     {self.username} \n"
                     f"password:     {self.password} \n")
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code

            self.assertNotEqual(201, status_code)

            logging.info("Test successful. User was Not registered. Password is empty")
            logging.info('\n')
        except AssertionError:
            message = response.json()
            self.user_id = message["userId"]

            logging.error("Error in testing registration with empty password!")
            logging.error('\n')
            raise

    def test_password_other_special_char(self):
        """
        7.  Password with '()/+-*=_' as a special char
        """
        logging.info("Starting test registration with password with '()/+-*=_' as a special characters")

        self.username = "invalidNewUser"
        self.password = "Password123()/+-*=_"

        logging.info(f"Testing with:\n"
                     f"username:     {self.username} \n"
                     f"password:     {self.password} \n")
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code

            self.assertEqual(201, status_code)

            message = response.json()
            self.user_id = message["userId"]

            logging.info("Test successful. User was registered. Password with '()/+-*=_' as a special character!")
            logging.info('\n')
        except AssertionError:
            logging.error("Error in testing registration with a password with '()/+-*=_' as a special character!")
            logging.error('\n')
            raise

    """ 
    Test registration using other alphabet
    1.  Only cyrillic in username
    2.  Mixed latin-cyrillic in username
    3.  Only cyrillic in password
    4.  Mixed latin-cyrillic in password
    """

    def test_only_cyrillic_username(self):
        """
        1.  Check if cyrillic is accepted in username
        """
        logging.info("Starting test registration with username entirely in cyrillic")

        self.username = "валидноИме"
        self.password = "Password123!"

        logging.info(f"Testing with:\n"
                     f"username:     {self.username} \n"
                     f"password:     {self.password} \n")
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code
            message = response.json()

            self.assertEqual(201, status_code)
            self.assertIsNotNone(message["userID"])
            self.assertEqual(message["username"], self.username)
            self.assertEqual(len(message["books"]), 0)

            self.user_id = message["userID"]

            logging.info("Username in another alphabet is accepted!")
            logging.info('\n')
        except AssertionError:
            logging.error("Error in creating a valid new user using different alphabet in username!")
            logging.error('\n')
            raise

    def test_mixed_username(self):
        """
        2.  Check if mixed alphabet is accepted in username
        """
        logging.info("Starting test registration with username with mixed alphabets")

        self.username = "валидноUsername"
        self.password = "Password123!"

        logging.info(f"Testing with:\n"
                     f"username:     {self.username} \n"
                     f"password:     {self.password} \n")
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code
            message = response.json()

            self.assertEqual(201, status_code)
            self.assertIsNotNone(message["userID"])
            self.assertEqual(message["username"], self.username)
            self.assertEqual(len(message["books"]), 0)

            self.user_id = message["userID"]

            logging.info("Username in another alphabet is accepted!")
            logging.info('\n')
        except AssertionError:
            logging.error("Error in creating a valid new user using different alphabet in username!")
            logging.error('\n')
            raise

    def test_only_cyrillic_password(self):
        """
        3.  Check if only cyrillic is accepted in password
        """
        logging.info("Starting test registration with password entirely in cyrillic")

        self.username = "validUsername"
        self.password = "Парола123!"

        logging.info(f"Testing with:\n"
                     f"username:     {self.username} \n"
                     f"password:     {self.password} \n")
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code

            self.assertNotEqual(201, status_code)

            logging.info("Test successful. User was Not registered. Password has no [a-z,A-Z] letters")
            logging.info('\n')
        except AssertionError:
            message = response.json()
            self.user_id = message["userId"]

            logging.error("Error, a password without [a-z,A-Z] letters was accepted!")
            logging.error('\n')
            raise

    def test_mixed_password(self):
        """
        4.  Check mixed alphabets in password
        """
        logging.info("Starting test registration with password with mixed alphabet")

        self.username = "validUsername"
        self.password = "PasswordПарола123!"

        logging.info(f"Testing with:\n"
                     f"username:     {self.username} \n"
                     f"password:     {self.password} \n")
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code
            message = response.json()

            self.assertEqual(201, status_code)

            self.user_id = message["userID"]

            logging.info("Test successful. Password with mixed alphabets that conforms to requirements accepted!")
            logging.info('\n')
        except AssertionError:
            logging.error("Error in creating a valid new user using mixed alphabets in password!")
            logging.error('\n')
            raise

    def test_password_long(self):
        """
        Test a valid password that is really long
        """
        logging.info("Starting test registration with a long valid password")

        self.username = "invalidNewUser"
        self.password = "validPassword123!" * 20

        logging.info(f"Testing with:\n"
                     f"username:     {self.username} \n"
                     f"password:     {self.password} \n")
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code

            self.assertEqual(201, status_code)

            message = response.json()
            self.userId = message["userID"]

            message = response.json()
            self.user_id = message["userId"]

            logging.info("Long valid password accepted")
            logging.info('\n')
        except AssertionError:
            logging.error("Error in testing registration with a long password!")
            logging.error('\n')
            raise

    """ 
    Test registration with invalid username
    1.  Empty Username and empty password
    2.  Empty Username and valid password
    """

    def test_empty_username_empty_password(self):
        """
        1.  Empty Username and empty password
        """
        logging.info("Starting test registration with empty username and password")

        self.username = ""
        self.password = ""

        logging.info(f"Testing with:\n"
                     f"username:     {self.username} \n"
                     f"password:     {self.password} \n")
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code

            self.assertNotEqual(201, status_code)

            logging.info("Test successful. User was Not registered. Username and Password are empty")
            logging.info('\n')
        except AssertionError:
            message = response.json()
            self.user_id = message["userId"]

            logging.error("Error in testing registration with empty username and password!")
            logging.error('\n')
            raise

    def test_empty_username(self):
        """
        2.  Empty Username and valid password
        """
        logging.info("Starting test registration with empty username and valid password")

        self.username = ""
        self.password = "Password123!"

        logging.info(f"Testing with:\n"
                     f"username:     {self.username} \n"
                     f"password:     {self.password} \n")
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code

            self.assertNotEqual(201, status_code)

            logging.info("Test successful. User was Not registered. Username is empty")
            logging.info('\n')
        except AssertionError:
            message = response.json()
            self.user_id = message(["userId"])

            logging.error("Error in testing registration with empty username and password!")
            logging.error('\n')
            raise

    def test_create_new_valid_user(self):
        """
        Test registration of a new valid user
        """
        logging.info("Starting test registration with valid credentials")

        self.username = "validUser"
        self.password = "Password123!"

        logging.info(f"Testing with:\n"
                     f"username:     {self.username} \n"
                     f"password:     {self.password} \n")
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code
            message = response.json()

            self.assertEqual(201, status_code)
            self.assertIsNotNone(message["userID"])
            self.assertEqual(message["username"], self.username)
            self.assertEqual(len(message["books"]), 0)

            self.user_id = message["userID"]

            logging.info("Valid User was registered")
            logging.info('\n')
        except AssertionError:
            logging.error("Error in creating a valid new user!")
            logging.error('\n')
            raise

        """ 
        Check that the newly registered user exists
        """
        try:
            response = create_new_user(self.username, self.password)
            status_code = response.status_code

            self.assertNotEqual(201, status_code)

            logging.info("Success in test with newly created valid existing credentials: username = 'validUser', "
                         "password = 'Number123!'. "
                         "User exists!")
            logging.info('\n')
        except AssertionError:
            logging.error("Error in test with newly created valid existing credentials! User does Not exist, "
                          "but should!")
            logging.error('\n')
            raise
