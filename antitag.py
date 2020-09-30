#made by github.com/AivenGog
from .. import loader, utils

import logging, time


from telethon import types

logger = logging.getLogger(__name__)

@loader.tds
class retMod(loader.Module):
    """Посылает сообщение при вашем теге"""
    strings = {"name": "RFD",
               "gone": "cock up",
               "back": "cock down",
               "ret": "<b>🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈🌈.</b>",
               "ret_reason": "{}"}

    async def client_ready(self, client, db):
        self._db = db
        self._me = await client.get_me()

    async def rfdcmd(self, message):
        """.rfd [текст]"""
        if utils.get_args_raw(message):
            self._db.set(__name__, "ret", utils.get_args_raw(message))
        else:
            self._db.set(__name__, "ret", self.strings("ret"))
        self._db.set(__name__, "gone", time.time())
        await self.allmodules.log("ret", data=utils.get_args_raw(message) or None)
        await message.edit(self.strings("gone", message))

    async def unrfdcmd(self, message):
        """Перестаёт писать"""
        self._db.set(__name__, "ret", False)
        self._db.set(__name__, "gone", None)
        await self.allmodules.log("unret")
        await message.edit(self.strings("back", message))

    async def watcher(self, message):
        if not isinstance(message, types.Message):
            return
        if message.mentioned or getattr(message.to_id, "user_id", None) == self._me.id:
            if self.get_ret() != False:
                ret_state = self.get_ret()
                ret = self.strings("ret_reason", message).format(ret_state)
                await message.reply(ret)


    def get_ret(self):
        return self._db.get(__name__, "ret", False)
