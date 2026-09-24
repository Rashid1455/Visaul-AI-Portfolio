"""Atomic private JSON storage with backup copies and retry-safe references."""
import json
import os
import re
import tempfile
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID
from service_catalog import validate_selection

def publish_json(path, record):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".pending-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(record, handle, ensure_ascii=False, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError:
            pass
    finally:
        Path(temporary).unlink(missing_ok=True)
    return json.loads(path.read_text(encoding="utf-8"))

def save_order(directory, order_id, details):
    reference = "ORD-" + str(UUID(order_id))
    selection, pricing = validate_selection(details.get("service_id"), details.get("selection", {}))
    customer = {}
    for field, limit in (("name",120), ("email",254), ("phone",40)):
        value = details.get("customer", {}).get(field, "")
        if not isinstance(value, str) or len(value)>limit or (field != "phone" and not value.strip()):
            raise ValueError(f"Enter a valid {field}.")
        customer[field] = value.strip()
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", customer["email"]):
        raise ValueError("Enter a valid email address.")
    if customer["phone"] and not re.fullmatch(r"[+\d() .-]{5,40}", customer["phone"]):
        raise ValueError("Enter a valid phone number or leave it empty.")
    if details.get("consent") is not True:
        raise ValueError("Please agree to storage of your request details.")
    record = dict(schema_version=2, order_id=reference, created_at=datetime.now(timezone.utc).isoformat(), service_id=details["service_id"], customer=customer, selection=selection, pricing=pricing, order_status="submitted", payment_status="unpaid", payment_reference=None, consent=True)
    directory = Path(directory).resolve()
    backup = Path(os.environ.get("PORTFOLIO_BACKUP_DIR", str(directory / "backups"))).resolve()
    project = Path(__file__).parent.resolve()
    for path in (directory, backup):
        if any(path.is_relative_to(project / name) for name in ("static","public","portfolio_uploads",".git")):
            raise ValueError("Order storage must be outside public asset directories.")
    backend = os.environ.get("PORTFOLIO_ORDER_BACKEND", "json")
    if backend == "sqlite":
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        with closing(sqlite3.connect(directory / "orders.sqlite3", timeout=30)) as database, database:
            database.execute("CREATE TABLE IF NOT EXISTS orders (id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
            database.execute("INSERT OR IGNORE INTO orders VALUES (?, ?)", (reference, json.dumps(record)))
            saved = json.loads(database.execute("SELECT payload FROM orders WHERE id = ?", (reference,)).fetchone()[0])
        publish_json(directory / f"{reference}.json", saved)
    elif backend == "json":
        saved = publish_json(directory / f"{reference}.json", record)
    else:
        raise ValueError("Unknown order storage backend.")
    publish_json(backup / f"{reference}.json", saved)
    return saved
