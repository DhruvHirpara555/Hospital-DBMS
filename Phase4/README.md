## To run

```
$ docker exec -i {container_name} sh -c 'exec mysql -uroot -{password} ' < generate_db.sql
$ python3 login.py 
```
OR

Any other commands to run "generate_db.sql" and "CLI.py"


DATABASE NAME : HOSPITAL_CLI

## Basic Structure and Functional Requirements implemented 

 **Login :**

1. Patient : Directs you to Patient Login
2. Employee : Directs you to  Employee Login
3. Quit: Quits the program

**EMPLOYEE :** 

1. EDIT DETAILS : Edits details of employee 
2. VIEW SUBORDINATES : Shows details of employees supervided by the User
3. ADD EMPLOYEES : Hire New Employees
4. ADD PATIENT : Admit New Patient
5. VIEW DEPARTMENT STATISTICS : Department Info
6. ADD TREATMENT INSTANCE : Every Treatment administered at the hospital is logged through this
7. Fire Employee : Remove Employee.
8. Logout

**PATIENT :**

1. View Patient : Shows all the patient detail for a patient which is logged in
2. Edit Patient : Updates the patient details for a patient which is logged in 
3. View Treatment  : Shows all the treatments taken by patient at a particular visit
4. Generate Bill : Generates a bill for a particular visit made by patient
5. Logout : Logs out from the patient login
