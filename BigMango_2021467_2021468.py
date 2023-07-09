import datetime
import mysql.connector
mydb= mysql.connector.connect(host='localhost', password='kartikeya2003', user='root', database='bigmango')
if mydb.is_connected():
    print("Connection Established")

mycursor=mydb.cursor()

def Admin():
    usrnm = input("Enter username: ")
    passwd = input("Enter Password: ")
    aid = input("Enter your id: ")
    mycursor.execute("select * from admin where username=%s and password=%s and A_id=%s",(usrnm,passwd,aid))
    myrecords=mycursor.fetchall()
    if(len(myrecords)==0):
        print("No Admin found")
        return
    else:
        print("Welcome ",usrnm,"!!");
        admctrl=True
        while(admctrl):
            print("=<< 1. Approve Product >>=")
            print("=<< 2. UnApprove Product >>=")
            print("=<< 3. Get monthly number of orders >>=")
            print("=<< 4. Get total approved products >>=")
            print("=<< 5. Get total sales for each product sold by each seller and grand total of total sales >>=")
            print("=<< 6. Get monthly sales >>=")
            print("=<< 7. Exit >>=")
            ch=input("Enter choice: ")
            if(ch=='1'):
                pid=int(input("Enter product id to approve: "))
                mycursor.execute("update product set approved=1 where P_id=%s",(pid,))
                mydb.commit()
            elif(ch=='2'):
                pid=int(input("Enter product id to Unapprove: "))
                mycursor.execute("update product set approved=0 where P_id=%s",(pid,))
                mydb.commit()
            elif(ch=='3'):
                mycursor.execute("Select Year(date) as Year , Month(date) as Month, count(*) from order_detail group by year, month with rollup")
                rcrd = mycursor.fetchall()
                print("Year \t Month \t Number")
                for i in rcrd:
                    if(i[1]=="None"):
                        print("Total in ",i[0]," = ",i[2])
                        continue
                    print(i[0],"\t",i[1],"\t",i[2])
                print()
            elif(ch=='4'):
                mycursor.execute("select P_name as product , sum(P_quantity) as tot_quantity from product where approved=1 group by P_name with rollup")
                rcrd=mycursor.fetchall()
                print("Product \t tot_quantity")
                for i in rcrd:
                    print(i[0],"\t",i[1])
                print()
            elif(ch=='5'):
                mycursor.execute("select P.P_name as product , S.username as Seller, sum(C.Quantity) as tot_quantity, sum(C.tot_amt) as total_sales \
                                 from cart c inner join adds A on c.C_id=A.C_id \
                                 inner join product P on A.P_id = P.P_id \
                                 inner join seller S on P.S_id = S.S_id \
                                 group by P.P_name , S.username with rollup")
                rcrd = mycursor.fetchall()
                print()
                print("Product \t Seller \t tot_quantity \t total_sales")
                for i in rcrd:
                    print(i[0]," ",i[1]," ",i[2]," ",i[3])
                print()
            elif(ch=='6'):
                mycursor.execute("select Year(date) as year , Month(date) as month, sum(tot_amt) from order_detail group by year, month with rollup")
                rcrd = mycursor.fetchall()
                print("Year \t Month \t tot_sales")
                for i in rcrd:
                    print(i[0],"\t",i[1],"\t",i[2])
                print()
            elif(ch=='7'):
                admctrl=False
            else:
                print("Enter choice from above given choices")


def Seller():
    control=True
    while(control):
        print("=<< 1. SignUp >>=")
        print("=<< 2. LogIn >>=")
        print("=<< 3. Exit >>=")
        c=input("Enter your choice: ")
        if(c=='1'):
            a=0
            usrnm=""
            while(a==0):
                usrnm=input("Enter username: ")
                mycursor.execute("select * from seller where username=%s",(usrnm,))
                rcrd=mycursor.fetchall()
                if(len(rcrd)==0):
                    a=1
                else:
                    print("Username already chosen")
                    print("try again")
            pswd=""
            t=1
            while(t==1):
                pswd= input("Enter password: ")
                pswdchk = input("ReEnter password: ")
                if(pswd!=pswdchk):
                    print("Both passwords does not match try again!!")
                else:
                    t=0
            mycursor.execute("Select max(S_id) from seller")
            rcrd=mycursor.fetchall()
            sid=1
            if(rcrd[0][0]!=None):
                sid=rcrd[0][0]+1
            mycursor.execute("Insert into seller values(%s,%s,%s,%s)",(sid,usrnm,pswd,1))
            mydb.commit()
            print("You are Regitered!!")
            print("Now Login again !! ")
            print("\n \n \n")
        elif (c=='2'):
            usrnm= input("Enter username: ")
            pswd = input("Enter password: ")
            mycursor.execute("select * from seller where username=%s and password=%s",(usrnm,pswd))
            rcrd=mycursor.fetchall()
            s_id=-1
            if(len(rcrd)==0):
                print("Seller not found with given username and password")
            else:
                s_id=rcrd[0][0]
                print("Welcome ",usrnm,"!!!")
                selcntr=True
                while(selcntr):
                    print("=<< 1. Sell Product >>=")
                    print("=<< 2. Add Quantity >>=")
                    print("=<< 3. Update Price >>=")
                    ch= input("Enter choice: ")
                    if(ch=='1'):
                        pid=1
                        mycursor.execute("select max(P_id) from seller")
                        rcrd=mycursor.fetchall()
                        if(rcrd[0][0]!=None):
                            pid=rcrd[0][0]+1
                        pname=input("Enter name of the product: ")
                        price=int(input("Enter name of the product: "))
                        stk=int(input("Enter the stock: "))
                        mycursor.execute("insert into product values(%s,%s,%s,%s,%s,%s,%s)",(pid,pname,price,stk,s_id,1,0))
                        mydb.commit()
                    elif(ch=='2'):
                        pid=int(input("Enter the product id: "))
                        amt = int(input("Enter the Quantity to add: "))
                        mycursor.execute("select * from product where P_id=%s and S_id=%s",(pid,s_id))
                        rcrd=mycursor.fetchall()
                        if(len(rcrd)==0):
                            print("You dont sell this product or the product is not available")
                        else:
                            mycursor.execute("update product set P_quantity=P_quantity+%s where P_id=%s",(amt,pid))
                            mydb.commit()
                    elif(ch=='3'):
                        pid=int(input("Enter the product id: "))
                        price = int(input("Enter the updated price: "))
                        mycursor.execute("select * from product where P_id=%s and S_id=%s",(pid,s_id))
                        rcrd=mycursor.fetchall()
                        if(len(rcrd)==0):
                            print("You dont sell this product or the product is not available")
                        else:
                            mycursor.execute("update product set P_price=%s where P_id=%s",(price,pid))
                            mydb.commit()
                    else:
                        print("Enter choice from above given choices: ")
                        
        elif(c=='3'):
            control=False
        else:
            print("Enter choice from above given choices: ")


def Customer():
    
    control=True
    while(control):
        print("=<< 1. SignUp >>=")
        print("=<< 2. LogIn >>=")
        print("=<< 3. Exit >>=")
        c=input("Enter your choice: ")
        if(c=='1'):
            a=0
            usrnm=""
            while(a==0):
                usrnm=input("Enter username: ")
                mycursor.execute("select * from customer where username=%s",(usrnm,))
                rcrd=mycursor.fetchall()
                if(len(rcrd)==0):
                    a=1
                else:
                    print("Username already chosen")
                    print("try again")
            
            fn = input("Enter your firstname: ")
            ln = input("Enter your lastname: ")
            strt= input("Enter your street: ")
            cty= input("Enter your city: ")
            sta= input("Enter your state: ")
            zc= int(input("Enter your zipcode: "))
            pswd=""
            t=1
            while(t==1):
                pswd= input("Enter password: ")
                pswdchk = input("ReEnter password: ")
                if(pswd!=pswdchk):
                    print("Both passwords does not match try again!!")
                else:
                    t=0
            mycursor.execute("Select max(C_id) from customer")
            rcrd=mycursor.fetchall()
            cid=1
            if(rcrd[0][0]!=None):
                cid=rcrd[0][0]+1
            mycursor.execute("Insert into customer values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(cid,fn,ln,usrnm,pswd,strt,cty,sta,zc))
            mydb.commit()
            print("You are Regitered!!")
            print("Now Login again !! ")
            print("\n \n \n")
        elif(c=='2'):
            usrnm=input("Enter username: ")
            passwd = input("Enter password: ")
            mycursor.execute("select * from customer where username=%s and password=%s",(usrnm,passwd))
            rcrd=mycursor.fetchall()
            c_id=-1
            if(len(rcrd)==0):
                print("No customer found with given username and password")
            else:
                c_id=rcrd[0][0]
                print("Welcome ",usrnm,"!!!")
                custcont=True
                while(custcont):
                    print("=<< 1. Explore Products >>=")
                    print("=<< 2. Search for Product >>=")
                    print("=<< 3. Add to Cart >>=")
                    print("=<< 4. See cart items >>=")
                    print("=<< 5. Remove from Cart >>=")
                    print("=<< 6. Place Order >>=")
                    print("=<< 7. Exit >>=")
                    ch=input("Enter choice: ")
                    if(ch=='1'):
                        mycursor.execute("select P_id,P_name,P_price,P_quantity from product where approved=1")
                        rcrd=mycursor.fetchall()
                        print("P_id \t Name \t Price \t StockAvailable")
                        for i in rcrd:
                            print(i[0],"\t",i[1],"\t",i[2],"\t",i[3])
                    elif(ch=='2'):
                        nm=input("Enter product name to search: ")
                        mycursor.execute("select * from product where P_name=%s and approved=1",(nm,))
                        rcrd=mycursor.fetchall()
                        if(len(rcrd)==0):
                            print("Sorry we dont have ",nm)
                        else:
                            print("Here is the product detail")
                            for i in rcrd:
                                print("P_id= ",i[0],"  Name= ",i[1],"  Price= ",i[2],"  StockAvailable= ",i[3])
                    elif(ch=='3'):
                        mycursor.execute("select * from cart where C_id=%s",(c_id,))
                        rcrd=mycursor.fetchall()
                        if(len(rcrd)==0):
                            mycursor.execute("Insert into cart values(%s,%s,%s,%s)",(c_id,c_id,0,0))
                            mydb.commit()
                        pid=int(input("Enter id of the product you want to add: "))
                        q=int(input("Enter the quantity you want to add: "))
                        mycursor.execute("select * from product where P_id=%s",(pid,))
                        rcrd=mycursor.fetchall()
                        if(len(rcrd)==0):
                            print("Product is not available")
                        else:
                            if(rcrd[0][3]<q):
                                print("Less Stock Available")
                            else:
                                mycursor.execute("insert into adds values(%s,%s,%s,%s)",(c_id,c_id,pid,q)) #trigger is already created 
                                mydb.commit()
                    elif (ch=='4'):
                        mycursor.execute("select P.P_id,P_name,P_price,quantity from adds as A,product as P where A.P_id=P.P_id and C_id=%s",(c_id,))
                        rcrd=mycursor.fetchall()
                        if(len(rcrd)==0):
                            print("Cart is Empty")
                        else:
                            for i in rcrd:
                                print(i)  
                    elif(ch=='5'):
                        pid=int(input("Enter id of the product you want to remove: "))
                        mycursor.execute("Select * from adds where P_id=%s and C_id=%s",(pid,c_id))
                        rcrd=mycursor.fetchall()
                        if(len(rcrd)==0):
                            print("Cart does not contain this product")
                        else:
                            tot_q=0;
                            for i in rcrd:
                                tot_q+=i[3]
                            mycursor.execute("select P_price from product where P_id=%s",(pid,))
                            rcrd=mycursor.fetchall()
                            price=rcrd[0][0]
                            
                            t_amt=price*tot_q;
                            mycursor.execute("Update cart set tot_amt=tot_amt-%s and Quantity=Quantity-%s where C_id=%s",(t_amt,tot_q,c_id))
                            mydb.commit()
                            mycursor.execute("delete from adds where P_id=%s and C_id=%s",(pid,c_id))
                            mydb.commit()
                            mycursor.execute("Update product set P_quantity=P_quantity+%s where P_id=%s",(tot_q,pid))
                            mydb.commit()
                            print("Product Removed")
                            print()

                    elif(ch=='6'):
                        mycursor.execute("Select Quantity from cart where C_id=%s",(c_id,))
                        rcrd=mycursor.fetchall()
                        if(rcrd[0][0]==0):
                            print("Cart is Empty")
                            print("Cant Place order")
                            print()
                        else:
                            mycursor.execute("Select max(pay_id) from payment")
                            rcrd=mycursor.fetchall()
                            pay_id=1
                            if(rcrd[0][0]!=None):
                                pay_id=rcrd[0][0]+1
                            mycursor.execute("select * from cart where C_id=%s",(c_id,))
                            rcrd=mycursor.fetchall()
                            cart_id=rcrd[0][0]
                            amt=rcrd[0][3]
                            now = datetime.datetime.now()
                            f_date=now.strftime('%Y-%m-%d')

                            mode=input("Enter the mode of payment: ")
                            mycursor.execute("Insert into payment values(%s,%s,%s,%s,%s,%s)",(pay_id,mode,f_date,amt,c_id,cart_id))
                            mydb.commit()
                            mycursor.execute("delete from adds where C_id=%s",(c_id,))
                            mydb.commit()
                            mycursor.execute("Update cart set Quantity=%s, tot_amt=%s where C_id=%s",(0,0,c_id))
                            mydb.commit()
                            now = datetime.datetime.now() + datetime.timedelta(days=7)
                            exp_del=now.strftime('%Y-%m-%d')
                            mycursor.execute("select max(Ord_no) from order_detail")
                            rcrd=mycursor.fetchall()
                            ord_no=1;
                            if(rcrd[0][0]!=None):
                                ord_no=rcrd[0][0]+1
                            mycursor.execute("Insert into order_detail Values(%s,%s,%s,%s,%s)",(ord_no,pay_id,amt,f_date,exp_del))
                            mydb.commit()

                            print("Order Placed")
                            print("Details: ")
                            print("Order Number = ",ord_no)
                            print("Date = ",f_date)
                            print("Expected Delivery = ",exp_del)
                            print("Total Amount = ",amt)
                            print()

                    elif(ch=='7'):
                        custcont=False
                    else:
                         print("Enter choice from above given choices: ")     


        elif(c=='3'):
            control=False
        else:
            print("Enter choice from above given choices: ")


mccontrol=True
while(mccontrol):
    print("===============================")
    print(" ----Welcome to Big Mango---- ")
    print("*******************************")
    print("=<< 1. Enter as Admin >>=")
    print("=<< 2. Enter as Seller >>=")
    print("=<< 3. Enter as Customer >>=")
    print("=<< 4. Exit/Quit >>=")
    print("*******************************")
    c= input("Enter your choice: ")
    if(c=="1"):
        Admin()
    elif(c=="2"):
        Seller()
    elif(c=="3"):
        Customer()
    elif(c=="4"):
        mccontrol=False
        print("Closing.....")
    
    else:
        print("Enter choice from above given choices")

