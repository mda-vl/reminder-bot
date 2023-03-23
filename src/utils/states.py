from fake_useragent import UserAgent

from utils.settings import Settings

config: Settings | None = None
base_uri = "https://api.binance.com/api/v3/"

ua = UserAgent()
headers = {"User-Agent": ua.chrome}
