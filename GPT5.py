# COM4018 — Fishing & Camping Equipment Hire System
# Tasks 1–3 (complete CLI) — No imports, single-file implementation.
#
# Features
# - Task 1: Main menu with input validation and loop until Exit.
# - Task 2: Hire entry subroutine: capture customer + hire details, validate inputs, store in-memory.
# - Task 3: Earnings report subroutine: show cumulative hires with totals and late-return extra charges.
#
# Note
# - No modules are imported (assignment restriction).
# - Data persists in-memory while the program runs (no files used).

# -----------------------------
# Read-only reference data
# -----------------------------
EQUIPMENT_ITEMS = [
    ("Day chairs", 15.00),
    ("Bed chairs", 25.00),
    ("Bite Alarm (set of 3)", 20.00),
    ("Bite Alarm (single)", 5.00),
    ("Bait Boat", 60.00),
    ("Camping tent", 20.00),
    ("Sleeping bag", 20.00),
    ("Rods (3lb TC)", 10.00),
    ("Rods (Bait runners)", 5.00),
    ("Reels (Bait runners)", 10.00),
    ("Camping Gas stove (Double burner)", 10.00),
]

# -----------------------------
# Mutable data (runtime state)
# -----------------------------
HIRES = []  # list of dicts, each representing one hire record


# -----------------------------
# Utility functions (no imports)
# -----------------------------

def format_money(amount):
    # Safely format a float as GBP with two decimals.
    # Avoid negative zero like -0.00.
    if -0.005 < amount < 0.005:
        amount = 0.0
    return "£" + ("%.2f" % amount)


def input_str(prompt):
    # Read a non-empty string.
    while True:
        s = input(prompt).strip()
        if s != "":
            return s
        print("Input cannot be empty. Please try again.")


def input_menu_choice(prompt, valid_choices):
    # Validate a menu choice string in valid_choices (e.g., {'1','2','3'}).
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print("Invalid choice. Please enter one of: " + ", ".join(sorted(valid_choices)))


def input_int(prompt, min_value=None, max_value=None):
    # Read an integer with optional min/max bounds.
    while True:
        s = input(prompt).strip()
        if s.startswith("+") and len(s) > 1:
            s = s[1:]
        if s == "":
            print("Please enter a number.")
            continue
        sign = 1
        if s.startswith("-"):
            sign = -1
            s = s[1:]
        if s.isdigit():
            val = sign * int(s)
            if min_value is not None and val < min_value:
                print("Value must be at least " + str(min_value) + ".")
                continue
            if max_value is not None and val > max_value:
                print("Value must be at most " + str(max_value) + ".")
                continue
            return val
        print("Invalid number. Please enter an integer.")


def input_yes_no(prompt):
    # Return True for yes, False for no.
    while True:
        s = input(prompt).strip().lower()
        if s in ("y", "yes"):
            return True
        if s in ("n", "no"):
            return False
        print("Please enter Y or N.")


def validate_phone(raw):
    # Simple phone validation: must contain only digits after removing spaces and common separators, length >= 7.
    s = ""
    for ch in raw:
        if ch in " -()+":
            continue
        s += ch
    if s.isdigit() and 7 <= len(s) <= 15:
        return True
    return False


# -----------------------------
# Cost calculations (per brief)
# -----------------------------

def base_sum_for_selection(selection):
    # Sum of full-price per-item costs times quantity (one night at full price)
    total = 0.0
    for idx, qty in selection.items():
        name, price = EQUIPMENT_ITEMS[idx]
        total += price * qty
    return total


def compute_total_cost(selection, nights, late_return):
    # Pricing rules:
    # - First night: full price per item.
    # - Each additional night: +50% of per-item cost.
    # - If returned after 14:00 (late_return = True): count as an additional night (extra +50%).
    base_night_sum = base_sum_for_selection(selection)
    additional_nights = 0
    if nights > 1:
        additional_nights = nights - 1
    late_extra_nights = 1 if late_return else 0
    extra_nights_total = additional_nights + late_extra_nights
    extra_cost = 0.5 * base_night_sum * extra_nights_total
    total = base_night_sum + extra_cost
    return total, (0.5 * base_night_sum if late_return else 0.0)


def selection_summary(selection):
    # Human-readable summary: "Item — qty; Item — qty"
    parts = []
    for idx in range(len(EQUIPMENT_ITEMS)):
        qty = selection.get(idx, 0)
        if qty > 0:
            parts.append(EQUIPMENT_ITEMS[idx][0] + " — " + str(qty))
    return "; ".join(parts)


# -----------------------------
# Task 2 — Hiring subroutine
# -----------------------------

def enter_hire():
    print("\n=== Enter Customer and Hire Details ===")

    # Customer fields
    customer_id = input_str("Customer ID: ")
    customer_name = input_str("Customer Name: ")

    # Phone validation
    while True:
        phone = input_str("Phone Number: ")
        if validate_phone(phone):
            break
        print("Phone must be 7–15 digits (spaces and +()- allowed). Please re-enter.")

    house_number = input_str("House Number: ")
    postcode = input_str("Postcode: ")
    card_ref = input_str("Credit/Debit Card (reference): ")

    # Equipment selection
    print("\nSelect equipment quantities (enter 0 if not needed):")
    selection = {}
    at_least_one = False
    for i, (name, price) in enumerate(EQUIPMENT_ITEMS):
        qty = input_int("  %2d) %s (%s) — quantity: " % (i + 1, name, format_money(price)), 0, 50)
        if qty > 0:
            selection[i] = qty
            at_least_one = True
    if not at_least_one:
        print("No equipment selected. Hire cancelled.")
        return

    # Nights and late return
    print("\nPricing rules:")
    print("- First night charged at full per-item price.")
    print("- Each additional night charged at +50% per item.")
    print("- If returned after 14:00 on the final day, an extra +50% per item is applied.")

    nights = input_int("Total number of nights kept (minimum 1): ", 1, 365)
    late = input_yes_no("Returned after 14:00 on the final day? (Y/N): ")

    total_cost, late_extra = compute_total_cost(selection, nights, late)

    # Store hire record
    hire = {
        "customer_id": customer_id,
        "customer_name": customer_name,
        "phone": phone,
        "house_number": house_number,
        "postcode": postcode,
        "card_ref": card_ref,
        "selection": selection,  # {item_index: qty}
        "nights": nights,
        "returned_on_time": (not late),
        "late_extra": late_extra,
        "total_cost": total_cost,
    }
    HIRES.append(hire)

    # Confirmation output
    print("\nHire recorded successfully:\n")
    print("Customer ID: ", customer_id)
    print("Name:        ", customer_name)
    print("Equipment:    ", selection_summary(selection))
    print("Nights:       ", nights)
    print("Returned on time: ", "Y" if not late else "N")
    print("Late extra:   ", format_money(late_extra))
    print("TOTAL COST:   ", format_money(total_cost))


# -----------------------------
# Task 3 — Earnings report subroutine
# -----------------------------

def earnings_report():
    print("\n=== Earnings Report ===")
    if len(HIRES) == 0:
        print("No hires recorded yet.")
        return

    # Header
    header_cols = [
        "Customer ID",
        "Equipment",
        "Number of nights",
        "Total cost",
        "Returned on time",
        "Extra charge (late)",
    ]
    # Simple column widths
    # Equipment column left wide; totals aligned.
    print("-" * 92)
    print(
        (
            (header_cols[0]).ljust(14)
            + (header_cols[1]).ljust(44)
            + (header_cols[2]).ljust(18)
            + (header_cols[3]).ljust(13)
            + (header_cols[4]).ljust(18)
            + (header_cols[5]).ljust(19)
        )[:92]
    )
    print("-" * 92)

    grand_total = 0.0
    for h in HIRES:
        equip = selection_summary(h["selection"])
        nights_str = str(h["nights"])  # total nights kept
        total_str = format_money(h["total_cost"])  # includes late effect
        on_time_str = "Y" if h["returned_on_time"] else "N"
        late_extra_str = format_money(h["late_extra"]) if h["late_extra"] > 0 else "-"
        grand_total += h["total_cost"]

        # Render row (truncate equipment if very long)
        equip_display = equip
        if len(equip_display) > 42:
            equip_display = equip_display[:39] + "..."
        row = (
            (h["customer_id"]).ljust(14)
            + equip_display.ljust(44)
            + nights_str.ljust(18)
            + total_str.ljust(13)
            + on_time_str.ljust(18)
            + late_extra_str.ljust(19)
        )
        print(row[:92])

    print("-" * 92)
    print("Grand total earnings: ", format_money(grand_total))


# -----------------------------
# Task 1 — Menu loop
# -----------------------------

def show_menu_and_get_choice():
    print("\n==============================")
    print(" Fishing & Camping Hire Shop ")
    print("==============================")
    print("1) Customer and hire details")
    print("2) Earnings report")
    print("3) Exit")
    return input_menu_choice("Select an option (1-3): ", {"1", "2", "3"})


def main():
    while True:
        choice = show_menu_and_get_choice()
        if choice == "1":
            # Task 2 — hiring flow
            enter_hire()
        elif choice == "2":
            # Task 3 — earnings report
            earnings_report()
        elif choice == "3":
            print("Exiting. Goodbye.")
            break
        # After action, loop continues back to the main menu.


if __name__ == "__main__":
    main()
