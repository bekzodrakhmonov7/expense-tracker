import argparse
import json
from uuid import uuid4
import datetime

FILE = "expences.json"


def get_curr_expences():
    with open(file=FILE, mode="r") as file:
        expences = json.load(file)
    return expences


def add_expence(args):
    id = uuid4()
    expences = get_curr_expences()
    new_expence = {
        "id": str(id),
        "description": args.description,
        "amount": args.amount,
        "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="seconds"
        ),
    }
    expences.append(new_expence)
    with open(file=FILE, mode="w") as file:
        json.dump(expences, file, indent=4)
    print(f"Expense added successfully (ID: {id})")


def list_expences():
    expences = get_curr_expences()
    print(json.dumps(expences, indent=4))


def remove_expence(args):
    expences = get_curr_expences()
    new_expences = []
    for expence in expences:
        if expence["id"] != args.id:
            new_expences.append(expence)
    if expences == new_expences:
        print(f"The expence with id {args.id} does not exist")
    else:
        with open(file=FILE, mode="w") as file:
            json.dump(new_expences, file, indent=4)
        print("Expence was successfully removed")


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


def summarize_expences(args, months=MONTH_MAPPING):
    expences = get_curr_expences()
    total_amount = 0

    if args.month is None:
        for expence in expences:
            total_amount += expence["amount"]
        print(f"Total expences: ${total_amount}")
    else:
        if 12 < args.month < 0:
            print("Specified month exceeds the number of month in a year (1-12)")
            return
        for expence in expences:
            date = datetime.datetime.fromisoformat(expence["createdAt"])
            if date.month == args.month:
                total_amount += expence["amount"]
        print(f"Total amount spent in {months[args.month - 1]} is {total_amount}")


def main():
    parser = argparse.ArgumentParser(
        prog="Expence Tracker", description="CLI tool to track your expences"
    )
    subparsers = parser.add_subparsers(dest="command")

    add_subparser = subparsers.add_parser("add", help="Add expences")
    list_subparser = subparsers.add_parser("list", help="List expences")
    remove_subparser = subparsers.add_parser("remove", help="Remove expences")
    summary_subparser = subparsers.add_parser(
        "summary", help="Total amount of expences tacked"
    )

    add_subparser.add_argument(
        "-d", "--description", type=str, help="Description of expence", required=True
    )
    add_subparser.add_argument(
        "-a", "--amount", type=int, help="Amount spent", required=True
    )

    remove_subparser.add_argument(
        "--id", type=str, help="ID of an expence to remove", required=True
    )

    summary_subparser.add_argument(
        "-m", "--month", type=int, help="Month to specify", required=False
    )

    args = parser.parse_args()

    if args.command == "add":
        add_expence(args=args)
    elif args.command == "list":
        list_expences()
    elif args.command == "remove":
        remove_expence(args=args)
    elif args.command == "summary":
        summarize_expences(args)


if __name__ == "__main__":
    main()
