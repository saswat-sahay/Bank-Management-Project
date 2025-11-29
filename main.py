import json
import random 
import string
from pathlib import Path

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

    def createAccount(self):
        info = {
            "name" : input("enter your name:- "),
            "age" : int(input("enter your age:- ")),
            "pin" : int(input("enter your 4 digit PIN:- ")),
            "accountNo" : Bank.__accountNumberGenerate(),
            "balance" : 0
        }

        if (info["age"] < 18 or info["age"] > 100) or len(str(info["pin"])) != 4:
            print("account cannot be created !")
        else:
            print("account created successfully !")
        
        for i in info:
            print(f"{i} : {info[i]}")
        print("Please note down your account number !")
        print("Please note down your PIN !")

        Bank.data.append(info)
        
        Bank.__update()

    def depositMoney(self):
        accNo = input("enter account number:- ")
        pin = int(input("enter your PIN:- "))
        userdata = [i for i in Bank.data if i["accountNo"] == accNo and i["pin"] == pin]

        if len(userdata) == 0:
            print("sorry no data found !")
        else:
            amount = int(input("how much money you want to deposit !"))
            if amount > 100000 or amount < 0:
                print("sorry the amount is too much | You can deposit between zero to 1 lakh !")
            else:
                userdata[0]["balance"] += amount
                Bank.__update()
                print("Amount Deposited Successfully !")
                print(f"Balance is: {userdata[0]["balance"]} !")

    def withdrawMoney(self):
        accNo = input("enter account number:- ")
        pin = int(input("enter your PIN:- "))
        userdata = [i for i in Bank.data if i["accountNo"] == accNo and i["pin"] == pin]

        if len(userdata) == 0:
            print("sorry no data found !")
        else:
            amount = int(input("how much money you want to withdraw !"))
            if userdata[0]["balance"] < amount or amount < 0:
                print("Amount is greater than your Bank balance !")
                print(f"Total available balance is: {userdata[0]["balance"]} !")
            else:
                print(userdata)
                userdata[0]["balance"] -= amount
                Bank.__update()
                print("Amount Withdraw Successfully !")

    def showDetails(self):
        accNo = input("enter your account number:- ")
        pin = int(input("enter your PIN:- "))

        userdata = [i for i in Bank.data if i["accountNo"] == accNo and i["pin"] == pin]
    
        if len(userdata) == 0:
            print("No such user found !")

        print("Here is your data: \n")
        for i in userdata[0]:
            print(f"{i} : {userdata[0][i]}")
    
    def updateDetails(self):
        accNo = input("enter you account number:- ")
        pin = int(input("enter you PIN:- "))

        userdata = [i for i in Bank.data if i["accountNo"] == accNo and i["pin"] == pin]
        
        if len(userdata) == 0:
            print("No such user found !")
        else:
            print("You can only change you name, age and PIN")
            print("Press 1 : change name")
            print("Press 2 : change age")
            print("Press 3 : change PIN")
            print("Press 4 : change multiple data")

        action = int(input("enter your action:- "))
        if action == 1:
            newName = input("enter your new name:- ")
            userdata[0]["name"] = newName
            print("name updated !")

        if action == 2:
            newAge = int(input("enter your new age:- "))
            userdata[0]["age"] = newAge
            print("age updated !")

        if action == 3:
            newPin = int(input("enter your new PIN:- "))
            userdata[0]["pin"] = newPin
            print("PIN updated !")
        if action == 4:
            print("Fill the details or leave it empty and press enter to skip !")

            newData = {
                "name" : input("enter new name or press enter to skip !"),
                "age" : input("enter new age or press enter to skip !"),
                "pin" : input("enter new PIN or press enter to skip !")
            }

            if newData["name"] == "":
                newData["name"] = userdata[0]["name"]

            if newData["age"] == "":
                newData["age"] = userdata[0]["age"]
                
            if newData["pin"] == "":
                newData["pin"] = userdata[0]["pin"]

            newData["accountNo"] = userdata[0]["accountNo"]     
            newData["balance"] = userdata[0]["balance"]    

            if type(newData["pin"]) == str:
                newData["pin"] = int(newData["pin"]) 

            for i in newData:
                if newData[i] == userdata[0][i]:
                    continue
                else:
                    userdata[0][i] = newData[i]
        Bank.__update()
        print("Details Updated !")

    def deleteAccount(self):
        accNo = input("enter your account number:- ")
        pin = int(input("enter your pin:- "))

        userdata = [i for i in Bank.data if i["accountNo"] == accNo and i["pin"] == pin]
    
        if len(userdata) == 0:
            print("No such user found !")
        else:
            check = input("press Y to Delete or N to Go back !")
            if check == 'n' or check == 'N':
                print("Your account is not deleted !")
            elif check == 'y' or check == 'Y':
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("account deleted successfully !")
        Bank.__update()

print("1 for create account")
print("2 for deposit money")
print("3 for withdrwal money")
print("4 for check user details")
print("5 for update user dtails")
print("6 for delete accoudnt")

user = Bank()
check = int(input("Enter Your Action:- "))

if check == 1:
    user.createAccount()
if check == 2:
    user.depositMoney()
if check == 3:
    user.withdrawMoney()
if check == 4:
    user.showDetails()
if check == 5:
    user.updateDetails()
if check == 6:
    user.deleteAccount()