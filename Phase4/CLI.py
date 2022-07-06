import subprocess as sp
from typing import Type
from time import sleep
import pymysql
import pymysql.cursors
#from employee import employee_home
from tabulate import tabulate
import datetime
##################################################################################


# Make sure sup is not Null
# Error Free
def veiw_emp_details(emp_det):
    
    # Get emp details from EMPLOYEE
    eid = emp_det[0]['EID']
    name = emp_det[0]['FName'] + ' ' + emp_det[0]['LName']
    gender = emp_det[0]['Gender']
    date_b  = emp_det[0]['DOB']
    email_id = emp_det[0]['Email']
    phoneno = emp_det[0]['PhoneNo']
    office = emp_det[0]['Office']


    # Get supervisor name from EMPLOYEE
    cur.execute("SELECT `FName`, `LName` FROM `EMPLOYEE` WHERE `EID` = %d" % emp_det[0]['Supervisor'])
    sup_det = cur.fetchone()
    supervisor = sup_det['FName'] + " " + sup_det['LName']

    
    # Print details
    print(f"Name = {name}")
    print(f"EID = {eid}")
    print(f"Gender = {gender}")
    print(f"Date of Birth = {date_b}")
    print(f"EmailId = {email_id }")
    print(f"Office = {office}")
    print(f"Phone No. = {phoneno}")
    print(f"Supervisor = {supervisor}")

    sleep(1)


# Error Free
def dep_stat() :
    cur.execute("SELECT `DID`, `DName` FROM `DEPARTMENT`")
    dep_det = cur.fetchall()
    print(tabulate(dep_det, headers="keys", tablefmt='psql'))
    input("\nPress Any Key to continue > ")
    return



def view_patients(eid) :
    query = "SELECT PATIENT.FName, PATIENT.LName, VISIT.PID, VISIT.VID, VISIT.Diagnosis, TREATS.Date FROM ((VISIT INNER JOIN PATIENT ON VISIT.PID = PATIENT.PID) INNER JOIN TREATS ON VISIT.VID = TREATS.Visit AND VISIT.PID = TREATS.Patient) WHERE TREATS.Doctor = %d ORDER BY TREATS.Date DESC;" %(eid)
    cur.execute(query)
    patients = cur.fetchall()
    print(tabulate(patients, headers="keys", tablefmt='psql'))
    input("\nPress Any Key to continue > ")


# Error Free
def view_subs(eid) :
    query = "SELECT `EID`, `FName`, `LName` FROM `EMPLOYEE` WHERE `Supervisor` = %d" %(eid)
    cur.execute(query)
    subs = cur.fetchall()
    if len(subs) == 0 :
        print("You Have NO Subordinates")
        return
    print("List Of Subordinates : \n")    
    print(tabulate(subs, headers="keys", tablefmt='psql'))
    input("\nPress Any Key to continue > ")



# Error Free
def add_employee() :
    print("Enter 'back' at any stage to go back\n")
    print("Enter EMPLOYEE Details :\n")


    while(True) :
        name = (input("EMPLOYEE Name : ")).split(' ')
        if len(name) == 1 : name.append("")

        if(name[0] == "back") :
            return
        if(name[0] != "") :
            break

        print("Please input valid values\n")



    while(True) :
        gender  = input("GENDER in (M),(F) or (O) : ")

        if ((gender == 'M') | (gender == 'F') | (gender == 'O')):
            break
        else:
            print("Please input valid values\n")


    while(True) :

        try :
            date = input("Enter Date of Birth [YYYY-MM-DD] : ")
            year, month, day = map(int,date.split('-'))
            datetemp = datetime.datetime(year, month, day)
            break
        except Exception as e :
            print(e)
            print("Please Enter Valid Date")


    while(True) :
        email = (input("EMPLOYEE Email : "))
        if(email == "back") :
            return
        if(email != "") :
            break

        print("Please input valid values\n")




    while(True) :
        p_no = input("EMPLOYEE Phone Number : ")
        if(p_no == "back") :
            return
        try :
            phoneno = int(p_no)
            break
        except :
            print("Please input valid values\n")



    while(True) :
        emp_type = input("EMPLOYEE Type in (D), (A), (M) or (O) : ")
        if ((emp_type == 'D') | (emp_type == 'A') | (emp_type == 'M') | (emp_type == 'O')):
            break
        else:
            print("Please input valid values\n")



    while(True) :
        office = input("EMPLOYEE Office [leave empty if no office]: ")
        if(office == "") :
            break

        office = int(office)
        cur.execute("SELECT * FROM ROOM WHERE RoomNo = %d AND Type = 'Office'" %(office))

        if len(cur.fetchall()) == 0 :
            print("Please input valid values\n")
        else:
            break



    while(True) :
        sup = input("EMPLOYEE Supervisor [Enter EID of Supervisor] : ")

        if(sup == "") :
            print("Please input valid values\n")
            break

        sup = int(sup)
        cur.execute("SELECT * FROM EMPLOYEE WHERE EID = %d" %(sup))

        if len(cur.fetchall()) == 0 :
            print("Please input valid values\n")
        else:
            break

    try:

        #cur.execute("SELECT MAX(`EID`) FORM `EMPLOYEE`;")
        #eid = int(cur.fetchone()['MAX(EID)']) + 1
        if (office != "") :
            query = "INSERT INTO EMPLOYEE (`FName`, `LName`, `Gender`, `DOB`, `Email`, `PhoneNo`, `Emp_Type`, `Office`, `Supervisor`) VALUES ('%s', '%s', '%s', DATE('%s'), '%s', '%d', '%s', %d, %d)" %(name[0], name[1], gender, date, email, phoneno, emp_type, office, sup)
            cur.execute(query)
            con.commit()
        else:
            query = "INSERT INTO EMPLOYEE (`FName`, `LName`, `Gender`, `DOB`, `Email`, `PhoneNo`, `Emp_Type`, `Office`, `Supervisor`) VALUES ('%s', '%s', '%s', DATE('%s'), '%s', '%d', '%s', NULL, %d)" %(name[0], name[1], gender, date, email, phoneno, emp_type, sup)
            cur.execute(query)
            con.commit()
        
        input("\nPress Any Key to continue > ")

    except Exception as e:
        con.rollback()
        print(e)
        print("Failed to Add EMPLOYEE")
        tmp = input("Enter any key to CONTINUE>")




def add_patient() :
    print("Enter 'back' at any stage to ge back\n")
    print("Enter EMPLOYEE Details :")

    while(True) :
        name = (input("PATIENT Name : ")).split(' ')
        if(len(name) == 1) : name.append("")
        if(name[0] == "back") :
            return
        if(name[0] != "") :
            break
        print("Please input valid values\n")

    while(True) :
        gender  = input("GENDER in (M),(F) or (O) : ")
        if ((gender == 'M') | (gender == 'F') | (gender == 'O')):
            break
        else:
            print("Please input valid values\n")

    while(True) :
        try :
            dob = input("Enter Date of Birth [YYYY-MM-DD] : ")
            year, month, day = map(int,dob.split('-'))
            datetemp = datetime.datetime(year, month, day)
            break
        except Exception as e :
            print(e)
            print("Please Enter Valid Date")

    while(True) :
        email = input("PATIENT Email : ")
        if(email == "back") :
            return
        if(email != "") :
            break
        print("Please input valid values")

    while(True) :
        p_no = input("PATIENT Phone Number : ")
        if(p_no == "back") :
            return
        try :
            phoneno = int(p_no)
            break
        except Exception as e :
            print(e)
            print("Please input valid values\n")


    print("Emergencr Contact Details\n")
    while(True) :
        em_name = (input("Emergency Contact Name : "))
        if(em_name == "back") :
            return
        if(em_name != "") :
            break
        print("Please input valid values\n")


    while(True) :
        em_email = (input("Emergency Contact Email : "))
        if(em_email == "back") :
            return
        if(em_email != "") :
            break
        print("Please input valid values\n")

    while(True) :
        em_p_no = input("Emergency Contact Phone Number : ")
        if(em_p_no == "back") :
            return
        try :
            em_phoneno = int(em_p_no)
            break
        except Exception as e :
            print(e)
            print("Please input valid values\n")

    while(True) :
        em_age = input("Emergency Contact Age : ")
        if(em_age == "back") :
            return
        try :
            em_age = int(em_age)
            if(em_age < 18) :
                print("Emergency contact must be over 18.")
                continue
            break
        except :
            print("Please input valid values\n")

    while(True) :
        em_rel = input("Emergency Contact Relation : ")
        if(em_rel == "back") :
            return
        if(em_rel != "") :
            break
        print("Please input valid values\n")

    
    
    is_inpatient = input("Is INPATIENT [y/N] : ")
    if is_inpatient == 'y' :
        is_inpatient = True
            
    else:
        is_inpatient = False

    while(is_inpatient) :
        try :
            room = int(input("Room Number : "))
            bed = int(input("Bed Number : "))
            cur.execute("SELECT * FROM BED WHERE RoomNo = %d AND BedNo = %d;" %(room, bed))
            res = cur.fetchall()

            if (len(res) == 0) :
                raise Exception("No Such Room / Bed Exists")

            elif(res['IsVacant'] == 1) :
                raise Exception("Bed is Occupied")
            
            break

        except Exception as e:
            print(e)
            print("Please input valid Room Number and Bed Number")
    

    dttm = datetime.datetime.now()
    indate = dttm.strftime("%Y-%m-%d")
    intime = dttm.strftime("%H:%M:%S")


    # Check if Patient is New
    try:
        cur.execute("SELECT PID FROM PATIENT WHERE Email = '%s';" %(email))
        res = cur.fetchall()
        if(len(res) == 0) :
            is_new = True
            vid = 1
            query = "INSERT INTO PATIENT (`FName`, `LName`, `Gender`, `DOB`, `Email`, `PhoneNo`, `EMContactName`, `EMContactPhNo`, `EMContactAge`, `EMContactRel`) VALUES ('%s', '%s', '%s', DATE('%s'), '%s', %d, '%s', %d, %d, '%s');" %(name[0], name[1], gender, dob, email, phoneno, em_name, em_phoneno, em_age, em_rel)
            try :
                cur.execute(query)
                con.commit()
                

                cur.execute("SELECT MAX(PID) FROM PATIENT WHERE Email = '%s';" %(email))
                res = cur.fetchone()
                pid = res['MAX(PID)']
                print(pid)

            except Exception as e:
                con.rollback()
                print(e)
                print("Failed to Add Patient")
                 

        else :
            is_new = False
            pid = res['PID']
            cur.execute("SELECT MAX(VID) FORM `VISIT` WHERE PID = %d;") %(pid)
            res = cur.fetchone()
            vid = res['MAX(VID)'] + 1


        print(pid)
        print(vid)
        query = "INSERT INTO VISIT (`PID`, `VID`) VALUES (%d, %d)" %(pid, vid)
        try :
            cur.execute(query)
            con.commit()
        except Exception as e:
            con.rollback()
            print(e)


        try :    
            if is_inpatient :
                query = "INSERT INTO INPATIENT (`PID`, `VID`, `InDate`, `InTime`, `RoomNo`, `Bed`) VALUES (%d, %d, '%s', '%s', %d, %d)" %(pid, vid, indate, intime, room, bed)
                cur.execute(query)
                con.commit()

            else :       
                query = "INSERT INTO OUTPATIENT (`PID`, `VID`, `InDate`, `InTime`) VALUES (%d, %d, '%s', '%s')" %(pid, vid, indate, intime)
                cur.execute(query)
                con.commit()

            print("Patient added Successfully")

            input("\nPress Any Key to continue > ")


        except Exception as e:
            con.rollback()
            print(e)
         

    except:
        print("Operation Failed")

    
    

def edit_employee(eid) :
    while(True):
        print("\n\nSELECT ATTRIBUTE TO EDIT : ")
        print("1 : NAME \n2 : GENDER \n3 : E-MAIL \n4 : PHONE NUMBER\n5:quit")
        choice = int(input("ENTER CHOICE : "))

        if choice == 1 :
            name = (input("New Name : ")).split(' ')
            if len(name) == 1 : name.append("")
            query = "UPDATE `EMPLOYEE` SET `FName` = '%s', `LName` = '%s' WHERE EID = %d" % (name[0], name[1], eid)
            try:
                cur.execute(query)
                con.commit()
            except:
                con.rollback()
                print("Failed to Update Name")

        elif choice == 2:
            while(1):
                gender  = input("GENDER in (M),(F) or (O) : ")
                if (gender == 'M') | (gender == 'F') | (gender == 'O') :
                    break
                else:
                    print("Please input valid values : ")

            query = "UPDATE `EMPLOYEE` SET `Gender` = '%c' WHERE `EID` = %d" % (gender, eid)
            try:
                cur.execute(query)
                con.commit()
            except:
                con.rollback()
                print("some error")
        elif choice == 3 :
            email_id = input("Enter NEW Email : ")
            query = "UPDATE `EMPLOYEE` SET `Email` = '%s' WHERE `EID` = %d" % (email_id, eid)
            try:
                cur.execute(query)
                con.commit()
            except:
                con.rollback()
                print("some error")
        elif choice == 4 :
            phoneno = int(input("Enter NEW Phone Number : "))
            query = "UPDATE `EMPLOYEE` SET `PhoneNo` = %d WHERE `EID` = %d" % (phoneno, eid)
            try:
                cur.execute(query)
                con.commit()
            except:
                con.rollback()
                print("some error")
        elif choice == 5 :
            break

        else :
            print("Read the Prompt DUMBASS")

        input("\nPress Any Key to continue > ")

# Error Free
def print_prompt(emp_det) :
    print("--------------------------")
    print("SELECT OPTION :\n")

    print("1 : EDIT DETAILS")
    print("2 : VIEW SUBORDINATES")

    if emp_det[0]['Emp_Type'] == 'D' :
        print("3 : VIEW PATIENTS")
    elif emp_det[0]['Emp_Type'] == 'A' :
        print("3 : ADD EMPLOYEES")
        print("4 : ADD PATIENT")
        print("5 : VIEW DEPARTMENT STATISTICS")
        print("6 : ADD TREATMENT INSTANCE")
        print("7 : FIRE EMPLOYEE")
    print("q : BACK")
    return 


def add_treats() :
    while(True) :
        try:

            print("Enter details of TREATMENT INSTANCE\n")
            doctor = input("Doctor [EID] : ")
            if doctor == "quit" : break
            doctor = int(doctor)
            patient = input("Patient [PID] : ")
            if patient == "quit" : break
            patient = int(patient)
            visit = input("[VID] : ")
            if visit == "quit" : break
            visit = int(visit)
            med_staff = input("Med Staff administering the Treatment [EID] : ")
            if med_staff == "quit" : break
            med_staff = int(med_staff)
            treatment = input("Treatment [TID] :")
            if treatment == "quit" : break
            treatment = int(treatment)
            date = input("Enter Date [YYYY-MM-DD] : ") 
            if date == "quit" : break
            time = input("Enter Time [hh:mm] : ")
            if time == "quit" : break
            time = time + ":00"

            query = "INSERT INTO TREATS (`Patient`, `Visit`, `Doctor`, `GivenBy`, `Treatment`, `Date`, `Time`) VALUES (%d, %d, %d, %d, %d, DATE('%s'), TIME('%s'))" %(patient, visit, doctor, med_staff, treatment, date, time)
            cur.execute(query)
            con.commit()
            print("Treatment Instance Added")
            input("\nPress Any Key to continue > ")
            break

        except Exception as e:
            print(e)
            con.rollback()
            print("Failed to Add Treatment Instance")
            input("\nPress Any Key to continue > ")
            break


def del_emp() :
    while(True) :
        try :
            eid = input("Enter EID of Employee to Fire : ").strip()
            if eid == quit : break
            eid = int(eid)

            query = "DELETE FROM `EMPLOYEE` WHERE `EID` = %d;" %(eid)
            cur.execute(query)
            con.commit()
            print("EMPLOYEE Removed")
            input("\nPress Any Key to continue > ")
            break

        except Exception as e:
            print(e)
            con.rollback()
            print("Failed remove Employee")
            input("\nPress Any Key to continue > ")
            break


    

# Error Free
def employee_home(eid):

    while(True) :
        #get employee details form EMPLOYEE
        query = f"SELECT * FROM `EMPLOYEE` WHERE `EID` = {eid}" #% (eid)
        cur.execute(query)
        emp_det = cur.fetchall()
        is_doctor = emp_det[0]['Emp_Type'] == "D"
        is_admin = emp_det[0]['Emp_Type'] == "A"

        sp.call('clear', shell=True)
        
        print("\n\n------------EMPLOYEE HOME------------")
        
        
        veiw_emp_details(emp_det)
        

        print("\n\n")
        print_prompt(emp_det)

        choice = input("Enter Choice :").strip()

        

        if choice == "q" :
            break
        elif choice == '1' :
            edit_employee(emp_det[0]['EID'])
        elif choice == '2' :
            view_subs(emp_det[0]['EID'])
            print(choice)
            
        else :
            if is_doctor :
                if choice == '3' :
                    view_patients(emp_det[0]['EID'])
            elif is_admin :
                if choice == '3' :
                    add_employee()
                elif choice == '4' :
                    add_patient()
                elif choice == '5' :
                    dep_stat()
                elif choice == '6' :
                    add_treats()
                elif choice == '7' :
                    del_emp()
            else :
                print("Read the Prompt DUMBASS")
    
    return 0

# Error Free
def login_emp() :
    while(True) :
        print("Enter EXIT in email to go back")

        eid = int(input("Enter EID : "))
        
        email_id = input("Enter Your Email id : ").strip()
        if email_id == "EXIT" :
            break

        
        query = "SELECT * FROM EMPLOYEE WHERE EID = %d AND Email = '%s'" % (eid ,email_id)
        
        cur.execute(query)
        result = cur.fetchall()
        if len(result) == 0:
            print("Incorrect Email or EID\n")
            
        elif len(result) >1:
            print("DATA IS WRONG DUMBASS\n")
        
        else:
            print("You successfully logged in")
            employee_home(eid)



##################################################################################
def Veiw_details(p_id):
    tmp = sp.call('clear', shell=True)

    query = "SELECT * FROM PATIENT WHERE PID = '%d'" % (p_id)

    cur.execute(query)
    result = cur.fetchall()

    pid = result[0]['PID']
    name = result[0]['FName'] + ' ' + result[0]['LName']
    gender = result[0]['Gender']
    date_b  = result[0]['DOB']
    email_id = result[0]['Email']
    phoneno = result[0]['PhoneNo']
    Em_name = result[0]['EMContactName']
    Em_contact = result[0]['EMContactPhNo']
    Em_age = result[0]['EMContactAge']
    Em_rel = result[0]['EMContactRel']

    print("\n -------- \n")
    print(f"Name ={name}")
    print(f"Patient id = {pid}")
    print(f"Gender = {gender}")
    print(f"Date of Birth = {date_b}")
    print(f"EmailId = {email_id }")
    print(f"Phone No. = {phoneno}")
    print(f"Emergency contact Name = {Em_name}")
    print(f"Emergency contact No. = {Em_contact}")
    print(f"Emergency contact age = {Em_age}")
    print(f"Emergency contact Relation = {Em_rel}")
    print("\n ------- \n")


def Edit_details(p_id):

    while(1):
        tmp = sp.call('clear', shell=True)
        print("0 for name \n1 for gender \n2 for dateofb \n3 for email \n4 for phoneno \n5 for EMinfo \n6 for logout \n")
        a = int(input("Number in 0 to 6 : "))

        if a == 0 :
            name = (input("Newname : ")).split(' ')
            query = "UPDATE PATIENT SET FName = '%s', LName = '%s' WHERE PID = '%d'" % (name[0],name[1],p_id)
            try:
                cur.execute(query)
                con.commit()
            except Exception as e:
                con.rollback()
                print("some error" + e)

        elif a==1:
            while(1):
                gender  = input("GENDER in (M),(F) or (O)")[0]
                if ((gender == 'M') | (gender == 'F') | (gender == 'O')) :
                    break
                else:
                    print("Please input valid values : ")

            query = "UPDATE PATIENT SET Gender = '%c' WHERE PID = '%d'" % (gender,p_id)
            try:
                cur.execute(query)
                con.commit()
            except Exception as e:
                con.rollback()
                print("some error" + e)
        elif a==3 :
            email_id = input("New email : ")
            query = "UPDATE PATIENT SET Email = '%s' WHERE PID = '%d'" % (email_id,p_id)
            try:
                cur.execute(query)
                con.commit()
            except Exception as e:
                con.rollback()
                print("some error" + e)
        elif a==4:
            phoneno = int(input("Enter your phone no. : "))
            query = "UPDATE PATIENT SET PhoneNo = '%d' WHERE PID = '%d'" % (phoneno,p_id)
            try:
                cur.execute(query)
                con.commit()
            except Exception as e:
                con.rollback()
                print("some error" + e)
        elif a==5:
            Em_name = input("New Emergency person name : ")
            Em_contact = int(input("New emergency contact no. : "))
            Em_age = int(input("AGE : "))
            EM_rel = input("Relationship : ")

            query = "UPDATE PATIENT SET EMContactName = '%s', EMContactPhNo = '%d', EMContactAge = '%d', EMContactRel = '%s' WHERE PID = '%d'" % (Em_name,Em_contact,Em_age,EM_rel,p_id)
            try:
                cur.execute(query)
                con.commit()
            except Exception as e:
                con.rollback()
                print("some error" + e)

        elif a==6:
            return
        tmp = input("Enter any key to CONTINUE>")



def treatment(p_id):
    while(1):
        tmp = sp.call('clear', shell=True)
        v_id = int(input("Please Input your visit id and -1 to exit: "))
        if v_id < 0:
            return
        try :
            query_treatment = "SELECT TID, Name, Cost, Type, Date, Time  FROM TREATS INNER JOIN TREATMENT ON TREATS.Treatment = TREATMENT.TID WHERE Patient ='%d' AND Visit = '%d'" % (p_id,v_id)
            cur.execute(query_treatment)
            result = cur.fetchall()

            if len(result) == 0 :
                print("pls check vid")

            for row in result :
                name = row['TID']
                cost = row['Cost']
                typ = row['Type']
                date = row['Date']
                time = row['Time']

                print(f"Name = {name} cost = {cost} type = {typ} date = {date} time = {time}")
            tmp = input("Enter any key to CONTINUE>")
        except Exception as e:
            print(e)


def visit_bill(p_id):

    while(1):
        tmp = sp.call('clear', shell=True)
        v_id = int(input("Please Input your visit id and -1 to exit: "))
        if v_id < 0:
            return
        try :
            query_treatment = "SELECT SUM(Cost) AS CHARGE FROM TREATS INNER JOIN TREATMENT ON TREATS.Treatment = TREATMENT.TID WHERE Patient ='%d' AND Visit = '%d' GROUP BY Patient, Visit" % (p_id,v_id)
            cur.execute(query_treatment)
            result = cur.fetchall()

            if len(result) > 0 :
                treatmentcost = result[0]['CHARGE']


                query_visit = "SELECT Bed, RoomNo, DATEDIFF(OutDate,InDate) AS DAYS FROM INPATIENT WHERE PID ='%d' AND VID = '%d' " % (p_id,v_id)
                cur.execute(query_visit)
                result = cur.fetchall()
                if len(result) ==0:
                    days = 0
                    cost =0
                else:

                    bed = result[0]['Bed']
                    room = result[0]['RoomNo']
                    days = result[0]['DAYS']

                    query_BED = "SELECT Cost FROM BED WHERE RoomNo = '%d' AND BedNo = '%d'" % (room,bed)
                    cur.execute(query_BED)
                    result = cur.fetchall()
                    cost = result[0]['Cost']
                print("\n --------- \n")
                print(f"Treatment Cost = {treatmentcost}")
                print(f"Bed Cost = {cost}")
                print(f"Days spent = {days}")
                print("\n --------- \n")
                total = treatmentcost + (cost*days)

                print(f"total Bill = {total}")
                print("\n ------- \n")
            else :
                print("Pls check V_id")

            tmp = input("Enter any key to CONTINUE>")

        except Exception as e:
            print(e)

def login_patient():

    while(1):
        tmp = sp.call('clear', shell=True)
        p_id = int(input("Enter patient id: "))
        email_id = input("Enter Your Email id: ")

        try :
            query = "SELECT * FROM PATIENT WHERE PID = '%d' AND Email = '%s'" % (p_id,email_id)

            cur.execute(query)
            result = cur.fetchall()
            if len(result) == 0:
                print("incorrect Email or Patient ID")
                tmp = input("Enter any key to CONTINUE>")
            elif len(result) >1:
                print("DATA IS WRONG DUMBASS")
                tmp = input("Enter any key to CONTINUE>")
            else:
                print("You successfully logged in")


                while (1) :
                    tmp = sp.call('clear', shell=True)
                    char = input("Press \n(e) to edit details \n(v) to view details \n(t) to view treatment \n(g) to genrate bill \n(q) to logout: ")

                    if char == 'v':
                        Veiw_details(p_id)
                    elif char == 'e':
                        Edit_details(p_id)
                    elif char == 'g':
                        visit_bill(p_id)
                    elif char == 't':
                        treatment(p_id)
                    elif char == 'q':
                        return
                    else:
                        print("please make choices from the given options")
                    tmp = input("Enter any key to CONTINUE>")

        except Exception as e :
            print(e)



############################ PATIENT OVER######################3




while(1):
    tmp = sp.call('clear', shell=True)

    try:

        con = pymysql.connect(host='localhost',
                              port=30306,
                              user="root",
                              password="pwd",
                              db='HOSPITAL_CLI',
                              cursorclass=pymysql.cursors.DictCursor)

        if(con.open):
            print("Connected")

        else:
            print("Failed to connect")

        tmp = input("Enter any key to CONTINUE>")

        with con.cursor() as cur:
            while(1):
                tmp = sp.call('clear', shell=True)
                # Here taking example of Employee Mini-world
                print("SELECT USER TYPE")  # Hire an Employee
                print("1: Patient")  # Fire an Employee
                print("2: Employee")  # Promote Employee
                print("3: EXIT")  # Employee Statistics
                ch = int(input("Enter choice> "))
                tmp = sp.call('clear', shell=True)
                if ch== 1:
                    login_patient()
                if ch == 2 :
                    login_emp()
                if ch == 3:
                    exit()

    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")