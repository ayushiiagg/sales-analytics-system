def generate_report(data):
    total_revenue = 0
    revenue_by_region = {}

    for record in data:
        revenue = record["quantity"] * record["unit_price"]
        total_revenue += revenue

        region = record["region"]
        revenue_by_region[region] = revenue_by_region.get(region, 0) + revenue

    with open("output/sales_report.txt", "w") as file:
        file.write(f"Total Revenue: {total_revenue}\n")
        file.write("Revenue by Region:\n")

        for region, amount in revenue_by_region.items():
            file.write(f"{region}: {amount}\n")
from datetime import datetime
from collections import defaultdict

def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    with open(output_file, "w", encoding="utf-8") as f:

        # ===============================
        # 1. HEADER
        # ===============================
        now = datetime.now()
        f.write("SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {len(transactions)}\n\n")

        # ===============================
        # 2. OVERALL SUMMARY
        # ===============================
        total_revenue = sum(t["Quantity"] * t["UnitPrice"] for t in transactions)
        total_transactions = len(transactions)
        avg_order_value = total_revenue / total_transactions if total_transactions else 0

        dates = [t["Date"] for t in transactions]

        f.write("OVERALL SUMMARY\n")
        f.write(f"Total Revenue: {total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_transactions}\n")
        f.write(f"Average Order Value: {avg_order_value:,.2f}\n")
        f.write(f"Date Range: {min(dates)} to {max(dates)}\n\n")

        # ===============================
        # 3. REGION WISE PERFORMANCE
        # ===============================
        region_data = defaultdict(lambda: {"revenue": 0, "count": 0})

        for t in transactions:
            amount = t["Quantity"] * t["UnitPrice"]
            region_data[t["Region"]]["revenue"] += amount
            region_data[t["Region"]]["count"] += 1

        f.write("REGION WISE PERFORMANCE\n")
        f.write("Region | Sales | % of Total | Transactions\n")

        for region, data in sorted(region_data.items(), key=lambda x: x[1]["revenue"], reverse=True):
            percent = (data["revenue"] / total_revenue) * 100 if total_revenue else 0
            f.write(f"{region} | {data['revenue']:,.2f} | {percent:.2f}% | {data['count']}\n")

        f.write("\n")

        # ===============================
        # 4. TOP 5 PRODUCTS
        # ===============================
        product_data = defaultdict(lambda: {"qty": 0, "revenue": 0})

        for t in transactions:
            product_data[t["ProductName"]]["qty"] += t["Quantity"]
            product_data[t["ProductName"]]["revenue"] += t["Quantity"] * t["UnitPrice"]

        f.write("TOP 5 PRODUCTS\n")
        f.write("Rank | Product | Quantity | Revenue\n")

        top_products = sorted(product_data.items(), key=lambda x: x[1]["revenue"], reverse=True)[:5]

        for i, (name, data) in enumerate(top_products, 1):
            f.write(f"{i} | {name} | {data['qty']} | {data['revenue']:,.2f}\n")

        f.write("\n")

        # ===============================
        # 5. TOP CUSTOMERS
        # ===============================
        customer_data = defaultdict(lambda: {"spent": 0, "orders": 0})

        for t in transactions:
            amount = t["Quantity"] * t["UnitPrice"]
            customer_data[t["CustomerID"]]["spent"] += amount
            customer_data[t["CustomerID"]]["orders"] += 1

        f.write("TOP CUSTOMERS\n")
        f.write("Rank | CustomerID | Total Spent | Orders\n")

        top_customers = sorted(customer_data.items(), key=lambda x: x[1]["spent"], reverse=True)[:5]

        for i, (cid, data) in enumerate(top_customers, 1):
            f.write(f"{i} | {cid} | {data['spent']:,.2f} | {data['orders']}\n")

        f.write("\n")

        # ===============================
        # 6. DAILY SALES TREND
        # ===============================
        daily = defaultdict(lambda: {"revenue": 0, "count": 0, "customers": set()})

        for t in transactions:
            amount = t["Quantity"] * t["UnitPrice"]
            daily[t["Date"]]["revenue"] += amount
            daily[t["Date"]]["count"] += 1
            daily[t["Date"]]["customers"].add(t["CustomerID"])

        f.write("DAILY SALES TREND\n")
        f.write("Date | Revenue | Transactions | Unique Customers\n")

        for date in sorted(daily):
            d = daily[date]
            f.write(f"{date} | {d['revenue']:,.2f} | {d['count']} | {len(d['customers'])}\n")

        f.write("\n")

        # ===============================
        # 7. PRODUCT PERFORMANCE ANALYSIS
        # ===============================
        best_day = max(daily.items(), key=lambda x: x[1]["revenue"])

        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write(f"Best Selling Day: {best_day[0]} ({best_day[1]['revenue']:,.2f})\n")

        low_products = [p for p, d in product_data.items() if d["qty"] < 5]
        f.write(f"Low Performing Products: {', '.join(low_products) if low_products else 'None'}\n\n")

        # ===============================
        # 8. API ENRICHMENT SUMMARY
        # ===============================
        enriched_count = sum(1 for t in enriched_transactions if t.get("API_Match"))
        success_rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0

        failed_products = {t["ProductName"] for t in enriched_transactions if not t.get("API_Match")}

        f.write("API ENRICHMENT SUMMARY\n")
        f.write(f"Total Records Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")
        f.write(f"Failed Products: {', '.join(failed_products) if failed_products else 'None'}\n")
