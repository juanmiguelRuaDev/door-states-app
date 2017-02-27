import unittest
import datetime
import os
from src.bbdd.dao import *
from src.bbdd.model import create_tables


class DataBaseTestCase(unittest.TestCase):

    def setUp(self):
        base_dir = os.path.dirname(os.path.realpath(__name__))
        config = Config.instance(base_dir)
        self.config = config
        create_tables(check_exists=True)

    def test_authorized_create_database(self):
        auth_dao = AuthorizedDAO.instance()
        object_test = auth_dao.create(tag_id="AT014931")
        auth_dao.remove(object_id=object_test.id)

    def test_authorized_update_database(self):
        auth_dao = AuthorizedDAO.instance()
        object_test = auth_dao.create(tag_id="AT014931")
        object_test.tag_id = "AT014932"
        to_delete = auth_dao.update(object_test)
        auth_dao.remove(object_id=to_delete.id)

    def test_authorized_create_delete_list_database(self):
        auth_dao = AuthorizedDAO.instance()
        to_save = [{"tag_id": "ABCDEFGH"}, {"tag_id": "QRSTUVWXY"}]
        auth_dao.create_list(to_save)
        auth_dao.delete_list(to_save)

    def test_check_is_authorized_database(self):
        auth_dao = AuthorizedDAO.instance()
        object_test = auth_dao.create(tag_id="AT014931")
        result_check = auth_dao.is_tag_authorized(tag_id="AT014931")
        self.assertTrue(result_check)
        auth_dao.remove(object_id=object_test.id)
        result_check = auth_dao.is_tag_authorized(tag_id="AT014932")
        self.assertFalse(result_check)

    def test_pass_create_database(self):
        pass_dao = PassDAO.instance()
        kwargs = {"tag_id": "12ABCD34",
                  "booster_id": "12345678",
                  "pass_time": datetime.datetime.now(),
                  "barrier_id": 21,
                  "pass_type": False}
        result = pass_dao.create(**kwargs)
        #pass_dao.remove(object_id=result.id)

    def test_pass_update_database(self):
        pass_dao = PassDAO.instance()
        kwargs = {"tag_id": "AT014931",
                  "booster_id": "12345678",
                  "pass_time": datetime.datetime.now(),
                  "barrier_id": 21,
                  "pass_type": False}
        result = pass_dao.create(**kwargs)
        result.tag_id = "AT014932"
        obj_to_remove = pass_dao.update(result)
        pass_dao.remove(object_id=obj_to_remove.id)

    @unittest.skip("adding software engineering cards to test")
    def test_add_cards_database(self):
        auth_dao = AuthorizedDAO.instance()
        to_save = [{"tag_id": "B7560464"},
                   {"tag_id": "95F6F0E4"},
                   {"tag_id": "168010D4"},
                   {"tag_id": "4A52A034"},
                   {"tag_id": "E49D194A"}]
        auth_dao.create_list(to_save)
