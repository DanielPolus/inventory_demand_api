from fastapi import APIRouter, HTTPException

from app.services.products_service import get_all_products, get_product_by_sku


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("")
def read_products():
    return get_all_products()


@router.get("/{sku}")
def read_product(sku: str):
    product = get_product_by_sku(sku)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product