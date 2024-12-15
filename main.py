import asyncio
import logging
import ssl
import warnings
import random
from datetime import datetime
from typing import Dict, List, Optional, Set

import cloudscraper
from colorama import Fore, Style, init
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Inisialisasi
init(autoreset=True)
warnings.simplefilter("ignore", InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)


# Kelas Warna untuk Output
class Colors:
    SUCCESS = f"{Fore.GREEN}"
    ERROR = f"{Fore.RED}"
    INFO = f"{Fore.CYAN}"
    WARNING = f"{Fore.YELLOW}"
    RESET = f"{Style.RESET_ALL}"


# Bot Validator
class DawnValidatorBot:
    API_URLS = {
        "keepalive": "https://www.aeropres.in/chromeapi/dawn/v1/userreward/keepalive",
        "getPoints": "https://www.aeropres.in/api/atom/v1/userreferral/getpoint",
        "socialmedia": "https://www.aeropres.in/chromeapi/dawn/v1/profile/update",
    }

    EXTENSION_ID = "675f168c9e13e15af4311da1"
    VERSION = "1.1.1"

    def __init__(self):
        self.verified_accounts: Set[str] = set()
        self.scraper = cloudscraper.create_scraper()
        self.proxies: List[str] = []

    def get_base_headers(self, token: str) -> Dict[str, str]:
        return {
            "Accept": "*/*",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Origin": f"chrome-extension://{self.EXTENSION_ID}",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
            ),
        }

    @staticmethod
    def log_colored(level: str, message: str, color: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {color}{level}: {message}{Colors.RESET}")

    def get_random_proxy(self) -> Optional[str]:
        return random.choice(self.proxies) if self.proxies else None

    async def fetch_points(self, headers: Dict[str, str]) -> int:
        try:
            response = self.scraper.get(
                f"{self.API_URLS['getPoints']}?appid=675f168c9e13e15af4311da1",
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()

            if not data.get("status"):
                raise ValueError(data.get("message", "Unknown error"))

            points_data = data.get("data", {})
            reward = points_data.get("rewardPoint", {})
            referral = points_data.get("referralPoint", {})

            total = sum(
                [
                    reward.get("points", 0),
                    reward.get("registerpoints", 0),
                    reward.get("signinpoints", 0),
                    reward.get("twitter_x_id_points", 0),
                    reward.get("discordid_points", 0),
                    reward.get("telegramid_points", 0),
                    reward.get("bonus_points", 0),
                    referral.get("commission", 0),
                ]
            )
            return total

        except Exception as e:
            self.log_colored("ERROR", f"Failed to fetch points: {str(e)}", Colors.ERROR)
            return 0

    async def keep_alive_request(self, headers: Dict[str, str], email: str) -> bool:
        payload = {
            "username": email,
            "extensionid": self.EXTENSION_ID,
            "numberoftabs": 0,
            "_v": self.VERSION,
        }

        try:
            response = self.scraper.post(
                f"{self.API_URLS['keepalive']}?appid=675f168c9e13e15af4311da1",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            return True
        except Exception as e:
            self.log_colored(
                "ERROR", f"Keep-alive failed for {email}: {str(e)}", Colors.ERROR
            )
            return False

    async def verify_social_media(self, account: Dict[str, str], proxy: Optional[str] = None) -> None:
        email = account["email"]

        if email in self.verified_accounts:
            return

        headers = self.get_base_headers(account["token"])
        if proxy:
            headers["Proxy"] = proxy

        social_types = ["twitter_x_id", "discordid", "telegramid"]

        self.log_colored(
            "INFO", f"Starting social media verification for {email}", Colors.INFO
        )

        for social_type in social_types:
            try:
                response = self.scraper.post(
                    f"{self.API_URLS['socialmedia']}?appid=675f168c9e13e15af4311da1",
                    json={social_type: social_type},
                    headers=headers,
                    timeout=60,
                )
                response.raise_for_status()

                result = response.json()
                if result.get("success"):
                    self.log_colored(
                        "SUCCESS", f"Verified {social_type} for {email}", Colors.SUCCESS
                    )
                else:
                    self.log_colored(
                        "ERROR",
                        f"Failed to verify {social_type} for {email}: {result.get('message')}",
                        Colors.ERROR,
                    )

            except Exception as e:
                self.log_colored(
                    "ERROR", f"Error verifying {social_type} for {email}: {str(e)}", Colors.ERROR
                )

            await asyncio.sleep(90)

        self.log_colored(
            "INFO", f"Completed social media verification for {email}", Colors.INFO
        )
        self.verified_accounts.add(email)

    @staticmethod
    def load_accounts() -> List[Dict[str, str]]:
        try:
            with open("accounts.txt", "r") as f:
                accounts = [
                    {"email": line.split(":")[0], "token": line.split(":")[1].strip()}
                    for line in f
                    if ":" in line
                ]
            if accounts:
                DawnValidatorBot.log_colored(
                    "SUCCESS",
                    f"Loaded {len(accounts)} accounts from accounts.txt",
                    Colors.SUCCESS,
                )
            else:
                raise ValueError("No accounts found in accounts.txt")
            return accounts
        except FileNotFoundError:
            DawnValidatorBot.log_colored(
                "ERROR", "accounts.txt not found. Exiting...", Colors.ERROR
            )
            return []

    def load_proxies(self) -> None:
        try:
            with open("proxies.txt", "r") as f:
                self.proxies = [line.strip() for line in f if line.strip()]

            if self.proxies:
                self.log_colored(
                    "SUCCESS", f"Loaded {len(self.proxies)} proxies", Colors.SUCCESS
                )
            else:
                self.log_colored(
                    "WARNING", "No proxies found in proxies.txt", Colors.WARNING
                )

        except FileNotFoundError:
            self.log_colored("WARNING", "proxies.txt not found. Running without proxies.", Colors.WARNING)

    @staticmethod
    def display_welcome() -> None:
        print(
            f"""
{Colors.INFO}{Style.BRIGHT}╔══════════════════════════════════════════════╗
║            Dawn Bot Anzcrypto           ║
║      Welcome and do with your own risk!      ║
╚══════════════════════════════════════════════╝{Colors.RESET}
"""
        )

    async def process_account(self, account: Dict[str, str]) -> int:
        email = account["email"]
        proxy = self.get_random_proxy()
        headers = self.get_base_headers(account["token"])

        if proxy:
            headers["Proxy"] = proxy

        self.log_colored("INFO", f"Processing account: {email}", Colors.INFO)
        self.log_colored("INFO", f"Using proxy: {proxy or 'No Proxy'}", Colors.INFO)

        points = await self.fetch_points(headers)
        self.log_colored("INFO", f"Current points: {points}", Colors.WARNING)

        await self.verify_social_media(account, proxy)
        await self.keep_alive_request(headers, email)

        return points


async def main():
    bot = DawnValidatorBot()
    bot.display_welcome()

    accounts = bot.load_accounts()
    if not accounts:
        return

    bot.load_proxies()

    try:
        while True:
            account_tasks = [bot.process_account(account) for account in accounts]
            await asyncio.gather(*account_tasks)
            await asyncio.sleep(300)
    except KeyboardInterrupt:
        bot.log_colored("WARNING", "Process interrupted by user. Exiting...", Colors.WARNING)


if __name__ == "__main__":
    asyncio.run(main())
