import sqlite3
from datetime import datetime
connection = sqlite3.connect('instance/namelist.db')

cursor = connection.cursor()

# create_table = """
# CREATE TABLE employers (
#         id INTEGER NOT NULL, 
#         name VARCHAR(255) NOT NULL, 
#         sex VARCHAR(6) NOT NULL, 
#        nric VARCHAR(255) NOT NULL, 
#         dob DATETIME, 
#         age INTEGER, 
#        phone_number INTEGER,
#         email VARCHAR(255),
#        home_address VARCHAR(255),
#         exp INTEGER,
#         grade INTEGER,
#         avail BOOLEAN,
#         PRIMARY KEY(id),
#         UNIQUE(id),
#         UNIQUE(nric)
# );
# """
# cursor.execute(create_table)

#cursor.execute("""INSERT INTO employers VALUES (1,'John Tan','Male','S9001011A',01/01/1990,33,91234567,'john.tan@email.com','Block 123 Ang Mo Kio Avenue 4 #12-34',10,4,TRUE)""")

all_employers = [ 
    (1,'John Tan','Male','S9001011A',datetime.strptime('01/01/1990', '%m/%d/%Y').date(),33,91234567,'john.tan@email.com','Block 123 Ang Mo Kio Avenue 4 #12-34',10,4,True),
    (2,'Michael Lim','Male','S9002012B',datetime.strptime('02/02/1990', '%m/%d/%Y').date(),33,82345678,'michael.lim@email.com','Blk 456 Bukit Timah Road #02-12',8,5,False),
    (3,'David Ng','Male','S9003013C',datetime.strptime('03/03/1990', '%m/%d/%Y').date(),33,73456789,'david.ng@email.com','789 Clementi Street 2 #05-67',12,5,True), 
    (4,'Robert Ong','Male','S9004014D',datetime.strptime('04/04/1990', '%m/%d/%Y').date(),33,64567890,'robert.ong@email.com','10A Jurong West Street 8 #23-45',7,4,False), 
    (5,'William Wong ','Male','S9005015E',datetime.strptime('05/05/1990', '%m/%d/%Y').date(),33,55678901,'william.wong@email.com','#07-89 123 Sengkang East Avenue',9,4,True), 
    (6,'Benjamin Goh','Male','S9006016F', datetime.strptime('06/06/1990', '%m/%d/%Y').date(),33,46789012,'benjamin.goh@email.com','55 Marine Parade Central #06-78',11,5,False), 
    (7,'James Lim','Male','S9007017G',datetime.strptime('07/07/1990', '%m/%d/%Y').date(),33,37890123,'james.lim@email.com','9A Serangoon Garden Way #03-21',6,5,True), 
    (8,'Charles Tan','Male','S9008018H',datetime.strptime('08/08/1990', '%m/%d/%Y').date(),33,28901234,'charles.tan@email.com','77 Tampines Avenue 5 #09-87',14,4,False), 
    (9,'Daniel Lee','Male','S9009019I',datetime.strptime('09/09/1990', '%m/%d/%Y').date(),33,19876543,'daniel.lee@email.com','#02-34 66 Holland Drive',5,4,True),  
    (10,'Matthew Chong','Male','S9010010J',datetime.strptime('10/10/1990', '%m/%d/%Y').date(),33,10987654,'matthew.chong@email.com','888 Toa Payoh Lorong 2 #11-11',13,5,False), 
    (11,'Kevin Lim','Male','S9011011K',datetime.strptime('11/11/1990', '%m/%d/%Y').date(),33,21098765,'kevin.lim@email.com','Block 123 Yishun Street 11, #08-88',8,5,True), 
    (12,'Andrew Ng','Male','S9012012L',datetime.strptime('12/12/1990', '%m/%d/%Y').date(),33,32109876,'andrew.ng@email.com','Blk 456 Woodlands Street 33 #01-12',10,4,False), 
    (13,'Jonathan Koh','Male','S9013013M', datetime.strptime('01/01/1991', '%m/%d/%Y').date(),32,43210987,'jonathan.koh@email.com','789 Bishan Street 22 #03-45',11,5,True), 
    (14,'Samantha Lee','Female','S9014014N',datetime.strptime('02/02/1991', '%m/%d/%Y').date(),32,54321098,'samantha.lee@email.com','10A Bedok North Road #02-76',9,4,False), 
    (15,'Joseph Goh','Male','S9015015O',datetime.strptime('03/03/1991', '%m/%d/%Y').date(),32,65432109,'joseph.goh@email.com','#07-34 123 Pasir Ris Central',7,4,True), 
    (16,'Richard Tan','Male','S9016016P',datetime.strptime('04/04/1991', '%m/%d/%Y').date(),32,81273645,'richard.tan@email.com','55 Jurong East Avenue 1 #06-23',12,5,False), 
    (17,'Thomas Lee','Male','S9017017Q', datetime.strptime('05/05/1991', '%m/%d/%Y').date(),32,76543210,'thomas.lee@email.com','9A Kallang Bahru, #09-09',6,4,True), 
    (18,'Nicholas Teo','Male', 'S9018018R', datetime.strptime('06/06/1991', '%m/%d/%Y').date(),32,87654321,'nicholas.teo@email.com','77 Geylang East Avenue 2 #05-67',14,5,False), 
    (19,'Christopher Tan','Male','S9019019S',datetime.strptime('07/07/1991', '%m/%d/%Y').date(),32,98765432,'christopher.tan@email.com','#02-34 66 Telok Blangah Drive',5,5,True), 
    (20,'Aaron Lim','Male','S9020010T',datetime.strptime('08/08/1991', '%m/%d/%Y').date(),32,76544321,'aaron.lim@email.com','888 Bukit Merah Central #03-11',13,4,False), 
    (21,'Jonathan Neo','Male','S9021011U',datetime.strptime('09/09/1991', '%m/%d/%Y').date(),32,65433210,'jonathan.neo@email.com','Block 123, Ang Mo Kio Street 22 #06-54',8,5,True), 
    (22,'Kenneth Tan','Male','S9022012V',datetime.strptime('10/10/1991', '%m/%d/%Y').date(),32,54322109,'kenneth.tan@email.com','Blk 456, Bukit Batok Central #02-34',10,4,False), 
    (23,'Matthew Lee','Male','S9023013W',datetime.strptime('11/11/1991', '%m/%d/%Y').date(),32,43211098,'matthew.lee@email.com', '789 Choa Chu Kang Avenue 3 #09-87',11,4,True), 
    (24,'Nicholas Ng','Male','S9024014X',datetime.strptime('12/12/1991', '%m/%d/%Y').date(),32,32100987,'nicholas.ng@email.com','10A Hougang Avenue 8 #04-32',9,5,False), 
    (25,'Jonathan Tay','Male','S9025015Y',datetime.strptime('01/01/1992', '%m/%d/%Y').date(),31,21099876,'jonathan.tay@email.com','#07-78 123 Punggol Place',7,4,True), 
    (26,'Bryan Lim','Male','S9026016Z',datetime.strptime('02/02/1992', '%m/%d/%Y').date(),31,10988765,'bryan.lim@email.com','55 Sembawang Drive #02-11',12,5,False), 
    (27,'Jeremy Chan','Male','S9027017A', datetime.strptime('03/03/1992', '%m/%d/%Y').date(),31,19877654,'jeremy.chan@email.com','9A Sengkang West Way #08-77',6,5,True), 
    (28,'Brandon Tan','Male','S9028018B', datetime.strptime('04/04/1992', '%m/%d/%Y').date(),31,28906543,'brandon.tan@email.com','77 Clementi West Street 6 #03-45',14,4,False), 
    (29,'Timothy Goh','Male','S9029019C',datetime.strptime('05/05/1992', '%m/%d/%Y').date(),31,37895432,'timothy.goh@email.com', '#02-34 66 Bukit Timah Road',5,5,True), 
    (30,'Kelvin Lee','Male','S9030010D',datetime.strptime('06/06/1992', '%m/%d/%Y').date(),31,46784321,'kelvin.lee@email.com','888 Orchard Road #09-12',13,4,False) 
]

cursor.executemany("INSERT INTO employees VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", all_employers)

connection.commit()

connection.close()
