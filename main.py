import csv

import psycopg2
import psycopg2.extras

#Windows work
db_name = 'Fappdb'
db_user = 'postgres'
db_password = 'everyone'
db_host = 'localhost'
db_port = '5432'

'''
#macbook work (work laptop)
db_name = 'tester'
db_user = 'postgres'
db_password = 'everyone'
db_host = 'localhost'
db_port = '5432'
'''

DBNAME = 'TRANX'

class db:
    '''
    trans: Transaction table in database
        id(SERIAL): a primary key for the table
        name(VARCHAR): the place where the transaction took place
        total(FLOAT): the amount the transtion
        date(DATE): the time of the transaction
        type(VARCHAR): the category of the transtion

    '''

    def __init__(self):

        self.conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        #print(f'crating table TRANX')
        #self.cur.execute("CREATE TABLE TRANX (id SERIAL PRIMARY KEY, name VARCHAR, total FLOAT, date DATE, type VARCHAR);")

        # response = cur.fetchall()
        #self.conn.commit()

    def _create_table(self, table_name):

        self.cur.execute(
            f"CREATE TABLE {table_name} ;")

        # response = cur.fetchall()
        self.conn.commit()

        self.cur.close()

    def insert_transaction(self, csv_file):
        self.conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
        self.cur = self.conn.cursor()

        f = csv.DictReader(open(csv_file))

        for row in f:
            print(row)
            if csv_file == "chase.csv":
                dateA = row['Post Date']
                amt = row['Amount']
                names = row['Description']
                self.cur.execute(
                    #f'INSERT INTO {DBNAME} (name,total,date) VALUES {names,amt,dateA}')
                    "INSERT INTO TRANX (name,total,date) VALUES(%s,%s,%s)", (names, amt, dateA))
                self.conn.commit()
            else:
                dateA = row['Date']
                amt = row['Amount']
                names = row['Name']
                self.cur.execute(
                    #f'INSERT INTO {DBNAME} (name,total,date) VALUES {names, amt, dateA}')
                    "INSERT INTO TRANX (name,total,date) VALUES(%s,%s,%s)", (names, amt, dateA))
                self.conn.commit()

        self.cur.close()

    def view_table(self):
        self.conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        table_name = ''
        table_name = input("What is the name of the table?")
        self.cur.execute(
            f"SELECT * FROM {table_name}")
        print(self.cur.fetchall())
        self.conn.close()

    def categorize_transactions(self):
        '''
            Schema for type of transactions
            1: essentials (rent, electricity)
            2: gas
            3: essential food
            4: fun money
            5: eating out
            6:toby
            7:gifts/kindness
            8: retirment funds
            9: savings
            10: personal investment
            11: random need
            12: random want
            13: Ray
        :return:
        '''
        self.conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        self.cur.execute(f"SELECT * FROM {DBNAME} WHERE {DBNAME}.type is NULL;")
        tranx = self.cur.fetchall()
        self.conn.commit()
        print(len(tranx))
        for t in tranx:
            if t['total'] < 0:
                tranx_type = input(f'|{t["name"]}| charged you {t["total"]}. How would you like to categorize it?')
                print(f"UPDATE {DBNAME} SET type={tranx_type} WHERE id={t['id']}")
                self.cur.execute(
                    f'UPDATE {DBNAME} SET type={tranx_type} WHERE id={t["id"]}')
                    #"UPDATE TRANX SET tran_type=%s WHERE id=%s", (tranx_type, t[s"id"]))
                self.conn.commit()
            if t['total'] > 0:
                self.cur.execute(
                    f'UPDATE {DBNAME} SET type=paid WHERE id={t["id"]}')
                    #"UPDATE TRANX SET tran_type=%s WHERE id=%s", ('paid', t["id"]))
                self.conn.commit()
        self.conn.close()

    def add_manual_transaction(self):
        self.conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        names = input(f'what is the name of the transaction?')
        amt = input(f'What is the total of the transaction?')
        self.cur.execute(
            f'INSERT INTO {DBNAME} (name,total) VALUES ({names},{amt})')
            #"INSERT INTO TRANX (name,total) VALUES(%s,%s,%s)", (names, amt))
        self.conn.commit()
        self.conn.close()

    def sort_transactions(self):
        '''
            Schema for type of transactions
            1: essentials (rent, electricity)
            2: gas
            3: essential food
            4: weed money
            5: eating out
            6: toby
            7: gifts/kindness
            8: retirment funds
            9: savings
            10: personal investment
            11: random need
            12: random want
            13: Ray
        :return:
        '''
        self.conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        self.cur.execute(
            f'SELECT * FROM {DBNAME} WHERE tran_type  in ("1")')
            #"SELECT * FROM TRANX WHERE tran_type in ('1')")
        cur = self.cur.fetchall()
        self.sum = 0
        for row in cur:
            self.sum = row['total'] + self.sum
        print(f'sum of the essentials for Janurary 1 - March 11 = {self.sum}')

        self.cur.execute(
            f'SELECT * FROM {DBNAME} WHERE tran_type  in ("4")')
            #"SELECT * FROM TRANX WHERE tran_type in ('4')")
        cur = self.cur.fetchall()
        self.weed_sum = 0
        for row in cur:
            print(f'Adding {row["total"]} to weed_sum:{self.weed_sum}')
            self.weed_sum = row['total'] + self.weed_sum
        print(f'sum of money spent on weed jan1 - march 11 = {self.weed_sum}')
        # self.conn.commit()
        self.conn.close()


class VISA:
    def __init__(self):
        self.total = None
        self.f = None
        self.t = None
        self.file_name = None

    def open_file(self):
        if self.file_name is None:
            self.file_name = input('input the credit card file name: ')
            self.files = self.file_name + '.csv'

        self.f = csv.DictReader(open(self.files))

    def close_file(self):
        self.f.close()

    def print_file(self):
        for row in self.f:
            print(row)

    def sum_total(self, transactions):
        total = 0
        for item in transactions:
            total = total + int(float(item[0]))
        print("here", total)
        return total

    def sum_debits_and_credits(self):
        self.open_file()
        credits = {}
        debits = {}
        debit_total = 0
        credit_total = 0
        for row in self.f:
            if float(row['Amount']) < 0:
                credits[row['Date']] = row['Amount']
                hold = int(float(row['Amount']))
                # print(hold, type(hold))
                debit_total = debit_total + hold
            else:
                debits[row['Date']] = row['Amount']
                temp = int(float(row['Amount']))
                credit_total = credit_total + temp

        print('total: ' + str(credit_total))
        print('total: ' + str(debit_total))

    def sort_transactions(self):
        self.open_file()
        categories = {
            'fast_food': ['DAIRYQUEEN', 'EZELL\'S', 'TACOBELL', 'PITAPIT', 'STARBUCKS', 'PANDAEXPRESS', 'CHICK-FIL-A',
                          'DOMINO\'S', 'KFC'], 'grocery': ['COSTCO', 'ALBERTSONS', 'SAFEWAY'], 'misc': ['LEE\'S'],
            'recurring': ['Blizzard', 'Spotify'], 'fun': [], 'gas': ['CHEVRON']}
        credits = {'fast_food': [], 'grocery': [], 'misc': [], 'recurring': [], 'fun': [], 'gas': []}
        debits = {'fast_food': [], 'grocery': [], 'misc': [], 'recurring': [], 'fun': [], 'gas': []}

        for row in self.f:
            if float(row['Amount']) < 0:  # debit
                # print(row['Name'])
                for ele in row['Name'].split():
                    for cat in categories.keys():
                        if ele in categories[cat]:
                            debits[cat].append([row['Amount'], row['Date']])
                debits['misc'].append([row['Amount'], row['Date']])
            else:
                for ele in row['Name'].split():
                    # print(ele)
                    for cat in categories.keys():
                        if ele in categories[cat]:
                            print("cat, ele", cat, ele, row['Amount'])
                            credits[cat].append([row['Amount'], row['Date']])
        # print(credits)
        # print(debits)
        total = 0
        total = self.sum_total(debits['misc'])

        print("total spent on fast food", total)
        print(debits['misc'])
        print(credits['grocery'])


class checking:
    def __init__(self):
        self.total = None
        self.f = None
        self.t = None
        self.file_name = None
        self.data_frame = None

    def open_file(self):
        if self.file_name is None:
            self.file_name = input('input the checking file name: ')
            self.files = self.file_name + '.csv'

        self.f = csv.DictReader(open(self.files))

    def close_file(self):
        self.f.close()

    def print_file(self):
        for row in self.f:
            print(row)

    def sum_debits_and_credits(self):
        credits = {}
        debits = {}
        debit_total = 0
        credit_total = 0
        for row in self.f:
            if float(row['Amount']) < 0:  # IF negative value, it was a purchase A.K.A CREDIT
                credits[row['Date']] = row['Amount']
                hold = int(float(row['Amount']))
                # print(hold, type(hold))
                debit_total = debit_total + hold
            else:
                debits[row['Date']] = row['Amount']
                temp = int(float(row['Amount']))
                credit_total = credit_total + temp

        print('total: ' + str(credit_total))
        print('total: ' + str(debit_total))

    def cash_out(self):
        total = 0
        for row in self.f:
            if ('$' in row['Name']):
                list = [x.split() for x in
                        row['Name'].split('$')]  # the second index, first position has the cash request back
                total = total + int(float(list[1][0]))
        print("total cash withdrawn:", total)

done = True
db = db()
finished = False
while done:
    option1 = input("what are you doing? 1:input transaction 2: view transtions: 3:sort transaction \n 4: View table: ")
    if int(option1) == 1:
        in_file = input("what is the file name?")
        db.insert_transaction(in_file + '.csv')
        finished = input("are you done?: ")
    elif int(option1) == 2:
        db.categorize_transactions()
        finished = input("are you done?: ")
    elif int(option1) == 3:
        db.sort_transactions()
    elif int(option1) == 4:
        db.view_table()
    if finished == "yes":
        done = False
