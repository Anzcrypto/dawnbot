# Dawn Validator Bot

This bot automates the process of validating accounts and fetching points using the Dawn platform.

## Requirements

- Python 3.x
- All requirements are listed in the `req.txt` file.

## Setup

1. Clone this repository:

    ```bash
    git clone https://github.com/Anzcrypto/dawnbot
    cd dawnbot
    ```

2. Install dependencies:

    ```bash
    pip3 install -r req.txt
    ```

3. Prepare the `accounts.txt` and `proxies.txt` files (if required).

   - `accounts.txt` should contain account data in the following format:

     ```
     email:token
     ```

   - `proxies.txt` should contain a list of proxies if you intend to use them.
## How to Get Bearer Token

To use the bot, you will need to obtain a Bearer token. Follow these steps to get it:

1. **Log in to the Dawn platform** using your browser.
2. Open **Developer Tools** in your browser (press `F12` or `Ctrl+Shift+I`).
3. Go to the **Network** tab.
4. Perform any action that requires authentication (e.g., logging in or making a request).
5. Look for the request in the **Network** tab that includes an `Authorization` header with the Bearer token.
6. Copy the token from the `Authorization` header.

## Running the Script

1. **Run the script:**

    ```bash
    python3 main.py
    ```

2. **Notes:**

   - Use `CTRL + C` to stop the process.
   - Ensure the `accounts.txt` and `proxies.txt` files are prepared (if needed).
   - The bot will ask you to choose between processing a single account or multiple accounts from the `accounts.txt` file.

## Features

- Fetches points from the Dawn platform.
- Verifies social media accounts like Twitter, Discord, and Telegram.
- Supports proxy usage for requests.
- Automatically keeps the session alive by sending keep-alive requests.

## License

This project is open-source and available under the [MIT License](LICENSE).
