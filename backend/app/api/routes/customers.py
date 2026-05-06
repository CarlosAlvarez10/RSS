from fastapi import APIRouter
from app.db.repositories.customer_repository import CustomerRepository
from app.models.customer import Customer
from app.schemas.customer_schema import CustomerCreate
from app.utils.id_generator import new_id


router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("")
def create_customer(payload: CustomerCreate):
    customer = Customer(id=new_id("customer"), **payload.model_dump())
    return CustomerRepository().add(customer)


@router.get("")
def list_customers():
    return CustomerRepository().list()


@router.patch("/{customer_id}")
def update_customer(customer_id: str, payload: dict):
    return CustomerRepository().update(customer_id, **payload)
