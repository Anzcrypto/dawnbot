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

## Running the Script

1. **Run the script:**

    ```bash
    python main.py
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
