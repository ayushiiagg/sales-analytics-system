def clean_sales_data(records):
    valid_records = []
    invalid_count = 0
    total_records = len(records)

    for record in records:
        parts = record.split('|')

        # Check column count
        if len(parts) != 8:
            invalid_count += 1
            continue

        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts
def clean_sales_data(records):
    total_records = 0
    invalid_records = 0
    valid_records = []

    for record in records:
        record = record.strip()
        if not record or record.startswith("TransactionID"):
            continue

        total_records += 1
        parts = record.split('|')

        # Check column count
        if len(parts) != 8:
            invalid_records += 1
            continue

        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts

        # Invalid conditions
        if not transaction_id.startswith('T'):
            invalid_records += 1
            continue
        if not customer_id or not region:
            invalid_records += 1
            continue

        # Clean product name
        product_name = product_name.replace(',', '')

        # Clean numbers
        quantity = int(quantity)
        unit_price = float(unit_price.replace(',', ''))

        if quantity <= 0 or unit_price <= 0:
            invalid_records += 1
            continue

        valid_records.append({
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        })

    print(f"Total records parsed: {total_records}")
    print(f"Invalid records removed: {invalid_records}")
    print(f"Valid records after cleaning: {len(valid_records)}")

    return valid_records


def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries

    Returns: list of dictionaries
    """

    clean_transactions = []

    for line in raw_lines:
        parts = line.split('|')

        # Skip incorrect number of fields
        if len(parts) != 8:
            continue

        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts

        # Clean product name
        product_name = product_name.replace(',', '')

        # Clean and convert numeric fields
        try:
            quantity = int(quantity)
            unit_price = float(unit_price.replace(',', ''))
        except ValueError:
            continue

        transaction = {
            'TransactionID': transaction_id,
            'Date': date,
            'ProductID': product_id,
            'ProductName': product_name,
            'Quantity': quantity,
            'UnitPrice': unit_price,
            'CustomerID': customer_id,
            'Region': region
        }

        clean_transactions.append(transaction)

    return clean_transactions

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters

    Returns:
    tuple (valid_transactions, invalid_count, filter_summary)
    """

    valid_transactions = []
    invalid_count = 0

    # Show available regions
    regions = set()
    for txn in transactions:
        regions.add(txn.get('Region'))
    print("Available Regions:", regions)

    for txn in transactions:

        # Validation rules
        if (
            txn.get('Quantity') <= 0 or
            txn.get('UnitPrice') <= 0 or
            not txn.get('TransactionID', '').startswith('T') or
            not txn.get('ProductID', '').startswith('P') or
            not txn.get('CustomerID', '').startswith('C')
        ):
            invalid_count += 1
            continue

        amount = txn['Quantity'] * txn['UnitPrice']

        # Apply filters
        if region and txn['Region'] != region:
            continue
        if min_amount and amount < min_amount:
            continue
        if max_amount and amount > max_amount:
            continue

        valid_transactions.append(txn)

    filter_summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'final_count': len(valid_transactions)
    }

    return valid_transactions, invalid_count, filter_summary
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)
    """
    total_revenue = 0.0

    for txn in transactions:
        total_revenue += txn['Quantity'] * txn['UnitPrice']

    return total_revenue
def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns: dictionary with region statistics
    """
    region_stats = {}

    # Calculate totals and counts
    for txn in transactions:
        region = txn['Region']
        amount = txn['Quantity'] * txn['UnitPrice']

        if region not in region_stats:
            region_stats[region] = {
                'total_sales': 0,
                'transaction_count': 0
            }

        region_stats[region]['total_sales'] += amount
        region_stats[region]['transaction_count'] += 1

    # Calculate overall sales
    overall_sales = 0
    for stats in region_stats.values():
        overall_sales += stats['total_sales']

    # Calculate percentage contribution
    for region in region_stats:
        percentage = (region_stats[region]['total_sales'] / overall_sales) * 100
        region_stats[region]['percentage'] = round(percentage, 2)

    # Sort by total_sales descending
    region_stats = dict(
        sorted(
            region_stats.items(),
            key=lambda item: item[1]['total_sales'],
            reverse=True
        )
    )

    return region_stats
def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns: list of tuples
    (ProductName, TotalQuantity, TotalRevenue)
    """
    product_stats = {}

    for txn in transactions:
        product = txn['ProductName']
        qty = txn['Quantity']
        revenue = txn['Quantity'] * txn['UnitPrice']

        if product not in product_stats:
            product_stats[product] = {
                'quantity': 0,
                'revenue': 0.0
            }

        product_stats[product]['quantity'] += qty
        product_stats[product]['revenue'] += revenue

    product_list = []
    for product, data in product_stats.items():
        product_list.append((product, data['quantity'], data['revenue']))

    product_list.sort(key=lambda x: x[1], reverse=True)

    return product_list[:n]
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns: dictionary of customer statistics
    """
    customer_stats = {}

    for txn in transactions:
        customer = txn['CustomerID']
        product = txn['ProductName']
        amount = txn['Quantity'] * txn['UnitPrice']

        if customer not in customer_stats:
            customer_stats[customer] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }

        customer_stats[customer]['total_spent'] += amount
        customer_stats[customer]['purchase_count'] += 1
        customer_stats[customer]['products_bought'].add(product)

    for customer in customer_stats:
        total = customer_stats[customer]['total_spent']
        count = customer_stats[customer]['purchase_count']
        avg = total / count

        customer_stats[customer]['avg_order_value'] = round(avg, 2)
        customer_stats[customer]['products_bought'] = list(
            customer_stats[customer]['products_bought']
        )

    customer_stats = dict(
        sorted(
            customer_stats.items(),
            key=lambda item: item[1]['total_spent'],
            reverse=True
        )
    )

    return customer_stats
def daily_sales_trend(transactions):
    daily_data = {}

    for txn in transactions:
        date = txn['Date']
        customer = txn['CustomerID']
        revenue = txn['Quantity'] * txn['UnitPrice']

        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers': set()
            }

        daily_data[date]['revenue'] += revenue
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['unique_customers'].add(customer)

    for date in daily_data:
        daily_data[date]['unique_customers'] = len(
            daily_data[date]['unique_customers']
        )

    daily_data = dict(sorted(daily_data.items()))

    return daily_data
def find_peak_sales_day(transactions):
    daily_data = daily_sales_trend(transactions)

    max_revenue = 0
    peak_date = None
    peak_count = 0

    for date, stats in daily_data.items():
        if stats['revenue'] > max_revenue:
            max_revenue = stats['revenue']
            peak_date = date
            peak_count = stats['transaction_count']

    return (peak_date, max_revenue, peak_count)

def low_performing_products(transactions, threshold=10):
    product_summary = {}
    for txn in transactions:
        product = txn['ProductName']
        qty = txn['Quantity']
        revenue = txn['Quantity'] * txn['UnitPrice']

        if product not in product_summary:
            product_summary[product] = {
                'qty': 0,
                'revenue': 0.0
            }

        product_summary[product]['qty'] += qty
        product_summary[product]['revenue'] += revenue

    low_products = []
    for product, data in product_summary.items():
        if data['qty'] < threshold:
            low_products.append(
                (product, data['qty'], data['revenue'])
            )
    low_products.sort(key=lambda x: x[1])

    return low_products

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """

    enriched_transactions = []

    for txn in transactions:
        enriched_txn = txn.copy()

        try:
            # Extract numeric ProductID (P101 -> 101)
            product_id_str = txn.get("ProductID", "")
            numeric_id = int(product_id_str[1:])  # remove 'P'

            if numeric_id in product_mapping:
                api_product = product_mapping[numeric_id]

                enriched_txn["API_Category"] = api_product.get("category")
                enriched_txn["API_Brand"] = api_product.get("brand")
                enriched_txn["API_Rating"] = api_product.get("rating")
                enriched_txn["API_Match"] = True
            else:
                enriched_txn["API_Category"] = None
                enriched_txn["API_Brand"] = None
                enriched_txn["API_Rating"] = None
                enriched_txn["API_Match"] = False

        except Exception:
            enriched_txn["API_Category"] = None
            enriched_txn["API_Brand"] = None
            enriched_txn["API_Rating"] = None
            enriched_txn["API_Match"] = False

        enriched_transactions.append(enriched_txn)

    return enriched_transactions
def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file
    """

    with open(filename, "w") as file:
        # Header
        header = (
            "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|"
            "CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
        )
        file.write(header)

        for txn in enriched_transactions:
            line = (
                f"{txn.get('TransactionID')}|"
                f"{txn.get('Date')}|"
                f"{txn.get('ProductID')}|"
                f"{txn.get('ProductName')}|"
                f"{txn.get('Quantity')}|"
                f"{txn.get('UnitPrice')}|"
                f"{txn.get('CustomerID')}|"
                f"{txn.get('Region')}|"
                f"{txn.get('API_Category')}|"
                f"{txn.get('API_Brand')}|"
                f"{txn.get('API_Rating')}|"
                f"{txn.get('API_Match')}\n"
            )

            file.write(line)
def validate_transactions(transactions):
    """
    Simple validation: keeps transactions with transaction_id and amount.
    """
    valid = []
    invalid_count = 0
    for t in transactions:
        if t.get("transaction_id") and t.get("amount") is not None:
            valid.append(t)
        else:
            invalid_count += 1
    return valid, invalid_count

