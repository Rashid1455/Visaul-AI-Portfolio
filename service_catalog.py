import json
from pathlib import Path

def load_catalog():
    return json.loads(Path(__file__).with_name("services.json").read_text(encoding="utf-8"))

def validate_selection(service_id, selection):
    catalog = load_catalog()
    if service_id not in catalog["services"]:
        raise ValueError("Unknown service.")
    service = catalog["services"][service_id]
    quantity = selection.get("quantity")
    if type(quantity) is not int or not 1 <= quantity <= 100:
        raise ValueError("Quantity must be between 1 and 100.")
    if selection.get("option") not in service["options"] or selection.get("dimensions") not in service["dimensions"]:
        raise ValueError("Choose an available option and size.")
    brief = selection.get("requirements", "")
    if not isinstance(brief, str) or not brief.strip() or len(brief) > 10000:
        raise ValueError("Enter project requirements (up to 10,000 characters).")
    custom = selection.get("custom_requirements", False)
    if type(custom) is not bool:
        raise ValueError("Invalid custom requirements selection.")
    duration = selection.get("duration_seconds")
    if service["kind"] == "video" and (type(duration) is not int or not 2 <= duration <= 300):
        raise ValueError("Video duration must be between 2 and 300 seconds; describe longer work in a custom request.")
    clean = dict(quantity=quantity, option=selection["option"], dimensions=selection["dimensions"], requirements=brief.strip(), custom_requirements=custom, duration_seconds=duration if service["kind"] == "video" else None)
    quote = custom or clean["dimensions"] == "Custom" or service["unit_price"] is None
    total = None if quote else service["unit_price"] * quantity * (duration if service["kind"] == "video" else 1)
    return clean, dict(currency=catalog["currency"], estimated_total=total, quote_required=quote)
