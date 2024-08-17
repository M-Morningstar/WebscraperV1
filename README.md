# Web Scraper Project

This project is a web scraper that uses the Playwright library to scrape product information from Amazon. The scraper works with various country-specific Amazon websites and can be customized for different products and countries.

## Prerequisites

Before running this project, you need to have the following installed:

- Python 3.8+
- pip (Python package installer)
- Virtualenv (recommended, but optional)

## Installation

### Step 1: Clone the Repository

Clone this repository to your local machine using the following command:

```bash```
`git clone <repository-url>`

### Step 2: Set Up a Virtual Environment

It's recommended to create a virtual environment to manage dependencies

#### Navigate to the project directory
`cd <repository-folder>`

#### Create a virtual environment
`python -m venv venv`

## Activate the virtual environment
### On Windows
`venv\Scripts\activate`

### On macOS/Linux
`source venv/bin/activate`

### Step 3: Install Dependencies

Install the necessary dependencies listed in the requirements.txt file:

`pip install -r requirements.txt`

### Step 4: Download Playwright Browsers

Since this project uses Playwright, you need to download the necessary browsers:

`playwright install`

### Usage

You can run the scraper by executing the main script within the src folder:

`python main.py`

The user enters the IDs of the products to be scraped and the countries can be edited in the 'countires.csv' file

Follow the prompts to enter product IDs

### Notes

Make sure that the virtual environment is activated whenever you work on this project to avoid dependency issues.

If you encounter issues related to Playwright, ensure that the browsers are correctly installed using the playwright install command.
