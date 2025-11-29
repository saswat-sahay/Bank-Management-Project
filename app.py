import json
import random
import string
from pathlib import Path
import gradio as gr

class Bank:

    database = 'data.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("No such file Exists !")
    except Exception as err:
        print(f"An Exception Occured as {err}")

    @staticmethod
    def __update():
        with open(Bank.database, 'w') as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __accountNumberGenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%&*", k=1)
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)

    def createAccount(self, name, age, pin):
        info = {
            "name": name,
            "age": age,
            "pin": pin,
            "accountNo": Bank.__accountNumberGenerate(),
            "balance": 0
        }

        if (age < 18 or age > 100) or len(str(pin)) != 4:
            return "Account cannot be created — Age or PIN invalid!"

        Bank.data.append(info)
        Bank.__update()

        return (
            f"Account Created Successfully!\n"
            f"Name: {name}\nAge: {age}\nPIN: {pin}\n"
            f"Your Account Number: {info['accountNo']}"
        )

    def depositMoney(self, accNo, pin, amount):
        userdata = [i for i in Bank.data if i["accountNo"] == accNo and i["pin"] == pin]

        if len(userdata) == 0:
            return "User not found!"

        if amount > 100000 or amount < 0:
            return "Deposit amount must be between 0 and 100000!"

        userdata[0]["balance"] += amount
        Bank.__update()
        return f"Deposit Successful! New Balance: {userdata[0]['balance']}"

    def withdrawMoney(self, accNo, pin, amount):
        userdata = [i for i in Bank.data if i["accountNo"] == accNo and i["pin"] == pin]

        if len(userdata) == 0:
            return "User not found!"

        if amount > userdata[0]["balance"]:
            return f"Insufficient balance! Available: {userdata[0]['balance']}"

        userdata[0]["balance"] -= amount
        Bank.__update()
        return f"Withdrawal Successful! Remaining Balance: {userdata[0]['balance']}"

    def showDetails(self, accNo, pin):
        userdata = [i for i in Bank.data if i["accountNo"] == accNo and i["pin"] == pin]
        if len(userdata) == 0:
            return "User not found!"

        u = userdata[0]
        return f"""
Name: {u['name']}
Age: {u['age']}
PIN: {u['pin']}
Account No: {u['accountNo']}
Balance: {u['balance']}
"""

    def updateDetails(self, accNo, pin, new_name, new_age, new_pin):
        userdata = [i for i in Bank.data if i["accountNo"] == accNo and i["pin"] == pin]

        if len(userdata) == 0:
            return "User not found!"

        if new_name != "":
            userdata[0]["name"] = new_name
        if new_age != "":
            userdata[0]["age"] = int(new_age)
        if new_pin != "":
            userdata[0]["pin"] = int(new_pin)

        Bank.__update()
        return "Details updated successfully!"

    def deleteAccount(self, accNo, pin):
        userdata = [i for i in Bank.data if i["accountNo"] == accNo and i["pin"] == pin]

        if len(userdata) == 0:
            return "User not found!"

        Bank.data.remove(userdata[0])
        Bank.__update()
        return "Account Deleted Successfully!"


bank = Bank()


# ----------- GRADIO UI --------------

with gr.Blocks(title="Bank Management System") as ui:

    gr.Markdown("<h1>🏦 Bank Management System</h1>")

    with gr.Tab("Create Account"):
        name = gr.Textbox(label="Name")
        age = gr.Number(label="Age")
        pin = gr.Number(label="PIN (4 digits)")
        btn = gr.Button("Create Account")
        out = gr.Textbox()
        btn.click(bank.createAccount, [name, age, pin], out)

    with gr.Tab("Deposit Money"):
        acc = gr.Textbox(label="Account No")
        pin2 = gr.Number(label="PIN")
        amt = gr.Number(label="Amount")
        btn2 = gr.Button("Deposit")
        out2 = gr.Textbox()
        btn2.click(bank.depositMoney, [acc, pin2, amt], out2)

    with gr.Tab("Withdraw Money"):
        acc3 = gr.Textbox(label="Account No")
        pin3 = gr.Number(label="PIN")
        amt3 = gr.Number(label="Amount")
        btn3 = gr.Button("Withdraw")
        out3 = gr.Textbox()
        btn3.click(bank.withdrawMoney, [acc3, pin3, amt3], out3)

    with gr.Tab("Show Details"):
        acc4 = gr.Textbox(label="Account No")
        pin4 = gr.Number(label="PIN")
        btn4 = gr.Button("Show")
        out4 = gr.Textbox()
        btn4.click(bank.showDetails, [acc4, pin4], out4)

    with gr.Tab("Update Details"):
        acc5 = gr.Textbox(label="Account No")
        pin5 = gr.Number(label="PIN")
        uname = gr.Textbox(label="New Name (optional)")
        uage = gr.Textbox(label="New Age (optional)")
        upin = gr.Textbox(label="New PIN (optional)")
        btn5 = gr.Button("Update")
        out5 = gr.Textbox()
        btn5.click(bank.updateDetails, [acc5, pin5, uname, uage, upin], out5)

    with gr.Tab("Delete Account"):
        acc6 = gr.Textbox(label="Account No")
        pin6 = gr.Number(label="PIN")
        btn6 = gr.Button("Delete")
        out6 = gr.Textbox()
        btn6.click(bank.deleteAccount, [acc6, pin6], out6)


ui.launch()
