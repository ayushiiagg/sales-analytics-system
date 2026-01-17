# Sales Analytics System

This project is a Python-based Sales Data Analytics System.
It reads raw sales transaction data from a text file, cleans
data quality issues, removes invalid records, and prepares
clean data for analysis.

## Features

- Reads pipe-delimited sales data from a text file
- Handles non-UTF-8 file encoding
- Cleans product names and numeric values
- Removes invalid sales records
- Displays total, invalid, and valid record counts
- Includes basic API integration for product information

Project Structure

sales-analytics-system/
├── main.py
├── README.md
├── requirements.txt
├── utils/
│   ├── file_handler.py
│   ├── data_processor.py
│   └── api_handler.py
├── data/
│   └── sales_data.txt
└── output/

Data Cleaning Rules

The following records are removed:
- Missing CustomerID or Region
- Quantity less than or equal to 0
- UnitPrice less than or equal to 0
- TransactionID not starting with "T"

The following cleaning is applied:
- Commas removed from ProductName
- Commas removed from numeric values

## How to Run the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/ayushiiagg/sales-analytics-system
cd sales-analytics-system
pip install -r requirements.txt
python main.py

#output-
Total records parsed: 80
Invalid records removed: 10
Valid records after cleaning: 70
