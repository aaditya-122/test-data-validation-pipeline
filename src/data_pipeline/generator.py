"""Generate repeatable synthetic customer and order datasets."""
from faker import Faker


def generate(count: int, profile: str = "standard", seed: int = 42):
    if not 1 <= count <= 100_000:
        raise ValueError("count must be between 1 and 100000")
    if profile not in {"standard", "edge-cases"}:
        raise ValueError("profile must be 'standard' or 'edge-cases'")
    fake = Faker()
    Faker.seed(seed)
    customers, orders = [], []
    for i in range(count):
        email = fake.unique.email().lower()
        customer = {"customer_id": f"C{i+1:06d}", "name": fake.name(), "email": email,
                    "age": fake.random_int(min=18, max=85), "country": fake.country_code()}
        if profile == "edge-cases":
            if i % 20 == 0: customer["age"] = 12
            elif i % 20 == 1: customer["email"] = "not-an-email"
            elif i % 20 == 2: customer["name"] = ""
            elif i % 20 == 3: customer["customer_id"] = "C000001"
        customers.append(customer)
        orders.append({"order_id": f"O{i+1:06d}",
                       "customer_id": "C999999" if profile == "edge-cases" and i % 25 == 0 else f"C{i+1:06d}",
                       "amount": -1.0 if profile == "edge-cases" and i % 25 == 1 else round(fake.pyfloat(min_value=1, max_value=5000, right_digits=2), 2)})
    return customers, orders
