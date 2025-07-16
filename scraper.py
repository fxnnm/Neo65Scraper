import json
import logging
import os
import signal
import sys
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.email_utils import send_email

# Load environment variables from .env
load_dotenv()

# Load configuration
with open("config/config.json", "r") as config_file:
    config = json.load(config_file)

SEARCH_PHRASE_PREFIX = config["SEARCH_PHRASE_PREFIX"]
CHECK_INTERVAL = config["CHECK_INTERVAL"]
STATUS_FILE = os.getenv("STATUS_FILE", "status.txt")
URL = config["URL"]  # Set to live URL from configuration

# Configure logging
logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

DEFAULT_STATUS = "Neo65: invoiced on 2024/10/24, not paid"


# Update get_notion_text to fetch content from the URL
def get_notion_text():
    try:
        # Configure Firefox options for headless mode (required for servers)
        options = FirefoxOptions()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Firefox(options=options)

        driver.get(URL)

        wait = WebDriverWait(driver, 20)

        anchor_span = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[text()='Candykeys Order Status, updated daily:']")
            )
        )

        neo_span = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//span[text()='Candykeys Order Status, updated daily:']/following::span[@data-token-index='6'][1]",
                )
            )
        )

        invoiced_span = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//span[text()='Candykeys Order Status, updated daily:']/following::span[@data-token-index='7'][1]",
                )
            )
        )

        logging.debug("Fetched HTML content dynamically using Selenium.")

        if SEARCH_PHRASE_PREFIX in neo_span.text:
            return f"{neo_span.text} {invoiced_span.text}".strip()
        logging.warning("SEARCH_PHRASE_PREFIX not found in the fetched HTML.")
    except Exception as e:
        logging.error(f"Error during Selenium scraping: {e}")
    finally:
        driver.quit()
    return None


def load_last_status():
    try:
        with open(STATUS_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        logging.error(f"Status file not found: {STATUS_FILE}")
        return ""
    except Exception as e:
        logging.error(f"Error reading status file: {e}")
        return ""


def save_status(status):
    try:
        with open(STATUS_FILE, "w") as f:
            f.write(status)
    except Exception as e:
        logging.error(f"Error writing to status file: {e}")


def send_email_notification(subject, message):
    try:
        send_email(subject, message)
        logging.info(f"Email sent successfully: {subject}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")


def send_initialization_email(initial_status):
    message = (
        "The Neo65 scraper is now running and monitoring the status.\n\n"
        f"Initial status: {initial_status if initial_status else 'No status found.'}"
    )
    send_email_notification("✅ Neo65 Scraper Initialized", message)


def send_shutdown_email():
    send_email_notification(
        "⚠️ Neo65 Scraper Stopped",
        (
            "The Neo65 scraper has been stopped or encountered an error. "
            "Please check the logs for details."
        ),
    )


def graceful_shutdown(signum, frame):
    logging.info("[!] Shutting down gracefully...")
    send_shutdown_email()  # Notify the user about the shutdown
    # Perform cleanup actions here
    try:
        if os.path.exists(STATUS_FILE):
            os.remove(STATUS_FILE)  # Remove the status file
            logging.info("[+] Status file removed.")
    except Exception as e:
        logging.error(f"Error during cleanup: {e}")
    sys.exit(0)


# Register signal handlers for graceful shutdown
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)


def main():
    first_check = True
    initial_status = get_notion_text()
    send_initialization_email(
        initial_status
    )  # Notify the user that the scraper is running

    while True:
        logging.info("[*] Checking page...")
        current_status = get_notion_text()
        if not current_status:
            logging.warning("[!] Status block not found.")
        else:
            if first_check:
                # Compare against the default status on the first check
                if current_status != DEFAULT_STATUS:
                    logging.info(
                        f"[+] Status changed: {DEFAULT_STATUS} -> {current_status}"
                    )
                    send_email(
                        "⚠️ Neo65 Status Changed", f"New status:\n\n{current_status}"
                    )
                    save_status(current_status.strip())  # Save normalized status
                else:
                    save_status(DEFAULT_STATUS)  # Save the default status
                first_check = False
            else:
                last_status = load_last_status().strip()  # Normalize saved status
                if current_status != last_status:
                    logging.info(
                        f"[+] Status changed: {last_status} -> {current_status}"
                    )
                    send_email(
                        "⚠️ Neo65 Status Changed", f"New status:\n\n{current_status}"
                    )
                    save_status(current_status.strip())  # Save normalized status
                else:
                    logging.info("[=] No change.")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
