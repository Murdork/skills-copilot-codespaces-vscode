# ==========================================
# COM4018 – Fishing & Camping Hire System (Tasks 1–3)
# No imports. Money handled in integer pence.
#
# Pricing per item line:
#   • First night: 100% of daily rate × qty
#   • Additional nights: +50% per night × qty
#   • Late return (after 2pm): +50% once × qty
#
# Inputs:
#   • Customer header (ID first): id,name,phone,house_no,postcode,card_last4
#   • Nights: whole number ≥ 1
#   • Returned on time: y/n
#   • Items (repeat until blank): CODE,quantity  (NO space after comma)
# ==========================================

# -----------------------------
# Read-only equipment catalogue
# -----------------------------
CATALOG: tuple[dict[str, int | str], ...] = (
    {"code": "DCH", "name": "Day chairs",                           "daily_p": 1500},
    {"code": "BCH", "name": "Bed chairs",                           "daily_p": 2500},
    {"code": "BAS", "name": "Bite Alarm (set of 3)",                "daily_p": 2000},
    {"code": "BA1", "name": "Bite Alarm (single)",                  "daily_p":  500},
    {"code": "BBT", "name": "Bait Boat",                            "daily_p": 6000},
    {"code": "TNT", "name": "Camping tent",                         "daily_p": 2000},
    {"code": "SLP", "name": "Sleeping bag",                         "daily_p": 2000},
    {"code": "R3T", "name": "Rods (3lb TC)",                        "daily_p": 1000},
    {"code": "RBR", "name": "Rods (Bait runners)",                  "daily_p":  500},
    {"code": "REB", "name": "Reels (Bait runners)",                 "daily_p": 1000},
    {"code": "STV", "name": "Camping Gas stove (Double burner)",    "daily_p": 1000},
)

# -----------------------------
# In-memory store (per run)
# -----------------------------
HIRE_RECORDS: list[dict] = []   # each hire: header + computed lines

# -----------------------------
# Utilities
# -----------------------------
def money(pence: int) -> str:
    """Format integer pence as '£x.xx'."""
    pounds = pence // 100
    pp = pence % 100
    return f"£{pounds}.{pp:02d}"

def show_catalog() -> None:
    """Print the catalogue for reference."""
    print("\nAvailable equipment (read-only)")
    print("CODE  ITEM                                        RATE/NIGHT")
    print("----  ------------------------------------------  ----------")
    for it in CATALOG:
        print(f"{str(it['code']):<4}  {str(it['name']):<42}  {money(int(it['daily_p'])):>10}")
    print()

def find_item(code: str) -> dict | None:
    """Return catalogue dict by code or None."""
    c = code.strip().upper()
    for item in CATALOG:
        if item["code"] == c:
            return item
    return None

def catalog_codes() -> str:
    """Comma-separated list of valid equipment codes."""
    return ", ".join([str(it["code"]) for it in CATALOG])

def display_menu() -> None:
    print("\n=== Main Menu ===")
    print("1) Customer & hire details")
    print("2) Earnings report")
    print("3) Exit")

def read_choice() -> int | None:
    s = input("Enter choice (1-3): ").strip()
    if not s.isdigit():
        return None
    n = int(s)
    return n if n in (1, 2, 3) else None

def read_yes_no(prompt: str = "(y/n): ") -> str:
    while True:
        s = input(prompt).strip().lower()
        if s in ("y", "n", "yes", "no"):
            return "y" if s.startswith("y") else "n"
        print("Please enter 'y' or 'n'.")

def parse_csv_line(line: str) -> list[str]:
    """
    Simple CSV with optional quotes; trims spaces around fields.
    """
    fields: list[str] = []
    buf: list[str] = []
    in_quotes: bool = False
    quote_char: str = ""
    for ch in line:
        if in_quotes:
            if ch == quote_char:
                in_quotes = False
            else:
                buf.append(ch)
        else:
            if ch in ("'", '"'):
                in_quotes = True
                quote_char = ch
            elif ch == ",":
                fields.append("".join(buf).strip()); buf = []
            else:
                buf.append(ch)
    fields.append("".join(buf).strip())
    return fields

# -----------------------------
# Input: Customer + Hire header
# -----------------------------
def read_customer_header() -> dict | None:
    """
    Enter customer details (ID first). Blank line returns to menu.
      Format (6 fields):
        customer_id,name,phone,house_no,postcode,card_last4
      Example:
        101,Bob Barker,07970263076,3b,WA9 RY,1452
    """
    while True:
        raw = input("Customer (id,name,phone,house_no,postcode,card_last4) or blank to return: ").strip()
        if raw == "":
            return None
        parts = parse_csv_line(raw)
        if len(parts) != 6:
            print("  Expected 6 values. Try again.")
            continue

        cust_id, name, phone, house_no, postcode, last4 = parts
        if cust_id == "":
            print("  Customer ID is required.")
            continue
        digits_phone = "".join(ch for ch in phone if ch.isdigit())
        digits_card  = "".join(ch for ch in last4 if ch.isdigit())
        if len(digits_phone) < 7:
            print("  Phone must have at least 7 digits."); continue
        if len(digits_card) != 4:
            print("  Card last 4 must be exactly 4 digits."); continue

        return {
            "customer_id": cust_id,
            "customer_name": name,
            "phone": digits_phone,
            "house_no": house_no,
            "postcode": postcode,
            "card_last4": digits_card,
        }

def read_positive_int(prompt: str, min_value: int = 1) -> int:
    """Read integer >= min_value."""
    while True:
        s = input(prompt).strip()
        if not s.isdigit():
            print("Please enter a whole number."); continue
        n = int(s)
        if n < min_value:
            print(f"Please enter a number >= {min_value}."); continue
        return n

def read_item_lines(nights: int, returned_on_time: str) -> list[dict]:
    """
    Enter item lines: CODE,quantity  (NO space after comma; parser tolerant)
    Example: DCH,2
    """
    print("\nEnter item lines (one per line), then press ENTER on a blank line to finish.")
    print("Format: CODE,quantity   e.g.,  DCH,2")
    print(f"Nights for this hire: {nights}  | Returned on time: {returned_on_time}")
    print(f"Known codes: {catalog_codes()}")
    lines: list[dict] = []
    while True:
        raw = input("> ").strip()
        if raw == "":
            if len(lines) == 0:
                print("You must enter at least one item."); continue
            break
        parts = [p.strip() for p in parse_csv_line(raw)]
        if len(parts) != 2:
            print("Expected 2 fields: CODE,quantity"); continue
        code = parts[0].upper()
        item = find_item(code)
        if not item:
            print(f"Unknown code '{code}'. Known: {catalog_codes()}"); continue
        if not parts[1].isdigit():
            print("Quantity must be a whole number."); continue
        qty = int(parts[1])
        if qty < 1:
            print("Quantity must be >= 1."); continue

        # --- pricing for this line ---
        daily: int = int(item["daily_p"])
        first_night_p: int = daily * qty
        additional_n: int = max(0, nights - 1)
        additional_p: int = (daily * qty * additional_n) // 2
        late_extra_p: int = 0 if returned_on_time == "y" else (daily * qty) // 2
        line_total_p: int = first_night_p + additional_p + late_extra_p

        lines.append({
            "code": str(item["code"]),
            "name": str(item["name"]),
            "daily_p": daily,
            "qty": qty,
            "first_night_p": first_night_p,
            "additional_n": additional_n,
            "additional_p": additional_p,
            "late_extra_p": late_extra_p,
            "line_total_p": line_total_p,
        })
    return lines

# -----------------------------
# Hire workflow (loop to add another hire)
# -----------------------------
def run_hire_flow() -> None:
    show_catalog()
    print("Tip: Press Enter at the first prompt to return to the main menu.\n")

    while True:
        header = read_customer_header()
        if header is None:
            print("Returning to main menu.")
            return

        nights: int = read_positive_int("Number of nights (>=1): ", 1)
        returned_on_time: str = read_yes_no("Returned on time (y/n)? ")
        lines: list[dict] = read_item_lines(nights, returned_on_time)

        total_p: int = 0
        extra_delay_p: int = 0
        for ln in lines:
            total_p += int(ln["line_total_p"])
            extra_delay_p += int(ln["late_extra_p"])

        hire: dict = {
            "customer_id": header["customer_id"],
            "customer_name": header["customer_name"],
            "phone": header["phone"],
            "house_no": header["house_no"],
            "postcode": header["postcode"],
            "card_last4": header["card_last4"],
            "nights": nights,
            "returned_on_time": returned_on_time,  # 'y'/'n'
            "extra_delay_p": extra_delay_p,
            "total_p": total_p,
            "lines": lines,
        }
        HIRE_RECORDS.append(hire)

        items_summary = "; ".join([f"{ln['name']} - {ln['qty']}" for ln in lines])
        print("\nSaved hire:")
        print(f"  Customer ID: {hire['customer_id']}")
        print(f"  Equipment:   {items_summary}")
        print(f"  Number of nights: {nights}")
        print(f"  Returned on time: {returned_on_time}")
        print(f"  Extra charge for delayed return: {money(extra_delay_p)}")
        print(f"  Total charge: {money(total_p)}\n")

        if read_yes_no("Add another hire (y/n)? ") == "n":
            print("Returning to main menu.")
            return
        print()  # spacer before next capture

# -----------------------------
# Task 3B — Earnings report (simple fixed-width)
# -----------------------------
def earnings_report() -> None:
    """
    Generates and displays the earnings report (simple fixed-width layout).
    Columns:
      Customer ID | Equipment | Number Of Nights | Total Charge | Returned On Time (y/n) | Extra Charge For Delayed Return
    One line per hire; equipment shown as a single summary (name – qty; ...).
    """
    if not HIRE_RECORDS:
        print("\nNo hires recorded yet.")
        return

    print("\nEarnings Report:")
    # Header (fixed widths for clarity)
    print(
        f"{'Customer ID':<15}"
        f"{'Equipment':<60}"
        f"{'Number Of Nights':<18}"
        f"{'Total Charge':<15}"
        f"{'Returned On Time (y/n)':<25}"
        f"{'Extra Charge For Delayed Return':<30}"
    )

    for r in HIRE_RECORDS:
        equip_summary = "; ".join(f"{ln['name']} - {ln['qty']}" for ln in r["lines"])
        nights = str(r["nights"])
        total = money(int(r["total_p"]))
        on_time = str(r["returned_on_time"])  # 'y' / 'n'
        extra = money(int(r["extra_delay_p"]))
        cid = str(r["customer_id"])

        print(
            f"{cid:<15}"
            f"{equip_summary:<60}"
            f"{nights:<18}"
            f"{total:<15}"
            f"{on_time:<25}"
            f"{extra:<30}"
        )
    print()  # trailing newline

# -----------------------------
# Main loop (Task 1)
# -----------------------------
def main() -> None:
    while True:
        display_menu()
        choice = read_choice()
        if choice is None:
            print("Invalid option, try again.")
            continue
        if choice == 1:
            run_hire_flow()
        elif choice == 2:
            earnings_report()
        elif choice == 3:
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
