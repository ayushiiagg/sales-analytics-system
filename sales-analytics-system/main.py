from utils.file_handler import read_sales_file
from utils.data_processor import clean_sales_data

def main():
    file_path = "data/sales_data.txt"
    records = read_sales_file(file_path)
    clean_sales_data(records)

if __name__ == "__main__":
    main()

from utils.file_handler import read_sales_data

data = read_sales_data("data/sales_data.txt")
print(data[:5])

from utils.file_handler import read_sales_data
from utils.data_processor import parse_transactions

raw_data = read_sales_data("data/sales_data.txt")
clean_data = parse_transactions(raw_data)

print(clean_data[0])

from utils.file_handler import read_sales_data
from utils.data_processor import parse_transactions, validate_and_filter

raw = read_sales_data("data/sales_data.txt")
parsed = parse_transactions(raw)

valid, invalid_count, summary = validate_and_filter(
    parsed,
    region="North",
    min_amount=1000,
    max_amount=50000
)

print("Invalid records:", invalid_count)
print("Summary:", summary)
print("Valid sample:", valid[:2])

from utils.file_handler import read_sales_data
from utils.data_processor import parse_transactions, validate_and_filter, calculate_total_revenue

raw = read_sales_data("data/sales_data.txt")
parsed = parse_transactions(raw)

valid_txns, _, _ = validate_and_filter(parsed)

total = calculate_total_revenue(valid_txns)
print("Total Revenue:", total)

from utils.data_processor import region_wise_sales

region_report = region_wise_sales(valid_txns)

for region, data in region_report.items():
    print(region, data)
from utils.data_processor import top_selling_products

top_products = top_selling_products(valid_txns, n=5)

for item in top_products:
    print(item)
from utils.data_processor import customer_analysis

customer_report = customer_analysis(valid_txns)

for cust, data in customer_report.items():
    print(cust, data)
from utils.data_processor import (
    parse_transactions,
    daily_sales_trend,
    find_peak_sales_day
)
with open("data/sales_data.txt", "r") as file:
    raw_lines = file.readlines()
valid_transactions = parse_transactions(raw_lines)
daily = daily_sales_trend(valid_transactions)
peak = find_peak_sales_day(valid_transactions)

print(daily)
print(peak)
print(type(raw_lines), type(valid_transactions))

from utils.data_processor import low_performing_products
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import get_all_products

# File processing
read_sales_data("data/sales_data.txt")
parsed = parse_transactions(raw)
valid_transactions, _, _ = validate_and_filter(parsed)

print("Total Revenue:", calculate_total_revenue(valid_transactions))
print("Low Products:", low_performing_products(valid_transactions))

# API example
api_data = get_all_products(limit=5)
for p in api_data['products']:
    print(p['title'], p['price'])
from utils.api_handler import fetch_all_products
products = fetch_all_products()

print("Total products fetched:", len(products))

# Print first 5 products
for product in products[:5]:
    print(product["title"], product["price"])

from utils.api_handler import fetch_all_products, create_product_mapping
products = fetch_all_products()
product_map = create_product_mapping(products)

print("Total mapped products:", len(product_map))

# Example: print product with ID 1
print(product_map.get(1))

from utils.file_handler import read_sales_file
from utils.data_processor import (
    parse_transactions,
    enrich_sales_data,
    save_enriched_data
)
from utils.api_handler import fetch_all_products, create_product_mapping
raw_lines = read_sales_file("data/sales_data.txt")
transactions = parse_transactions(raw_lines)
api_products = fetch_all_products()
product_mapping = create_product_mapping(api_products)
print(type(transactions), len(transactions))
enriched = enrich_sales_data(transactions, product_mapping)
save_enriched_data(enriched)
print("Enriched sales data saved successfully.")

from utils.report_generator import generate_sales_report

generate_sales_report(
    transactions,
    enriched,
    "output/sales_report.txt"
)

print("Sales report generated successfully.")
from utils.file_handler import read_sales_file
from utils.data_processor import (
    parse_transactions,
    validate_transactions,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import fetch_all_products, create_product_mapping
from utils.enrichment import enrich_sales_data, save_enriched_data
from utils.report_generator import generate_sales_report

# main.py

# Correct imports
from utils.data_processor import parse_transactions  # use parse_transactions since validate_transactions doesn't exist
from utils.analysis import perform_all_analyses
from utils.api_helper import fetch_product_data, enrich_sales_data
from utils.report import generate_report

def validate_transactions(transactions):
    """
    Simple validation placeholder.
    Checks if essential fields exist in each transaction.
    Returns a tuple: (valid_transactions, invalid_count)
    """
    valid = []
    invalid_count = 0
    for t in transactions:
        if t.get("transaction_id") and t.get("amount") is not None:
            valid.append(t)
        else:
            invalid_count += 1
    return valid, invalid_count

def main():
    try:
        print("SALES ANALYTICS SYSTEM")

        # 1. Load sales data file
        print("[1/18] Loading sales data...")
        try:
            with open("data/sales_data.csv", "r", encoding="utf-8") as f:
                raw_data = f.readlines()
            print(f"Successfully read {len(raw_data)} transactions")
        except Exception as e:
            print(f"Error reading file: {e}")
            return

        # 2. Parse and clean transactions
        print("[2/18] Parsing and cleaning data...")
        transactions = parse_transactions(raw_data)
        print(f"Parsed {len(transactions)} transactions")

        # 3. Show filter options
        print("[3/18] Filter Options Available")
        regions = set(t.get("region") for t in transactions)
        amounts = [t.get("amount", 0) for t in transactions]
        print(f"Regions: {', '.join(regions)}")
        print(f"Amount Range: {min(amounts)} - {max(amounts)}")

        # Ask user for filter
        apply_filter = input("Do you want to filter data? (y/n): ").strip().lower()
        if apply_filter == "y":
            selected_region = input("Enter region to filter: ").strip()
            min_amount = float(input("Enter minimum amount: "))
            max_amount = float(input("Enter maximum amount: "))
            transactions = [
                t for t in transactions
                if t.get("region") == selected_region and min_amount <= t.get("amount", 0) <= max_amount
            ]

        # 4. Validate transactions
        print("[4/18] Validating transactions...")
        transactions, invalid_count = validate_transactions(transactions)
        print(f"Valid: {len(transactions)}  Invalid: {invalid_count}")

        # 5. Perform all data analyses
        print("[5/18] Analyzing sales data...")
        perform_all_analyses(transactions)
        print("Analysis complete")

        # 6. Fetch product data from API
        print("[6/18] Fetching product data from API...")
        products = fetch_product_data()
        print(f"Fetched {len(products)} products")

        # 7. Enrich sales data
        print("[7/18] Enriching sales data...")
        enriched_transactions = enrich_sales_data(transactions, products)
        print(f"Enriched {len(enriched_transactions)}/{len(transactions)} transactions ({len(enriched_transactions)/len(transactions)*100:.2f}%)")

        # 8. Save enriched data to file
        print("[8/18] Saving enriched data...")
        enriched_file_path = "data/enriched_sales_data.csv"
        with open(enriched_file_path, "w", encoding="utf-8") as f:
            for t in enriched_transactions:
                f.write(",".join(str(v) for v in t.values()) + "\n")
        print(f"Saved to: {enriched_file_path}")

        # 9. Generate report
        print("[9/18] Generating report...")
        report_file_path = "output/sales_report.txt"
        generate_report(enriched_transactions, report_file_path)
        print(f"Report saved to: {report_file_path}")

        print("[10/18] Process Complete!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
from utils.data_processor import parse_transactions, validate_transactions
from utils.enrichment import enrich_sales_data, save_enriched_data
from utils.analysis import perform_all_analyses
