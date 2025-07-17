# Neo65 Web Scraper

## Description
The Neo65 Web Scraper is a Python-based tool designed to monitor the status of Neo65 invoices. It fetches content from a URL to extract status information and sends email notifications when the status changes, when the tool starts, or when it stops/crashes.

## Features
- Monitors a URL for status changes.
- Sends email notifications for:
  - Status changes.
  - Tool initialization.
  - Tool shutdown or crashes.
- Graceful shutdown with resource cleanup.
- Configurable via environment variables.

## Requirements
- Recommended: Python 3.12.2
- Dependencies listed in `requirements.txt`:
  ```
   beautifulsoup4==4.13.4
   certifi==2025.7.9
   charset-normalizer==3.4.2
   click==8.2.1
   colorama==0.4.6
   idna==3.10
   mccabe==0.7.0
   mypy_extensions==1.1.0
   packaging==25.0
   pathspec==0.12.1
   pip==25.1.1
   platformdirs==4.3.8
   pycodestyle==2.14.0
   pyflakes==3.4.0
   python-dotenv==1.1.1
   requests==2.31.0
   selenium>=4.0.0
   soupsieve==2.7
   typing_extensions==4.14.1
   urllib3==2.5.0
  ```

## Prerequisites
- A Gmail account for sending emails.
- 2FA has to be enabled on the Gmail account.
- A 16-Character App Password must be generated for the Gmail account to allow the scraper to send emails.
- Here: https://myaccount.google.com/apppasswords

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/neo65-webscraper.git
   cd Neo65Scraper
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the **project root** with the following variables:
   ```properties
   EMAIL_SENDER=your_email@gmail.com
   EMAIL_PASSWORD=1234abcd5678efgh (Use the 16-Character App Password)
   EMAIL_RECEIVER=recipient_email@gmail.com
   SMTP_SERVER=smtp.gmail.com
   ```

4. **Configure the URL**:
   Adjust the `config/config.json` file as needed, per default the tool runs once every Minute:
   ```json
   {
    "URL": "https://qwertykeys.notion.site/Abnormal-Vendor-Order-Status-e8d312367c84464fa191a34ec6e2a05b",
    "SEARCH_PHRASE_PREFIX": "Neo65:",
    "CHECK_INTERVAL": 60,
    "STATUS_FILE": "status.txt"
   }
   ```

## Usage

1. **Run the Scraper**:
   ```bash
   python scraper.py
   ```

2. **Logs**:
   Check `logs/scraper.log` for runtime information and errors.

## How It Works
- On startup, the tool sends an initialization email.
- It fetches content from the configured URL and monitors for changes in the status.
- If the status changes, it sends an email notification and updates `status.txt`.
- On shutdown or crash, it sends a shutdown email and cleans up resources.

## Help
- For questions and help, write to me on Discord: fiiiiinn (You can find me on CandyKeys or QwertyKeys Discord servers) or open an issue on this repository.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Author
Finn M.
