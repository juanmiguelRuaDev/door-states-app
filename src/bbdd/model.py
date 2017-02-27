from peewee import *
import platform
import os
from src.utils.common import Config, Constants


BASE_DIR = os.path.dirname(os.path.realpath(__name__))
system = platform.system().lower()
"""TODO: take out this code from here => if system == "windows":
    BASE_DIR += ".."+os.path.sep+".." """
config = Config(BASE_DIR).config
database_path = config['database'][system]
database = SqliteDatabase(database_path)


class BaseModel(Model):
    class Meta:
        database = database


class Authorized(BaseModel):
    tag_id = CharField(unique=True)

    class Meta:
        order_by = ('tag_id',)

    def as_dict(self):
        return {"id": self.id, "tag_id": self.tag_id}


class Pass(BaseModel):
    tag_id = CharField(null=False)
    booster_id = CharField(null=False)
    pass_time = DateTimeField(null=False)
    barrier_id = IntegerField(null=False)
    last_sent_to_server = DateTimeField(null=True)
    pass_type = BooleanField(default=False)

    class Meta:
        order_by = ('pass_time',)

    def as_dict(self):
        pass_time_str, last_sent_str = None, None
        if self.pass_time:
            pass_time_str = str(self.pass_time)
        if self.last_sent_to_server:
            last_sent_str = str(self.last_sent_to_server)

        return {"id": self.id,
                "tag_id": self.tag_id,
                "booster_id": self.booster_id,
                "pass_time": pass_time_str,
                "barrier_id": self.barrier_id,
                "last_sent_to_server": last_sent_str,
                "pass_type": self.pass_type}


def create_tables(check_exists=True):
    database.connect()
    print("--> connected to database")
    database.create_tables([Authorized, Pass], check_exists)
    database.close()
