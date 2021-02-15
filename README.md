<!-- ABOUT THE PROJECT -->

# About The Project

![Scraper tag][product-screenshot]

This is a console program that sends email using Gmail account. You just need to be logged with your google account in Chrome to be able to send a fast email with your terminal.

## Built With

- [Python](https://www.python.org)
- [Selenium WebDriver](https://www.selenium.dev/)

## Prerequisites

This application requires the following software components:

- Python (I recommend install as a virtual environment).

  To install Python follow instructions at https://www.python.org. After Python installation on your system run these commands in the project folder :

  ```sh
  pip install virtualenv
  virtualenv venv
  ./venv/Scripts/activate
  ```

  Install these Python librarys on your system or virtual environment:

- Selenium

  ```sh
  pip install selenium

  ```

## Installation

- See the prerequisites above and clone the repo inside a folder.

```sh
git clone https://github.com/vol-automation/automation-gmail_fast_email.git
```

## Usage

Make sure you are logged in your goggle account in your system's google chrome browser.

### Run program whitin your terminal:

- Windows:

  ```sh
  get_price_amazon "recipient email" "title" "message body or text file"
  ```

  where:

  1. First argument is the recipient email
  2. Second argument is title of the email
  3. Third argument is message body text. This message can be an inline text or the name of a text file. If you use a text file you can send an email with multiple lines.

  practical example:

  Using text file in the same folder as the script:

  ```sh
  send_gmail.bat "vol.design.br@gmail.com" "Hello Marcos" "message.txt"
  ```

  - IMPORTANT: Type complete name of the file

  Using text inline body text:

  ```sh
  send_gmail.bat "vol.design.br@gmail.com" "Hello Marcos" "Please call me when you have the time."
  ```

- Any system:

  ```sh
  py main.py "recipient email" "title" "message body"
  ```

- ### IMPORTANT: Normally defaul google profile is named "Profile 1". If script doesn't work make sure you are using a valid profile folder.

| :warning: In windows chrome's user data folder is located at **%LOCALAPPDATA%\Google\Chrome\User Data**. Inside that folder you will find all profile folders available. Main profile usually is 'Profile 1' folder or 'Default' folder. |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

To change user profile edit main.py script variable:

```python
profile_directory = 'Profile 1' # or 'Default' or whatever
```

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[product-screenshot]: images/tag.png
