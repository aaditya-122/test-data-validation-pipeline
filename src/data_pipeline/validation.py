"""Field, uniqueness, range, and reference validation."""
import re

EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def validate(customers, orders):
    issues = []
    ids, emails = set(), set()
    valid_customer_ids = set()
    for index, row in enumerate(customers, start=1):
        def issue(field, kind, detail):
            issues.append({"record_type":"customer", "record_id":row.get("customer_id", ""),
                           "row_number":index, "field":field, "error_type":kind, "detail":detail})
        required = ("customer_id", "name", "email", "age", "country")
        for field in required:
            if row.get(field) in (None, ""):
                issue(field, "missing_required", f"{field} is required")
        cid = row.get("customer_id")
        if cid in ids: issue("customer_id", "duplicate", "customer_id must be unique")
        elif cid: ids.add(cid); valid_customer_ids.add(cid)
        email = row.get("email", "")
        if email and not EMAIL.match(str(email)): issue("email", "invalid_format", "email must have a local part and dotted domain")
        elif email in emails: issue("email", "duplicate", "email must be unique")
        elif email: emails.add(email)
        age = row.get("age")
        if age is not None and (isinstance(age, bool) or not isinstance(age, int) or not 18 <= age <= 120):
            issue("age", "out_of_range", "age must be an integer from 18 to 120")
    for index, row in enumerate(orders, start=1):
        def issue(field, kind, detail):
            issues.append({"record_type":"order", "record_id":row.get("order_id", ""),
                           "row_number":index, "field":field, "error_type":kind, "detail":detail})
        if row.get("customer_id") not in valid_customer_ids:
            issue("customer_id", "foreign_key", "order references an unknown customer")
        amount = row.get("amount")
        if isinstance(amount, bool) or not isinstance(amount, (int, float)) or amount <= 0:
            issue("amount", "out_of_range", "amount must be a positive number")
    return issues

def valid_customers(customers, issues):
    invalid = {(i["record_type"], i["row_number"]) for i in issues}
    return [row for n, row in enumerate(customers, 1) if ("customer", n) not in invalid]

def valid_orders(orders, issues):
    invalid = {(i["record_type"], i["row_number"]) for i in issues}
    return [row for n, row in enumerate(orders, 1) if ("order", n) not in invalid]
