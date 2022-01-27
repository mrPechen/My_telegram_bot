from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
TOKEN = env.str("PROVIDER_TOKEN")
CHANNEL = env.str("CHANNEL") #ID канала для подписки
DATABASE = env.str("DATABASE")
PGUSER = env.str("PGUSER")
PGPASSWORD = env.str("PGPASSWORD")
DBHOST = env.str("DBHOST")

