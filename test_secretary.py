import copy
from unittest.mock import patch

import pytest
import secretary


INITIAL_DOCUMENTS = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

INITIAL_DIRECTORIES = {
    '1': ['2207 876234', '11-2', '5455 028765'],
    '2': ['10006'],
    '3': []
}


@pytest.fixture(autouse=True)
def reset_data():
    secretary.documents = copy.deepcopy(INITIAL_DOCUMENTS)
    secretary.directories = copy.deepcopy(INITIAL_DIRECTORIES)
    yield
    secretary.documents = copy.deepcopy(INITIAL_DOCUMENTS)
    secretary.directories = copy.deepcopy(INITIAL_DIRECTORIES)


def test_check_document_existance_positive():
    assert secretary.check_document_existance('11-2') is True


def test_check_document_existance_negative():
    assert secretary.check_document_existance('12345') is False


@patch('builtins.input', return_value='11-2')
def test_get_doc_owner_name(mock_input):
    assert secretary.get_doc_owner_name() == 'Геннадий Покемонов'


@patch('builtins.input', return_value='10006')
def test_get_doc_shelf(mock_input):
    assert secretary.get_doc_shelf() == '2'


def test_get_all_doc_owners_names():
    result = secretary.get_all_doc_owners_names()
    assert result == {
        'Василий Гупкин',
        'Геннадий Покемонов',
        'Аристарх Павлов'
    }


def test_add_new_shelf_adds_new_shelf():
    shelf_number, added = secretary.add_new_shelf('4')
    assert shelf_number == '4'
    assert added is True
    assert '4' in secretary.directories
    assert secretary.directories['4'] == []


def test_add_new_shelf_existing_shelf():
    shelf_number, added = secretary.add_new_shelf('1')
    assert shelf_number == '1'
    assert added is False
    assert secretary.directories['1'] == ['2207 876234', '11-2', '5455 028765']


def test_append_doc_to_shelf_existing_shelf():
    secretary.append_doc_to_shelf('12345', '3')
    assert '12345' in secretary.directories['3']


def test_append_doc_to_shelf_new_shelf():
    secretary.append_doc_to_shelf('12345', '4')
    assert '4' in secretary.directories
    assert '12345' in secretary.directories['4']


def test_remove_doc_from_shelf():
    secretary.remove_doc_from_shelf('11-2')
    assert '11-2' not in secretary.directories['1']


@patch('builtins.input', return_value='11-2')
def test_delete_doc(mock_input):
    doc_number, deleted = secretary.delete_doc()
    assert doc_number == '11-2'
    assert deleted is True
    assert secretary.check_document_existance('11-2') is False
    assert '11-2' not in secretary.directories['1']


@patch('builtins.input', side_effect=['12345', 'passport', 'Иван Иванов', '3'])
def test_add_new_doc(mock_input):
    shelf_number = secretary.add_new_doc()
    assert shelf_number == '3'
    assert secretary.check_document_existance('12345') is True
    assert '12345' in secretary.directories['3']
    assert {
        'type': 'passport',
        'number': '12345',
        'name': 'Иван Иванов'
    } in secretary.documents