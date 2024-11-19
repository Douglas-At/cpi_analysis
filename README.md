# CPI Analysis Tools

This repository contains two main components for analyzing Consumer Price Index (CPI) data from the Bureau of Labor Statistics (BLS):

1. **API Class**: Interacts with the BLS API to extract CPI metrics.
2. **Scraper**: Extracts CPI data from the latest BLS release notes.

---

## Features

### API Class (`api_bsl.py`)
The `APIbureau` class provides a structured way to interact with the BLS API to fetch various CPI indices. It includes methods for:
- Fetching CPI data by series ID, date range, and category.
- Cleaning and saving data in various formats (`xlsx`, `csv`, `txt`).
- Visualizing CPI trends using line plots.

#### Pre-built CPI Metrics
The following CPI metrics are supported out-of-the-box:
- All items
- All items less food and energy
- Food
- Energy
- Apparel
- Education and communication
- Other goods and services
- Medical care
- Recreation
- Transportation

Adding additional indices supported by the BLS API is straightforward by extending the class with a new method and providing the corresponding series ID.

---

### Scraper (`scrapper_release.py`)
A web scraper built using Selenium and Pandas, designed to:
- Navigate to the BLS CPI News Release page.
- Extract the - Table 2. Consumer Price Index for All Urban Consumers (CPI-U): U.S. city average, by detailed expenditure category - from the release notes.
- Save the table as an Excel file for further analysis.

The scraped data provides a quick way to access CPI figures without relying on API calls.

---

## Setup and Installation

### Prerequisites
- Python 3.8+
- Required libraries:
  - `pandas`
  - `requests`
  - `matplotlib`
  - `selenium`
  - `openpyxl` (for Excel support)

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo-name.git
   cd your-repo-name

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Set up your .env file for the BLS API key:

```bash
API_KEY=your_bls_api_key_here
```

---

## Usage

### API Example

Extract CPI data for medical care (2000-2023) and save as a text file:

```python
from api_bsl import APIbureau

api = APIbureau()
api.cpi_medical_care(start_year=2000, end_year=2023, format="txt", plot=True)
```
### Scraper Example

Run the scraper to save the latest CPI table:

```bash
python scrapper_release.py
```
The table will be saved as `CPI_NEWS_RELEASE.xlsx.`

--- 

## Contributing
Feel free to submit issues or pull requests for improvements or additional feature