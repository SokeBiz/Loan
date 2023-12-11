import mysql.connector as connection
mydb = connection.connect(host="127.0.0.1", user="root", password="", database="cooperative")
mycursor = mydb.cursor()

        # Creating the Database
# mycursor.execute("CREATE DATABASE IF NOT EXISTS cooperative")
# mycursor.execute("use mydatabase")

        # Create the db table
# mycursor.execute("create table society(ID int primary key auto_increment, fname char(20), lname char(20), username varchar(20), password varchar(20), membership char(10), contribution int(10), loanAmount int(10), interest int(3), balance int(10))")
        # Create treasury
# mycursor.execute("create table treasury(ID int primary key auto_increment, moneyIn int(10), moneyOut int(10), balance int (10))")

# query = "insert into treasury(moneyIn, moneyOut, balance) values (0, 0, 1000000)"
# mycursor.execute(query)


import time

class Loan:
    def __init__(self):
        mydb.commit()
        self.start()

    def start(self):
        print("""
              Welcome to Cooperative Society
              ENTER 1 to login
              ENTER 2 to register 
              """)
        action = input(">>>>> ")
        if action == "1": 
            self.login()
        elif action == "2":
            self.register()
        else: 
            print("Wrong Input, try again \n")
            time.sleep(3)
            self.start()
    
    def home(self):
        print("""
                What would you like to do?
                1. Deposit
                2. Check Balance
                3. Take a Loan
                4. Contribute
                5. Repay Loan
            """)
        do = input(">>>>> ")
        if do == "1":
            self.deposit()
        elif do == "2":
            self.checkBalance()
        elif do == "3":
            self.takeLoan()
        elif do == "4":
            self.contribute()
        elif do == "5":
            self.repay()
        else:
            self.home()

    def register(self):
        query = "insert into society(fname, lname, username, password, membership, contribution, loanAmount, interest, balance) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        fname = input("What is your first name: ")
        lname = input("what is your last name: ")
        username = input("Set a username: ")
        password = input("Set your password: ")
        memb = input("Would you like to become a member? YES or NO: ")
        if memb == "yes":
            self.member = "True"
        elif memb == "no":
            self.member = "False"
        info = (fname, lname, username, password, self.member, 0, 0, 0, 0)
        mycursor.execute(query, info)
        mydb.commit()
        self.login()
    
    def login(self):
        self.cred = input("Enter your username: ")
        self.call = "select * from society where username = %s"
        self.val = (self.cred, )
        mycursor.execute(self.call, self.val)
        self.user = mycursor.fetchone()
        # print(self.user)
        # print(self.user[9])
        if self.user is None:
            print("Invalid username, try again")
            self.login()
        self.passw = input("Enter your password: ")
        if self.passw in self.user[4]:
            print("Login Successful")
            self.home()
        else:
            print("Incorrect Password, please try again")
            time.sleep(1)
            self.login()
    
    def contribute(self):
        if self.user[5] == "True":
            self.con = input("Do you want to contribute? YES or NO: ")
            if self.con == "yes":
                self.contribute = input("How much would you like to contribute: ")
                if self.contribute.isdigit() == True:
                    self.contribute = int(self.contribute)
                    if self.contribute > 0 :
                        if self.user[9] >= self.contribute:    
                            conbal = self.user[6]
                            conbal = int(conbal)
                            newconbal = conbal + self.contribute
                            upc = "update society set contribution = %s where username = %s"
                            mycursor.execute(upc, (newconbal, self.cred))
                            balus = self.user[9]
                            balus = int(balus)
                            newbalus = balus - self.contribute
                            newbalus = int(newbalus)
                            upb = "update society set balance = %s where username = %s"
                            mycursor.execute(upb, (newbalus, self.cred))
                            mycursor.execute("select * from treasury")
                            result = mycursor.fetchall()
                            bal = result[-1][3]
                            newBal = self.contribute + bal
                            newBal = int(newBal)
                            uptre = "insert into treasury(moneyIn, moneyOut, balance) values (%s, 0, %s)"
                            mycursor.execute(uptre, (self.contribute, newBal))
                            mydb.commit()
                            print(f"You have successfully contributed {self.contribute}")
                        else: 
                            print("You do not have enough in your balance, please deposit")
                    else: 
                        print("Please enter a valid amount")
                else: 
                    print("Please enter a valid amount")
            else:
                self.contribute = 0
        else:
            pass
    
    def deposit(self):
        self.dep = input("How much would you like to deposit: ")
        if self.dep.isdigit() == True:
            self.dep = int(self.dep)
            if self.dep > 0:
                # self.call = f"select * from society where username = {'%s'}"
                # self.val = (self.cred, )
                # mycursor.execute(self.call, self.val)
                # self.user = mycursor.fetchone()
                # print(self.user)
                depamt = self.user[9]
                depamt = depamt + self.dep
                depamt = int(depamt)
                # print(depamt)
                updep = "update society set balance = %s where username = %s"
                mycursor.execute(updep, (depamt, self.cred))
                # print(depamt)
                mycursor.execute("select * from treasury")
                result = mycursor.fetchall()
                bal = result[-1][3]
                newBal = self.dep + bal
                newBal = int(newBal)
                uptre = "insert into treasury(moneyIn, moneyOut, balance) values (%s, 0, %s)"
                mycursor.execute(uptre, (self.dep, newBal))
                print("Successfully deposited")
                mydb.commit()
            else:
                print("You have deposit more than zero")
        else: 
            print("Invalid Input, please try again")
            self.deposit()
        
    def checkBalance(self): 
        print(f"""
              Your Balance is {self.user[9]}
              """)
    
    def takeLoan(self): 
        if self.user[6] > 0:
            pass
        else:  
            self.contribute()
        print("""
              Welcome to the loan service
              You can borrow up to the sum of 1,000,000.
              Interest is 3% for members with contribution
              Interest is 7% for members without contribution
              Interest is 10% for non-members without contribution
            """)
        amt = input("How much loan would you like to take?: ")
        if self.user[7] == 0:
            if amt.isdigit() == True:
                amt = int(amt)
                if  amt > 0:
                    if amt > 1000000 or amt == 0:
                        print("You have to borrow a valid amount")
                    else:
                        mycursor.execute("select * from treasury")
                        result = mycursor.fetchall()
                        bal = result[-1][3]
                        if amt > bal:
                            print("Loan is unavailable")
                        else:
                            if self.user[5] == "False":
                                interest = (10/100) * amt
                            elif self.user[5] == "True" and self.user[6] != 0:
                                interest = (3/100) * amt
                            elif self.user[5] == "True" and self.user[6] == 0:
                                interest = (7/100) * amt
                            amt += int(interest)
                            lam = self.user[7]
                            lam = amt + self.user[7]
                            upl = "update society set loanAmount = %s where username = %s"
                            mycursor.execute(upl, (lam, self.cred))
                            newBal = bal - amt
                            uptre = "insert into treasury(moneyIn, moneyOut, balance) values (0, %s, %s)"
                            mycursor.execute(uptre, (amt, newBal))
                            print(f"You have successfully taken a loan of {amt} with interest included")
                            mydb.commit()
                else:
                    print("Please enter a valid amount")
            else: 
                print("Please enter a valid amount")
        else:
            print(f"Sorry, You have to pay your outstanding loan of {self.user[7]}")
                
    def repay(self):
        print(f"You have an outstanding loan payment of {self.user[7]}")
        repay = input("How much would you like to repay now?: ")
        if repay.isdigit() == True:
            repay = int(repay)
            if repay > 0:
                if repay <= self.user[7]:
                    if self.user[9] >= repay: 
                        gbese = self.user[7]
                        gbese = gbese - repay
                        upl = "update society set loanAmount = %s where username = %s"
                        mycursor.execute(upl, (gbese, self.cred))
                        balus = self.user[9]
                        balus = int(balus)
                        newbalus = balus - repay
                        newbalus = int(newbalus)
                        upb = "update society set balance = %s where username = %s"
                        mycursor.execute(upb, (newbalus, self.cred))
                        mycursor.execute("select * from treasury")
                        result = mycursor.fetchall()
                        bal = result[-1][3]
                        newBal = repay + bal
                        uptre = "insert into treasury(moneyIn, moneyOut, balance) values (%s, 0, %s)"
                        mycursor.execute(uptre, (repay, newBal))
                        print(f"You have successfully repaid {repay}")
                        mydb.commit()
                    else:
                        print("You do not have enough money in your balance to pay the loan")
                else:
                    print("That amount is more than your loan deficit")  
            else:
                print("Please enter a valid amount")              
        else:
            print("Invalid Input, please try again \n")
            self.repay()
                      
    mydb.commit()
                    

Loan()
