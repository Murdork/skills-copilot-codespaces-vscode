# Fishing and Camping Equipment Hire System
# Prices for equipment
prices = {
    'DCH': 15.0,  # Day chairs
    'BBT': 25.0,  # Bed chairs
    'SLP': 20.0,  # Sleeping bag
    'TNT': 20.0,  # Camping tent
    'STV': 10.0,  # Camping Gas stove
    'BAS': 20.0,  # Bite Alarm (set of 3)
    'BA1': 5.0,   # Bite Alarm (single)
    'R3T': 10.0,  # Rods (3lb TC)
    'RBR': 5.0,   # Rods (Bait runners)
    'REB': 10.0,  # Reels (Bait runners)
    'BCH': 60.0   # Bait Boat
}

# Global data storage
customers = []
customer_id_counter = 1

def calculate_cost(price, qty, nights, ontime):
    """Calculate the total cost and extra charge for an equipment hire."""
    discounted_cost = price * qty * (1 + 0.5 * (nights - 1))
    extra = 0.0
    if ontime == 'n':
        extra = 0.5 * price * qty
    return discounted_cost + extra, extra

def hire_equipment():
    """Handle hiring equipment for a customer."""
    global customer_id_counter
    customer_input = input("Enter customer details (Name,Phone,House,Postcode,Card): ")
    parts = customer_input.split(',')
    if len(parts) != 5:
        print("Invalid input. Expected 5 comma-separated values.")
        return
    name, phone, house, postcode, card = [p.strip() for p in parts]
    
    equipment = []
    while True:
        equip_input = input("Enter equipment (Code,Qty,Nights,Late,OnTime) or press Enter to finish: ")
        if not equip_input.strip():
            break
        parts = equip_input.split(',')
        if len(parts) != 5:
            print("Invalid input. Expected 5 comma-separated values.")
            continue
        code, qty_str, nights_str, late_str, ontime = [p.strip() for p in parts]
        try:
            qty = int(qty_str)
            nights = int(nights_str)
            late = int(late_str)
        except ValueError:
            print("Invalid numbers for Qty, Nights, or Late.")
            continue
        if code not in prices:
            print(f"Invalid equipment code: {code}")
            continue
        if ontime not in ['y', 'n']:
            print("OnTime must be 'y' or 'n'.")
            continue
        if qty <= 0 or nights <= 0:
            print("Qty and Nights must be positive integers.")
            continue
        
        price = prices[code]
        total_cost, extra = calculate_cost(price, qty, nights, ontime)
        
        equip = {
            'code': code,
            'qty': qty,
            'nights': nights,
            'late': late,
            'ontime': ontime,
            'cost': total_cost,
            'extra': extra
        }
        equipment.append(equip)
        print(f"Added {code} x{qty} for {nights} nights.")
    
    if equipment:
        customer = {
            'id': customer_id_counter,
            'name': name,
            'phone': phone,
            'house': house,
            'postcode': postcode,
            'card': card,
            'equipment': equipment
        }
        customers.append(customer)
        customer_id_counter += 1
        print(f"Customer {customer['id']} added successfully.")
    else:
        print("No equipment added. Customer not saved.")

def earnings_report():
    """Display the earnings report."""
    if not customers:
        print("No customers to report.")
        return
    
    print("\nEarnings Report")
    print("-" * 100)
    print(f"{'Customer ID':<12} {'Equipment Summary':<30} {'Nights':<8} {'Total Cost':<12} {'On Time':<8} {'Extra Charge':<12}")
    print("-" * 100)
    
    for cust in customers:
        equip_summary = '; '.join(f"{e['code']}-{e['qty']}" for e in cust['equipment'])
        max_nights = max(e['nights'] for e in cust['equipment'])
        total_cost = sum(e['cost'] for e in cust['equipment'])
        all_ontime = all(e['ontime'] == 'y' for e in cust['equipment'])
        ontime_str = 'y' if all_ontime else 'n'
        total_extra = sum(e['extra'] for e in cust['equipment'])
        
        print(f"{cust['id']:<12} {equip_summary:<30} {max_nights:<8} {total_cost:<12.2f} {ontime_str:<8} {total_extra:<12.2f}")

def main():
    """Main menu loop."""
    while True:
        print("\nMain Menu")
        print("1. Customer and hire details")
        print("2. Earnings report")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            hire_equipment()
        elif choice == '2':
            earnings_report()
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
