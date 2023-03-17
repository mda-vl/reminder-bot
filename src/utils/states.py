from fake_useragent import UserAgent

from utils.settings import Settings

config: Settings | None = None

ua = UserAgent()
headers = {"User-Agent": ua.chrome}
