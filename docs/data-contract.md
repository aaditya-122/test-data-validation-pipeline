# Data contract

## Customer

| Field | Type | Rule |
| --- | --- | --- |
| `customer_id` | string | Required and unique |
| `name` | string | Required, non-empty |
| `email` | string | Required, syntactically plausible, unique |
| `age` | integer | 18 through 120 inclusive |
| `country` | string | Required ISO-style two-character country code |

## Order

| Field | Type | Rule |
| --- | --- | --- |
| `order_id` | string | Required and unique in generated fixtures |
| `customer_id` | string | Must reference a valid customer |
| `amount` | number | Greater than zero |

## Profile behavior

`standard` generates valid fixtures. `edge-cases` injects age below range, malformed email, missing name, duplicate customer ID, unknown customer references, and negative amounts at deterministic intervals. The `seed` makes Faker-generated values reproducible.

## Reports

`validation-summary.json` contains profile, seed, input sizes, affected row counts, issue count, and overall status. `validation-issues.csv` contains one row per validation finding. A row with multiple defects appears multiple times. `--persist` writes only rows with no validation findings.
