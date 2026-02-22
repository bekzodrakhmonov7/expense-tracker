# Expense tracker

---
CLI tool to track your expenses. With no external python library usage.

## Functionality

---

- Add expense to list
- Remove expense from list
- Summarize the total amount of expenses
- Summarize the expenses by month

## Usage

---

### Add expense

```bash
python main.py add --description "Movie ticket" --amount 7
```

Output:

```
Expense added successfully (ID: 6edbcc25-cc2d-4a5b-8d5a-54cec003d496)
```

### Remove expense

```bash
python main.py remove --id 6edbcc25-cc2d-4a5b-8d5a-54cec003d496
```

Output:

```
Expence was successfully removed
```

### Get total summary

```bash
python main.py summary
```

Output

```
Total expences: $7
```

### Get summary by month

```bash
python main.py summary --month 2
```

Output

```
Total amount spent in February is 7
```
