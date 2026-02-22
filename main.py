import argparse
import json
from uuid import uuid4
import datetime

FILE = "expenses.json"


def get_curr_expenses():
    with open(file=FILE, mode="r") as file:
        expenses = json.load(file)
    return expenses


def add_expense(args):
    id = uuid4()
    expenses = get_curr_expenses()
    new_expense = {
        "id": str(id),
        "description": args.description,
        "amount": args.amount,
        "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="seconds"
        ),
        "updatedAt": None,
    }
    expenses.append(new_expense)
    with open(file=FILE, mode="w") as file:
        json.dump(expenses, file, indent=4)
    print(f"Expense added successfully (ID: {id})")


def list_expenses():
    expenses = get_curr_expenses()
    print(json.dumps(expenses, indent=4))


def remove_expense(args):
    expenses = get_curr_expenses()
    new_expenses = []
    for expense in expenses:
        if expense["id"] != args.id:
            new_expenses.append(expense)
    if expenses == new_expenses:
        print(f"The expense with id {args.id} does not exist")
    else:
        with open(file=FILE, mode="w") as file:
            json.dump(new_expenses, file, indent=4)
        print("expense was successfully removed")


MONTH_MAPPING = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def summarize_expenses(args, months=MONTH_MAPPING):
    expenses = get_curr_expenses()
    total_amount = 0

    if args.month is None:
        for expense in expenses:
            total_amount += expense["amount"]
        print(f"Total expenses: ${total_amount}")
    else:
        if 12 < args.month < 0:
            print("Specified month exceeds the number of month in a year (1-12)")
            return
        for expense in expenses:
            date = datetime.datetime.fromisoformat(expense["createdAt"])
            if date.month == args.month:
                total_amount += expense["amount"]
        print(f"Total amount spent in {months[args.month - 1]} is {total_amount}")


def edit_expense(args):
    expenses = get_curr_expenses()
    for expense in expenses:
        if expense["id"] == args.id:
            expense["description"] = args.description
            expense["updatedAt"] = datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat(timespec="seconds")
    with open(file=FILE, mode="w") as file:
        json.dump(expenses, file, indent=4)
    print("Expense was successfully edited")


def main():
    parser = argparse.ArgumentParser(
        prog="expense Tracker", description="CLI tool to track your expenses"
    )
    subparsers = parser.add_subparsers(dest="command")

    add_subparser = subparsers.add_parser("add", help="Add expenses")
    list_subparser = subparsers.add_parser("list", help="List expenses")
    remove_subparser = subparsers.add_parser("remove", help="Remove expenses")
    summary_subparser = subparsers.add_parser(
        "summary", help="Total amount of expenses tacked"
    )
    edit_subparser = subparsers.add_parser("edit", help="Edit existing expense")

    add_subparser.add_argument(
        "-d", "--description", type=str, help="Description of expense", required=True
    )
    add_subparser.add_argument(
        "-a", "--amount", type=int, help="Amount spent", required=True
    )

    remove_subparser.add_argument(
        "--id", type=str, help="ID of an expense to remove", required=True
    )

    summary_subparser.add_argument(
        "-m", "--month", type=int, help="Month to specify", required=False
    )

    edit_subparser.add_argument(
        "--id", type=str, help="ID of expense to edit", required=True
    )
    edit_subparser.add_argument(
        "-d",
        "--description",
        type=str,
        help="New description of expense",
        required=True,
    )

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args=args)
    elif args.command == "list":
        list_expenses()
    elif args.command == "remove":
        remove_expense(args=args)
    elif args.command == "summary":
        summarize_expenses(args)
    elif args.command == "edit":
        edit_expense(args)


if __name__ == "__main__":
    main()
