from app.data.loader import load_products


def get_all_products():
    products = load_products()
    return products.to_dict(orient="records")


def get_product_by_sku(sku: str):
    products = load_products()

    product = products[products["sku"] == sku]

    if product.empty:
        return None

    return product.iloc[0].to_dict()
