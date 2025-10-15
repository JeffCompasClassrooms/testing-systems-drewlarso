from mydb import MyDB
import pytest
import os


@pytest.fixture
def db():
    db = MyDB("testing.db")
    yield db
    os.remove("testing.db")


def describe_constructor():

    def test_db_creates_file_if_doesnt_exist():
        if os.path.exists("test.db"):
            os.remove("test.db")

        assert not os.path.exists("test.db")

        db = MyDB("test.db")

        assert os.path.exists("test.db")

        os.remove("test.db")

    def test_db_does_nothing_if_file_exists():
        if not os.path.exists("test.db"):
            with open("test.db", 'wb') as f:
                f.write(b"hello world")

        assert os.path.exists("test.db")

        db = MyDB("test.db")

        assert os.path.exists("test.db")

        os.remove("test.db")


def describe_load_strings():

    def test_db_loads_data_when_empty(db):
        strings = db.loadStrings()
        assert strings == []

    def test_db_loads_data_with_one_string(db):
        db.saveString("python")
        strings = db.loadStrings()
        assert strings == ["python"]

    def test_db_loads_data_with_multiple_strings(db):
        db.saveStrings(["python", "javascript", "rust", "go"])
        strings = db.loadStrings()
        assert strings == ["python", "javascript", "rust", "go"]

    def test_db_loads_data_with_multiple_various_types(db):
        db.saveStrings(["python", 47, True, None])
        strings = db.loadStrings()
        assert strings == ["python", 47, True, None]


def describe_save_strings():

    def test_db_saves_valid_array(db):
        db.saveStrings(["python", "javascript", "rust", "go"])
        strings = db.loadStrings()
        assert strings == ["python", "javascript", "rust", "go"]

    def test_db_saves_arbitrary_data(db):
        db.saveStrings(47)
        strings = db.loadStrings()
        assert strings == 47
        db.saveStrings("python")
        strings = db.loadStrings()
        assert strings == "python"

    def test_save_strings_returns_nothing(db):
        data = db.saveStrings(["python", "javascript", "rust"])
        assert data == None


def describe_save_string():

    def test_db_saves_valid_string(db):
        db.saveString("python")
        strings = db.loadStrings()
        assert strings == ["python"]

    def test_db_saves_multiple_valid_strings(db):
        db.saveString("python")
        db.saveString("javascript")
        db.saveString("rust")
        strings = db.loadStrings()
        assert strings == ["python", "javascript", "rust"]

    def test_db_errors_when_load_strings_doesnt_return_an_array(db):
        db.saveStrings("not an array")

        with pytest.raises(AttributeError):
            db.saveString("python")

    def test_save_string_returns_nothing(db):
        data = db.saveString("python")
        assert data == None
