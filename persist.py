import logging
from typing import Optional
from telegram.ext._utils.types import BD, CD, UD, CDCData
import json
import os
from ast import literal_eval
from collections import defaultdict
from typing import Dict

import firebase_admin
from firebase_admin import db
from telegram.ext import BasePersistence, PersistenceInput

logger = logging.getLogger(__name__)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FIREBASE_CREDS = os.path.join(ROOT_DIR, os.environ["FIREBASE_CREDENTIALS"])

logger.info("-- firebase cred  %s, file - %s", FIREBASE_CREDS, os.environ["FIREBASE_CREDENTIALS"])


class Persist(BasePersistence):
    def __init__(
        self,
        database_url: str,
        credentials: dict,
        store_data: PersistenceInput = None,
        update_interval: float = 60
    ):
        cred = firebase_admin.credentials.Certificate(credentials)
        self.app = firebase_admin.initialize_app(cred, {"databaseURL": database_url})
        self.fb_user_data = db.reference("user_data")
        self.fb_chat_data = db.reference("chat_data")
        self.fb_bot_data = db.reference("bot_data")
        self.fb_conversations = db.reference("conversations")
        super().__init__(store_data=store_data, update_interval=update_interval)

    @classmethod
    def from_environment(cls):
        with open("flawless-star-133923-431daa09f037.json") as json_file:
            credentials = json.load(json_file)
        return cls(database_url=os.environ["FIREBASE_URL"], credentials=credentials)

    async def get_user_data(self):
        data = self.fb_user_data.get() or {}
        output = self.convert_keys(data)
        logger.info("-----get_user_data ======= data - %s, output - %s", data, output)
        return defaultdict(dict, output)

    async def get_chat_data(self):
        data = self.fb_chat_data.get() or {}
        output = self.convert_keys(data)
        logger.info("-----get_chat_data ======= data - %s, output -%s", data, output)
        return defaultdict(dict, output)

    async def get_bot_data(self):
        data = self.fb_bot_data.get() or {}
        logger.info("-----get_bot_data ======= data -%s", data)
        return defaultdict(dict, data)

    async def get_conversations(self, name):
        res = self.fb_conversations.child(name).get() or {}
        res = {literal_eval(k): v for k, v in res.items()}
        logger.info("-----get_conversations ======= res - %d", res)
        return res

    def update_conversation(self, name, key, new_state):
        if new_state:
            self.fb_conversations.child(name).child(str(key)).set(new_state)
            logger.info("-----update_conversation new_statae - %d, name - %d, key -%d", new_state, name, key)

        else:
            self.fb_conversations.child(name).child(str(key)).delete()
            logger.info("-----update_conversation = name - %d, key - %d ", name, key)

    def update_user_data(self, user_id, data):
        logger.info("-----update_user_data === user_id-%d, data - %s", user_id, data)
        self.fb_user_data.child(str(user_id)).update(data)

    def update_chat_data(self, chat_id, data):
        logger.info("-----update_chat_data ======= chat_id - %d,  data - %s", chat_id, data)
        self.fb_chat_data.child(str(chat_id)).update(data)

    def update_bot_data(self, data):
        logger.info("-----update_bot_data ======= data - %s", data)
        self.fb_bot_data = data

    @staticmethod
    def convert_keys(data: Dict):
        output = {}
        for k, v in data.items():
            if k.isdigit():
                output[int(k)] = v
            else:
                output[k] = v
        return output

    async def get_callback_data(self) -> Optional[CDCData]:
        logger.info("-----get_callback_data ======= CDCData - %s", CDCData)
        pass

    async def update_callback_data(self, data: CDCData) -> None:
        logger.info("-----update_callback_data ======= data -%s", data)
        pass

    async def drop_chat_data(self, chat_id: int) -> None:
        logger.info("-----drop_chat_data ======= chat_id - %s", chat_id)
        pass

    async def drop_user_data(self, user_id: int) -> None:
        logger.info("-----drop_user_data ====== user_id - %s", user_id)
        pass

    async def refresh_user_data(self, user_id: int, user_data: UD) -> None:
        logger.info("-----refresh_user_data ======= user_id -%s, user_data - %s", user_id, user_data)
        pass

    async def refresh_chat_data(self, chat_id: int, chat_data: CD) -> None:
        logger.info("-----refresh_chat_data ======= user_id -%s, user_data - %s", chat_id, chat_data)
        pass

    async def refresh_bot_data(self, bot_data: BD) -> None:
        logger.info("-----refresh_bot_data ======= bot_data - %s", bot_data)
        pass

    async def flush(self) -> None:
        logger.info("----- flush =======")
        pass
