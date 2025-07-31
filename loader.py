from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage, RedisStorage2

from data import config
from utils.db_api.additional_db import AdditionalDB
from utils.db_api.admin_db import AdminDB
from utils.db_api.articles_db import ArticlesDB
from utils.db_api.ayzenk_db import AyzenkDB
from utils.db_api.create_db_tables import Database
from utils.db_api.leo_db import LeongardDB
from utils.db_api.projects_db import ProjectsDB
from utils.db_api.statistics_db import StatisticsDB
from utils.db_api.users_admin_db import UsersDB
from utils.db_api.yaxin_db import YaxinDB

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(
    host='localhost',
    port=6379,
    db=5,
    state_ttl=3600
)

dp = Dispatcher(bot, storage=storage)
db = Database()
udb = UsersDB(db)
adb = AdminDB(db)
stdb = StatisticsDB(db)
artdb = ArticlesDB(db)
prdb = ProjectsDB(db)
ayzdb = AyzenkDB(db)
leodb = LeongardDB(db)
yxndb = YaxinDB(db)
adldb = AdditionalDB(db)
