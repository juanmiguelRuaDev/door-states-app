from src.bbdd.dao import AuthorizedDAO, PassDAO
from src.utils.common import Constants
from src.core.exception import ManagerException
import datetime


class AccessCardManager:
    """
    Manager that aims to manage all database AccessCard operations
    """
    __local_instance = None

    def __init__(self):
        self.auth_dao = AuthorizedDAO.instance()
        self.pass_dao = PassDAO.instance()

    def add_authorize_card_list(self, card_list=None) -> list:
        """
        From a list of card_ids, this operation will create an register in database for every element in \:card_list\n
        \:argument
        :param card_list:
        :return:
        """
        if not card_list:
            raise ManagerException("card_list is not iterable")

        list_to_save = [{"tag_id": card} for card in card_list]
        if not list_to_save:
            return None
        list_created = self.auth_dao.create_list(list_to_save)
        return list_created

    def update_authorized_card_list(self, card_list=None) -> list:
        """
        Replace all cards stored in database by all cards specified in card_list
        :param card_list:
        :return:
        """
        if not card_list:
            return None
        list_updated = self.auth_dao.replace_cards_by_list(card_list)
        return list_updated

    def get_authorized_card_list(self):
        all_authorized = self.auth_dao.find()
        return [item.as_dict() for item in all_authorized]

    def delete_authorized_card_list(self, card_list=None):
        list_to_delete = [{"tag_id": card} for card in card_list]
        if not list_to_delete:
            return None
        list_deleted = self.auth_dao.delete_list(list_to_delete)
        return list_deleted

    @classmethod
    def instance(cls):
        if cls.__local_instance is None:
            cls.__local_instance = cls()
        return cls.__local_instance


class PassManager:
    """
    Manager that aims to manage all database Pass operations
    """

    __local_instance = None

    def __init__(self):
        self.pass_dao = PassDAO.instance()

    def get_passing_between_dates(self, start_date, end_date):
        list_passes = self.pass_dao.find(start_date=start_date, end_date=end_date)
        return [elem.as_dict() for elem in list_passes]

    def get_tags_between_dates(self, start_date=None, end_date=None):
        if not start_date and not end_date:
            return []
        list_passes = self.pass_dao.find(start_date=start_date, end_date=end_date)
        return [elem.tag_id for elem in list_passes]

    def get_not_sent_to_server_passes(self):
        list_passes = self.pass_dao.find_sent_to_server()
        for pass_instance in list_passes:
            pass_instance.last_sent_to_server = datetime.datetime.now()

        final_list = self.pass_dao.update_list(list_passes)
        return [dict(cid=item.tag_id,
                     bid=item.booster_id,
                     inout=item.pass_type,
                     time=item.pass_time.strftime(Constants.DATE_FORMAT)) for item in final_list]


    @classmethod
    def instance(cls):
        if cls.__local_instance is None:
            cls.__local_instance = cls()
        return cls.__local_instance


class ConfigManager:

    __local_instance = None

    def __init__(self):
        pass

    @classmethod
    def instance(cls):
        if cls.__local_instance is None:
            cls.__local_instance = cls()
        return cls.__local_instance
