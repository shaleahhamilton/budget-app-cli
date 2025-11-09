import json
import os

DATA_FILE = "budget_data.json"

# ---------- Storage ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "pay": {"frequency": "weekly", "amount": 0.0},  # weekly | biweekly
        "expenses": [],                                  # {name, amount_per_period}
        "savings_goal_per_period": 0.0
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ---------- Helpers ----------
def choose(options):
    while True:
        c = input("Choose option: ").strip().lower()
        if c in options:
            return c
        print(f"Please enter one of: {', '.join(sorted(options))}")

def get_float(prompt):
    while True:
        raw = input(prompt).strip().replace(",", "")
        try:
            return float(raw)
        except ValueError:
            print("Enter a number (e.g., 1200 or 45.50).")

def get_nonempty(prompt):
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print("Please enter a value.")

def period_label(freq):
    return "per week" if freq == "weekly" else "per pay (biweekly)"

# ---------- Core features ----------
def set_pay(data):
    print("\n--- Set Pay ---")
    print("1) Weekly")
    print("2) Biweekly (every 2 weeks)")
    choice = choose({"1", "2"})
    data["pay"]["frequency"] = "weekly" if choice == "1" else "biweekly"
    data["pay"]["amount"] = get_float(f"Net pay {period_label(data['pay']['frequency'])}: ")
    save_data(data)
    print("✅ Saved.")

def add_expense(data):
    print("\n--- Add Expense ---")
    name = get_nonempty("Expense name (e.g., Groceries, Gas): ")
    amt = get_float(f"Amount {period_label(data['pay']['frequency'])}: ")
    data["expenses"].append({"name": name, "amount_per_period": amt})
    save_data(data)
    print("✅ Added.")

def list_expenses(data):
    print("\n--- Expenses ---")
    if not data["expenses"]:
        print("No expenses yet.")
        return
    for i, e in enumerate(data["expenses"], 1):
        print(f"{i:>2}. {e['name']:<20} {e['amount_per_period']:>10.2f} ({period_label(data['pay']['frequency'])})")

def delete_expense(data):
    list_expenses(data)
    if not data["expenses"]:
        return
    idx = input("\nEnter the number to delete (or blank to cancel): ").strip()
    if not idx:
        print("Cancelled.")
        return
    if not idx.isdigit():
        print("Invalid number.")
        return
    idx = int(idx)
    if not (1 <= idx <= len(data["expenses"])):
        print("Out of range.")
        return
    removed = data["expenses"].pop(idx - 1)
    save_data(data)
    print(f"🗑️ Deleted: {removed['name']}.")

def set_savings_goal(data):
    print("\n--- Savings Goal ---")
    goal = get_float(f"Savings goal {period_label(data['pay']['frequency'])}: ")
    data["savings_goal_per_period"] = goal
    save_data(data)
    print("✅ Saved.")

def summary(data):
    print("\n=== Summary ===")
    freq = data["pay"]["frequency"]
    pay = float(data["pay"]["amount"])
    total_exp = sum(e["amount_per_period"] for e in data["expenses"])
    goal = float(data["savings_goal_per_period"])
    leftover = pay - total_exp
    progress = 0.0 if goal <= 0 else max(0.0, min(100.0, (leftover / goal) * 100))

    print(f"Pay frequency: {freq}")
    print(f"Net income {period_label(freq)}:       {pay:>10.2f}")
    print(f"Total expenses {period_label(freq)}:   {total_exp:>10.2f}")
    print(f"Leftover {period_label(freq)}:         {leftover:>10.2f}")
    print(f"Savings goal {period_label(freq)}:     {goal:>10.2f}")
    print(f"Goal coverage this period:             {(str(f'{progress:>9.1f}%') if goal>0 else '(set a goal to see %)')}")

    if data["expenses"]:
        print("\nTop expenses:")
        for e in sorted(data["expenses"], key=lambda x: -abs(x["amount_per_period"]))[:5]:
            print(f" - {e['name']:<20} {e['amount_per_period']:>10.2f}")

# ---------- Main menu ----------
def main():
    data = load_data()
    while True:
        print("\n=== Budget App ===")
        print("1) Set pay (weekly/biweekly + amount)")
        print("2) Add expense")
        print("3) List expenses")
        print("4) Delete an expense")
        print("5) Set savings goal")
        print("6) View summary")
        print("7) Quit")
        choice = choose({"1","2","3","4","5","6","7"})
        if choice == "1":
            set_pay(data)
        elif choice == "2":
            add_expense(data)
        elif choice == "3":
            list_expenses(data)
        elif choice == "4":
            delete_expense(data)
        elif choice == "5":
            set_savings_goal(data)
        elif choice == "6":
            summary(data)
        elif choice == "7":
            print("Goodbye! 👋🏾")
            break

if __name__ == "__main__":
    main()