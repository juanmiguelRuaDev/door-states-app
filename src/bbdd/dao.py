from src.bbdd.model import *


class BaseDAO(object):

    def __init__(self):
        self.database = database
        create_tables()


class AuthorizedDAO(BaseDAO):

    __local_instance = None

    def __init__(self):
        BaseDAO.__init__(self)

    @database.transaction()
    def create(self, tag_id):
        result = Authorized.select().where(Authorized.tag_id == tag_id)
        if result:
            return result[0]
        result = Authorized.create(tag_id=tag_id)
        return result

    @database.transaction()
    def create_list(self, tags_list):
        tags_id_to_create = [item["tag_id"] for item in tags_list]
        current_created = Authorized.select().where(Authorized.tag_id << tags_id_to_create)
        current_tag_created = [item.tag_id for item in current_created]
        set_to_create = {tag for tag in tags_id_to_create if tag not in current_tag_created}
        list_to_create = [{"tag_id": tag} for tag in set_to_create]
        if not list_to_create:
            return list_to_create
        with database.atomic():
            Authorized.insert_many(list_to_create).execute()
        return list_to_create

    @database.transaction()
    def replace_cards_by_list(self, tags_list):
        list_to_create = [{"tag_id": tag} for tag in tags_list]
        with database.atomic():
            Authorized.delete().execute()
        with database.atomic():
            Authorized.insert_many(list_to_create).execute()
        return list_to_create

    @database.transaction()
    def delete_list(self, tags_list):
        tags_id_to_delete = [item["tag_id"] for item in tags_list]
        cards_to_delete = Authorized.select().where(Authorized.tag_id << tags_id_to_delete)
        list_response = [element.as_dict() for element in cards_to_delete]
        with database.atomic():
            Authorized.delete().where(Authorized.tag_id << tags_id_to_delete).execute()
        return list_response

    @database.transaction()
    def update(self, auth_instance):
        auth_instance.save()
        return auth_instance

    @database.transaction()
    def get(self, object_id):
        result = Authorized.get(Authorized.id == object_id)
        return result

    @database.transaction()
    def find(self, tag_id):
        result_list = Authorized.select().where(Authorized.tag_id == tag_id)
        return result_list

    @database.transaction()
    def find(self, tag_id_list=None):
        if tag_id_list:
            return Authorized.select().where(Authorized.tag_id << tag_id_list)
        return Authorized.select()

    @database.transaction()
    def is_tag_authorized(self, tag_id):
        result = Authorized.select().where(Authorized.tag_id == tag_id)
        if result:
            return True
        return False

    @database.transaction()
    def remove(self, object_id):
        result = Authorized.get(Authorized.id == object_id)
        if result is not None:
            result = result.delete_instance()
        return result

    @classmethod
    def instance(cls):
        if cls.__local_instance is not None:
            return cls.__local_instance
        cls.__local_instance = cls()
        return cls.__local_instance


class PassDAO(BaseDAO):

    __local_instance = None

    def __init__(self):
        BaseDAO.__init__(self)

    @database.transaction()
    def find(self, tag_id):
        result_list = Pass.select().where(Pass.tag_id == tag_id)
        return result_list

    @database.transaction()
    def find(self, start_date=None, end_date=None):
        if start_date and end_date:
            return Pass.select().where(Pass.pass_time.between(start_date, end_date))
        elif start_date and not end_date:
            return Pass.select().where(Pass.pass_time >= start_date)
        elif not start_date and end_date:
            return Pass.select().where(Pass.pass_time <= end_date)
        return Pass.select()

    @database.transaction()
    def find_sent_to_server(self, sent_to_server=False):
        #TODO: use sent_to_server later
        lista = Pass.select().where(Pass.last_sent_to_server >> None)
        return lista

    @database.transaction()
    def create(self, tag_id, booster_id, pass_time, barrier_id, pass_type):
        response = Pass.create(tag_id=tag_id,
                               booster_id=booster_id,
                               pass_time=pass_time,
                               barrier_id=barrier_id,
                               pass_type=pass_type)
        return response

    @database.transaction()
    def update(self, auth_instance):
        auth_instance.save()
        return auth_instance

    @database.transaction()
    def update_list(self, pass_instance_list):
        for pass_instance in pass_instance_list:
            pass_instance.save()
        return pass_instance_list

    @database.transaction()
    def remove(self, object_id):
        result = Pass.get(Pass.id == object_id)
        if result is not None:
            result = result.delete_instance()
        return result

    @classmethod
    def instance(cls):
        if cls.__local_instance is not None:
            return cls.__local_instance
        cls.__local_instance = cls()
        return cls.__local_instance









