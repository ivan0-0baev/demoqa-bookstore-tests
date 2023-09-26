import random
import requests


def create_new_user(username, password):
    """
    Register a new user
    :param      username:   Username to register with
    :param      password:   Password to register with
    :return:    response:   Response message
    """
    user = {
        'userName': username,
        'password': password
    }
    response = requests.post(url='https://demoqa.com/Account/v1/User', json=user)

    return response


def generate_token(username, password):
    """
    Generate Authorization Token for the specified user
    :param      username:   Username of the specified user
    :param      password:   Password of the specified user
    :return:    response:   Response message
    """
    user = {
        'userName': username,
        'password': password
    }
    response = requests.post(url='https://demoqa.com/Account/v1/GenerateToken', json=user)

    return response


def delete_user(user_id, username, password):
    """
    Delete a registered user
    :param      user_id:    User Id
    :param      username:   Username to register with
    :param      password:   Password to register with
    :return:    response:   Response message
    """
    response = generate_token(username, password)
    status_code = response.status_code
    message = response.json()

    token = message["token"] if status_code == 200 else " "
    headers = {"Authorization": f'Bearer {token}'}
    response = requests.delete(url=f'https://demoqa.com/Account/v1/User/{user_id}', headers=headers)

    return response


def get_user_info(user_id, token):
    """
    Get information of specified user
    :param      user_id:    Id of the specified user
    :param      token:      Authorization token of the specified user
    :return:    response:   Response message
    """
    headers = {"Authorization": f'Bearer {token}'}
    response = requests.get(url=f'https://demoqa.com/Account/v1/User/{user_id}', headers=headers)

    return response


def is_authorized(username, password):
    """
    Check if specified user is authorized
    :param      username:   Username of the specified user
    :param      password:   Password of the specified user
    :return:    response:   Response message
    """
    user = {
        'userName': username,
        'password': password
    }
    response = requests.post(url='https://demoqa.com/Account/v1/Authorized', json=user)

    return response


def add_book(user_id, collection_isbns, token):
    """
    Add book/s to add to a specified user
    :param      user_id:             UserId of specified user
    :param      collection_isbns:  Isbn/s of books to add to the collection of the specified user
    :param      token:              Token of specified user
    :return:    response:           Response message
    """
    body = {
        'userId': user_id,
        'collectionOfIsbns': collection_isbns
    }
    headers = {"Authorization": f'Bearer {token}'}
    response = requests.post('https://demoqa.com/BookStore/v1/Books', json=body, headers=headers)

    return response


def get_books():
    """
    Return all books in the store
    :return:    response:   Response message
    """
    response = requests.get('https://demoqa.com/BookStore/v1/Books')

    return response


def get_book(isbn):
    """
    Get a book by a given isbn
    :param      isbn:       Isbn of book wanted
    :return:    response:   Response message
    """
    params = {
        'ISBN': {isbn}
    }
    response = requests.get('https://demoqa.com/BookStore/v1/Book', params=params)

    return response


def get_random_book():
    """
    Get isbn of a random book
    :return:    isbn:   random isbn
    """
    response = get_books()
    books = response.json()["books"]
    index = random.randint(0, len(books))

    isbn = books[index]["isbn"]

    return isbn


def replace_book_in_collection(user_id, token, current_isbn, isbn_not_in_collection):
    """
    Replace book in collection with another
    :param      user_id:        UserId of the specified User
    :param      token:          Authorization token of specified user
    :param      current_isbn:   Isbn in collection that is to be replaced
    :param      isbn_not_in_collection:   New isbn to add to collection in place of the other
    :return:    Response:       Response message
    """
    body = {
        'userId': user_id,
        'isbn': isbn_not_in_collection
    }
    headers = {"Authorization": f'Bearer {token}'}
    response = requests.put(f'https://demoqa.com/BookStore/v1/Books/{current_isbn}', json=body, headers=headers)

    return response


def remove_book_from_collection(user_id, isbn, token):
    """
    Remove a book from the collection of a specified user
    :param      user_id:     UserId of specified user
    :param      isbn:       Isbn of the book you to be removed from the user's collection
    :param      token:      Authorization token of the specified user
    :return:    response:   Response message
    """
    body = {
        'isbn': isbn,
        'userId': user_id
    }
    headers = {"Authorization": f'Bearer {token}'}
    response = requests.delete('https://demoqa.com/BookStore/v1/Book', json=body, headers=headers)

    return response

