class Category:
    categories = set()

    # for the test to pass don't look if a category exsists already
    # which means if you create a category twice the first will be overwritten
    def __init__(self, category):
        # if category not in self.categories:
        self.category = category
        self.ledger = []
        self.categories.add(category)
        # print("Created new category:", category)
        # else:
        # print("Category exsist already.")

    def deposit(self, deposit, description=""):
        self.ledger.append({"amount": deposit, "description": description})

    def withdraw(self, withdrawl, description=""):
        if self.get_balance() >= withdrawl:
            self.ledger.append(
                {"amount": -withdrawl, "description": description})
            return True
        else:
            return False

    def get_balance(self):
        balance = float()
        for k in self.ledger:
            balance += k["amount"]
        return balance

    def transfer(self, transfer, category):
        name = category.__dict__['category']
        if name in self.categories:
            if self.withdraw(transfer, f"Transfer to {name}") is True:
                category.deposit(
                    transfer, f"Transfer from {self.category}")
                return True
            else:
                return False
        else:
            print("Error: the category your trying to " +
                  "transfer to does not exsist.")
            return False

    def check_funds(self, amount=0):
        if self.get_balance() >= amount:
            print("Enough funds in:", self.category)
            return True
        else:
            print("Not enough funds in:", self.category)
            return False

    def __str__(self):
        first_part = ((30 - len(self.category)) // 2) * "*"
        second_part = (30 - len(self.category) - len(first_part)) * "*"
        result = first_part + self.category + second_part + "\n"
        for item in self.ledger:
            description = item["description"][0:23]
            amount = str("{:.2f}".format(item["amount"]))[0:7]
            spaces = (30 - len(description) - len(amount)) * " "
            r = description + spaces + amount + "\n"
            result = result + r
        result = result + "Total: " + str(self.get_balance())
        return result


# percentage spent is a percentage from total spendings.
# categories is al list with the catogory objects
def create_spend_chart(categories):
    for category in categories:
        if category.__dict__['category'] not in Category.categories:
            print(
                f"Error: this category: {category.__dict__['category']},"
                + "not in your categories"
            )
            return "Error: a category is not in your categories"

    # create a list for total spendings per category (spendings)
    # and get the total of all spendings (tatal_spent)
    spendings = []
    total_spent = int()
    extra_length = int()
    for i in range(len(categories)):
        spendings.append(int())
        ledger = categories[i].ledger
        if len(categories[i].__dict__['category']) > extra_length:
            extra_length = len(categories[i].__dict__['category'])

        for entry in ledger:
            if entry["amount"] < 0:
                spendings[i] += entry["amount"]
                total_spent += entry["amount"]

    # get amount spent as a percentage from total spendings for each category
    percentages = []
    for i in range(len(spendings)):
        percentages.append(int())
        percentages[i] += spendings[i] / (total_spent / 100)

    # (print out for clarity)
    # print("categories", categories)
    # print("spendings:", spendings, "total spendings:", total_spent)
    # print("percentages:", percentages)

    # change categories to an iterable with the names of each (strings)
    categories = [category.__dict__['category'] for category in categories]
    categories = tuple(categories)

    # extra_length is the length from the longest word in categories, already
    # derived in a previous loop
    # the length from rows  will be 12 + extra_length (the amount of rows)
    # print("extra length:", extra_length)
    rows = []
    p = 100
    j = 0
    for i in range(12 + extra_length):
        rows.append(str())
        if i < 11:
            if p == 100:
                rows[i] += str(p) + "| "
            elif p == 0:
                rows[i] += "  " + str(p) + "| "
            else:
                rows[i] += " " + str(p) + "| "

            for perc in percentages:
                if perc >= p:
                    rows[i] += "o  "
                else:
                    rows[i] += "   "

            p -= 10
        elif i == 11:
            rows[i] += "    -"

            for perc in percentages:
                rows[i] += "---"
        else:
            rows[i] += "     "
            for category in categories:
                try:
                    rows[i] += category[j] + "  "
                except IndexError:
                    rows[i] += "   "
            j += 1

    # print(rows)
    chart = "Percentage spent by category\n"
    for row in rows:
        chart += row + "\n"

    chart = chart.rstrip("\n")

    # print(chart)
    return chart


# food = Category("food")
# food.deposit(900, "deposit")
# print(food.ledger)
# food.deposit(45.56)
# print(food.ledger)
# car = Category("car")
# car.deposit(2100, "a very long description: more funds")
# food.deposit(10.11)
# food.withdraw(10)
# food.withdraw(100, "for dinner")
# car.transfer(50, food)
# car.check_funds(10000)
# car.withdraw(500, "for insurance")
# print("food ledger:", food.ledger)
# print("car ledger:", car.ledger)
# print("categories:", Category.categories)
# print(food.get_balance())
# print(food, "\n")
# print(car, "\n")
# print(create_spend_chart([food, car]))
