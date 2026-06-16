# Inventory Demand Forecasting & Replenishment Demo Dataset

Synthetic but realistic dataset for a mini-ERP inventory demand forecasting and replenishment system.

## Files
- products.csv — product master data: SKU, category, supplier, price, cost, shelf life, reorder minimum, pack size.
- suppliers.csv — supplier lead time and basic purchasing constraints.
- sales_daily.csv — daily aggregated sales by SKU and warehouse from 2025-01-01 to 2026-06-14.
- current_inventory.csv — stock snapshot as of 2026-06-14.
- promotions.csv — promo periods with discount percentages.
- purchase_orders.csv — historical/recent purchase orders.

## Key use cases
- forecast demand for 7/14/30 days;
- detect SKUs likely to run out;
- calculate days of stock left;
- recommend replenishment quantities rounded to pack size;
- export reports by SKU/category/warehouse.

## Notes
The dataset intentionally includes:
- weekday/weekend effects;
- seasonality;
- promo-driven demand changes;
- stockouts and estimated lost sales;
- different supplier lead times;
- product category differences.
