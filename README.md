# Inventory Demand Forecasting API

Backend API for inventory demand forecasting, stockout risk analysis, and replenishment recommendations.

This project is a **portfolio-safe version of a paid freelance commercial project**. The original work involved building an MVP backend tool for inventory and purchasing analytics. All client-identifying details, real business data, dataset contents, company names, supplier information, and commercially sensitive values have been intentionally removed or generalized.

The repository demonstrates the technical architecture, business logic, API design, and data-processing approach without exposing confidential client information.

---

## Project Context

Businesses that manage physical inventory often need quick answers to practical operational questions:

- Which products are selling fastest?
- What demand should be expected for the next 7, 14, or 30 days?
- Which products are at risk of running out of stock?
- How many units should be reordered?
- Which replenishment actions are urgent?
- Can purchasing recommendations be exported for further work?

The goal of this project was to build a simple backend MVP that turns inventory and sales data into actionable purchasing insights through REST API endpoints and CSV reports.

---

## My Role

I worked on the backend and data-processing part of the project, including:

- Designing the FastAPI service structure
- Implementing CSV-based data loading and validation
- Building analytics endpoints for sales and product data
- Implementing demand forecasting logic
- Implementing stockout risk calculation
- Implementing replenishment recommendation logic
- Adding filters for business users, such as category, warehouse, risk level, and priority
- Generating downloadable CSV reports
- Documenting API usage and project limitations

---

## Key Features

- REST API built with FastAPI
- CSV-based ERP-style data ingestion
- Product and inventory lookup endpoints
- Sales summary analytics
- Demand forecast for configurable time windows
- Stockout risk estimation
- Replenishment recommendation engine
- Order quantity rounding by pack size
- Filtering by category, warehouse, risk level, and priority
- Downloadable CSV report export
- Data quality check endpoint
- Interactive Swagger documentation

---

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pandas
- NumPy
- Pydantic
- CSV-based data processing

---

## Architecture Overview

```text
inventory-demand-api/
│
├── app/
│   ├── main.py
│   │
│   ├── data/
│   │   └── loader.py
│   │
│   ├── routers/
│   │   ├── analytics.py
│   │   ├── data_quality.py
│   │   ├── forecast.py
│   │   ├── inventory.py
│   │   ├── products.py
│   │   ├── replenishment.py
│   │   └── reports.py
│   │
│   └── services/
│       ├── analytics_service.py
│       ├── data_quality_service.py
│       ├── forecasting_service.py
│       ├── inventory_risk_service.py
│       ├── products_service.py
│       ├── replenishment_service.py
│       └── reporting_service.py
│
├── data/
│   ├── raw/
│   │   └── .gitkeep
│
├── requirements.txt
├── .gitignore
└── README.md
```

The project is organized into routers and service modules to keep API endpoints separate from business logic.

---

## Data Privacy Notice

Real client data is **not included** in this repository.

The original commercial task involved inventory, sales, supplier, and purchase-related data. These files may contain confidential business information, so they are excluded from the public portfolio version.

This repository only documents the expected input structure and the implemented logic. To run the project locally, use your own anonymized or synthetic CSV files with the expected schema.

Place input files in:

```text
data/raw/
```

Expected file names:

```text
products.csv
sales_daily.csv
current_inventory.csv
suppliers.csv
promotions.csv
purchase_orders.csv
```

---

## Expected Input Files

### `products.csv`

Product master data.

Expected columns:

```text
sku
product_name
category
supplier_id
order_pack_size
```

### `sales_daily.csv`

Daily sales history.

Expected columns:

```text
date
sku
warehouse_id
units_sold
revenue
```

### `current_inventory.csv`

Current stock levels by product and warehouse.

Expected columns:

```text
sku
warehouse_id
warehouse_name
on_hand_units
reserved_units
available_units
supplier_id
lead_time_days
```

### `suppliers.csv`

Supplier reference data.

Expected columns:

```text
supplier_id
supplier_name
```

### `purchase_orders.csv`

Open or historical purchase order data.

Expected columns:

```text
sku
warehouse_id
ordered_units
status
```

### `promotions.csv`

Promotion periods and discount information.

Expected columns:

```text
sku
start_date
end_date
discount_percent
```

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/inventory-demand-api.git
cd inventory-demand-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Add CSV files

Place anonymized or synthetic CSV files into:

```text
data/raw/
```

### 6. Run the API

```bash
uvicorn app.main:app --reload
```

API URL:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Returns basic service status.

---

### Products

```http
GET /products
GET /products/{sku}
```

Returns product information.

---

### Sales Analytics

```http
GET /analytics/sales-summary
GET /analytics/sales-summary?days=7
```

Returns sales summary for a selected period.

Example response fields:

```text
sku
product_name
category
units_sold
avg_daily_sales
revenue
```

---

### Demand Forecast

```http
GET /forecast
GET /forecast?days=7
GET /forecast/{sku}?days=30
```

Returns demand forecast based on recent sales.

Current MVP forecasting method:

```text
30-day moving average
```

Example response:

```json
{
  "forecast_days": 30,
  "method": "30_day_moving_average",
  "item": {
    "sku": "SKU-1001",
    "product_name": "Example Product",
    "category": "Example Category",
    "units_sold_30d": 1722,
    "avg_daily_sales": 57.4,
    "forecast_units": 1722
  }
}
```

---

### Stockout Risk

```http
GET /inventory/stockout-risk
GET /inventory/stockout-risk/{sku}
```

Available filters:

```http
GET /inventory/stockout-risk?risk_level=HIGH
GET /inventory/stockout-risk?category=ExampleCategory
GET /inventory/stockout-risk?warehouse_id=WH-01
GET /inventory/stockout-risk?risk_level=HIGH&category=ExampleCategory&limit=10
```

Risk levels:

```text
HIGH
MEDIUM
LOW
NO_DEMAND
```

Risk is calculated using:

- available stock
- average daily sales
- supplier lead time
- estimated days until stockout

---

### Replenishment Recommendations

```http
GET /replenishment/recommendations
GET /replenishment/recommendations/{sku}
```

Available filters:

```http
GET /replenishment/recommendations?priority=URGENT
GET /replenishment/recommendations?category=ExampleCategory
GET /replenishment/recommendations?warehouse_id=WH-01
GET /replenishment/recommendations?priority=URGENT&target_days=14&limit=10
```

Priority levels:

```text
URGENT
HIGH
NORMAL
NO_ORDER_NEEDED
```

The recommendation logic considers:

- forecasted demand for the target period
- expected demand during supplier lead time
- safety stock
- current available stock
- incoming purchase orders
- product order pack size

---

### CSV Report Export

```http
GET /reports/replenishment.csv
```

With filters:

```http
GET /reports/replenishment.csv?priority=URGENT
GET /reports/replenishment.csv?category=ExampleCategory
GET /reports/replenishment.csv?warehouse_id=WH-01
GET /reports/replenishment.csv?priority=URGENT&target_days=14
```

Returns a downloadable CSV file with replenishment recommendations.

---

### Data Quality Check

```http
GET /data/quality-check
```

Returns basic information about the input data:

- number of rows
- column names
- missing values
- duplicate rows
- sales date range
- number of products
- number of warehouses

---

## Business Logic

### Forecasting

The MVP uses a simple 30-day moving average approach:

```text
average_daily_sales = units_sold_last_30_days / 30
forecast_units = average_daily_sales * forecast_days
```

This method was chosen because it is explainable, easy to validate, and appropriate for an MVP version of an operational business tool.

---

### Stockout Risk

The system estimates how many days of stock are available:

```text
days_until_stockout = available_units / average_daily_sales
```

The result is compared with supplier lead time and risk thresholds to classify each product.

---

### Replenishment Quantity

Recommended order quantity is based on:

```text
target period demand
+ demand during supplier lead time
+ safety stock
- current available stock
- incoming stock
```

The final quantity is rounded up according to the product order pack size.

---

## Example Business Use Case

A purchasing manager wants to identify products that require urgent restocking.

They can call:

```http
GET /replenishment/recommendations?priority=URGENT&limit=20
```

The API returns products with:

- current stock
- average daily sales
- incoming stock
- supplier lead time
- recommended order quantity
- supplier reference

The same recommendations can be exported as a CSV report:

```http
GET /reports/replenishment.csv?priority=URGENT
```