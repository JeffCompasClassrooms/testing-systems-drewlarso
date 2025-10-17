from squirrel_server import SquirrelServerHandler
from http.server import HTTPServer
import shutil
import os
import pytest
import threading
import requests
import time


@pytest.fixture(autouse=True)
def database():
    file = shutil.copyfile("empty_squirrel_db.db", "squirrel_db.db")
    yield file
    os.remove("squirrel_db.db")


@pytest.fixture
def server():
    listen = ("127.0.0.1", 8080)
    server = HTTPServer(listen, SquirrelServerHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    yield f"http://{listen[0]}:{listen[1]}"

    server.shutdown()
    server.server_close()
    server_thread.join()


def describe_handle_squirrel_index():

    def it_gets_empty_list(server):
        url = f"{server}/squirrels"
        response = requests.get(url)
        assert response.status_code == 200
        assert response.json() == []

    def it_gets_list_with_one_element(server):
        url = f"{server}/squirrels"
        billy = {
            "name": "billy",
            "size": "mini",
        }
        requests.post(url, billy)
        response = requests.get(url)
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "name": "billy",
                "size": "mini"
            }
        ]

    def it_gets_list_with_many_elements(server):
        url = f"{server}/squirrels"
        billy = {
            "name": "billy",
            "size": "mini",
        }
        desmond = {
            "name": "desmond",
            "size": "medium"
        }
        oscar = {
            "name": "oscar",
            "size": "bowling ball",
        }
        requests.post(url, billy)
        requests.post(url, desmond)
        requests.post(url, oscar)
        response = requests.get(url)
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "name": "billy",
                "size": "mini"
            },
            {
                "id": 2,
                "name": "desmond",
                "size": "medium"

            },
            {
                "id": 3,
                "name": "oscar",
                "size": "bowling ball"
            }
        ]


def describe_handle_squirrels_retrieve():
    def it_gets_valid_squirrel_from_list_of_one(server):
        create_url = f"{server}/squirrels"
        retrieve_url = f"{server}/squirrels/1"
        billy = {
            "name": "billy",
            "size": "mini",
        }
        requests.post(create_url, billy)
        response = requests.get(retrieve_url)
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "billy",
            "size": "mini",
        }

    def it_gets_valid_squirrel_from_list_of_many(server):
        create_url = f"{server}/squirrels"
        retrieve_url = f"{server}/squirrels/2"
        billy = {
            "name": "billy",
            "size": "mini",
        }
        desmond = {
            "name": "desmond",
            "size": "medium"
        }
        oscar = {
            "name": "oscar",
            "size": "bowling ball",
        }
        requests.post(create_url, billy)
        requests.post(create_url, desmond)
        requests.post(create_url, oscar)
        response = requests.get(retrieve_url)
        assert response.status_code == 200
        assert response.json() == {
            "id": 2,
            "name": "desmond",
            "size": "medium",
        }

    def it_returns_404_on_invalid_squirrel(server):
        create_url = f"{server}/squirrels"
        retrieve_url = f"{server}/squirrels/10"
        billy = {
            "name": "billy",
            "size": "mini",
        }
        desmond = {
            "name": "desmond",
            "size": "medium"
        }
        oscar = {
            "name": "oscar",
            "size": "bowling ball",
        }
        requests.post(create_url, billy)
        requests.post(create_url, desmond)
        requests.post(create_url, oscar)
        response = requests.get(retrieve_url)
        assert response.status_code == 404


def describe_handle_squirrels_create():
    def it_creates_squirrel_with_valid_data(server):
        url = f"{server}/squirrels"
        billy = {
            "name": "billy",
            "size": "mini",
        }
        response = requests.post(url, billy)
        assert response.status_code == 201

    # def it_errors_when_creating_squirrel_with_invalid_data(server):
    #     url = f"{server}/squirrels"
    #     billy = {
    #         "title": "billy",
    #         "dimensions": "mini",
    #     }
    #     response = requests.post(url, billy)
    #     assert response.status_code == 400

    def it_can_retrieve_squirrel_after_creating_it(server):
        create_url = f"{server}/squirrels"
        get_url = f"{server}/squirrels/1"
        billy = {
            "name": "billy",
            "size": "mini",
        }
        response = requests.post(create_url, billy)
        assert response.status_code == 201
        response = requests.get(get_url)
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "billy",
            "size": "mini",
        }


def describe_handle_squirrels_update():
    def it_updates_valid_squirrel_with_valid_data(server):
        create_url = f"{server}/squirrels"
        update_url = f"{server}/squirrels/1"
        billy = {
            "name": "billy",
            "size": "mini",
        }
        billy_v2 = {
            "name": "billy",
            "size": "pudgy",
        }
        requests.post(create_url, billy)
        response = requests.put(update_url, billy_v2)
        assert response.status_code == 204
        response = requests.get(update_url)
        assert response.json() == {
            "id": 1,
            "name": "billy",
            "size": "pudgy",
        }

    # def it_returns_404_when_updating_valid_squirrel_with_invalid_data(server):
    #     create_url = f"{server}/squirrels"
    #     update_url = f"{server}/squirrels/1"
    #     billy = {
    #         "name": "billy",
    #         "size": "mini",
    #     }
    #     billy_v2 = {
    #         "title": "billy",
    #         "dimensions": "pudgy",
    #     }
    #     requests.post(create_url, billy)
    #     response = requests.put(update_url, billy_v2)
    #     assert response.status_code == 400

    def it_returns_404_when_updating_invalid_squirrel(server):
        create_url = f"{server}/squirrels"
        update_url = f"{server}/squirrels/10"
        billy = {
            "name": "billy",
            "size": "mini",
        }
        requests.post(create_url, billy)
        response = requests.put(update_url, billy)
        assert response.status_code == 404


def describe_handle_squirrels_delete():
    def it_deletes_valid_squirrel(server):
        create_url = f"{server}/squirrels"
        delete_url = f"{server}/squirrels/1"
        billy = {
            "name": "billy",
            "size": "mini",
        }
        requests.post(create_url, billy)
        response = requests.delete(delete_url)
        assert response.status_code == 204
        response = requests.get(delete_url)
        assert response.status_code == 404

    def it_returns_404_when_deleting_invalid_squirrel(server):
        delete_url = f"{server}/squirrels/1"
        response = requests.delete(delete_url)
        assert response.status_code == 404
