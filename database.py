
# pip install mysql-connector-python ,install mysql-connector-python==8.0.29
import mysql.connector
import datetime
import logging
global times
global date
import ast
from cachetools import cached, TTLCache
cache = TTLCache(maxsize=100, ttl=86400)



dateing = str(datetime.datetime.now().date())
timesss = str(datetime.datetime.now().time().strftime(f'%H:%M:%S'))
timesss = f'{timesss.split(":")[0] + "-" + timesss.split(":")[1] + "-" + timesss.split(":")[2]}'

logging.basicConfig(filename=f"logs [{dateing +' '+ timesss}].log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

@cached(cache)
def start():
    global timesss
    global date
    global db
    global my_curser
    date = datetime.datetime.now().date()

    db = mysql.connector.connect(
        host='34.18.53.199',
        user='root',
        passwd='112233',
        database='storage')
    my_curser = db.cursor()
    logger.debug("Database connected successfully")




def new_table(table_name, instractions):
    '''Create new table'''
    try:
        # UNSIGNED there is no - or +
        # Example: instractions =  mention_ID int PRIMARY KEY AUTO_INCREMENT,name VARCHAR(50),id int(20) UNSIGNED,date VARCHAR(50),message VARCHAR(50)
        my_curser.execute(f'CREATE TABLE {table_name} ({instractions})')
        return "Table has been created successfully"
    except Exception:
        return 'This table is already existed'






def add_new_crad(table,card_id ,card_type,owner_name,college_id ,phone_number,role, rank ,expiration_date):  # Insert new details

    '''Add new data in elements'''
    global timesss

    # table = id_list
    #user_id VARCHAR(300),name VARCHAR(300) ,phone_number VARCHAR(300) ,book_date VARCHAR(300),finish_date

    my_curser.execute(
        f'INSERT INTO {table} (`card_id`, `card_type`, `owner_name`, `college_id`,`role`, `rank`, `issue_date`, `phone_number`, `expiration_date`) VALUES {(card_id ,card_type ,owner_name, college_id ,role , rank ,f"{date} {timesss}",phone_number ,expiration_date)}')
    logger.debug("committing")
    db.commit()
    logger.debug("Data saved successfully in database")
    print("succ")

def log_history(college_id,info):
    my_curser.execute(
        f'INSERT INTO `log_history` (`college_id`, `info`, `date`) VALUES {(college_id, info, f"{date} {timesss}")}')
    logger.debug("committing")
    db.commit()
    logger.debug("Data saved successfully in database")
    print("succ")
def get_table_info(table, parm=None):
    global my_curser
    '''Get infos of the current table'''
    if parm == None:
        try:
            my_curser.execute(f'SELECT item_name,total,used,available FROM {table}')
            logger.debug("test")
            x = []
            for i in my_curser:
                x.append(i)
            logger.debug("Data imported successfully")
            return x

        except Exception:
            logger.debug("Error while gathering information from database")
    else:
        try:
            my_curser.execute(f'SELECT user_id,name,booking_detail,booking_time,finish_date FROM {table}')
            logger.debug("test")
            x = []
            for i in my_curser:
                x.append(i)
            logger.debug("Data imported successfully")
            return x

        except Exception:
            logger.debug("Error while gathering information from database")



def get_availablity(x=False):
    if x == False:
        base = {}
        data = get_table_info("entertain_quantities")
        for i in data:
            base.update({i[0]:[i[1],i[2],i[3]]})

        return base


def update_value(item_name,avail,used):
    my_curser.execute(f'UPDATE `entertain_quantities` SET `used` = {used}, `available` = {avail} WHERE item_ID = {items_id[item_name]}')
    db.commit()
    logger.debug(f"available status for {item_name} has been updated. used {used}, available {avail}")




def get_in_game_users(user_id=None):
    datas = []
    data = {}
    try:
        if user_id==None:
            print("Gathering information of in game users(No user parameter)-database")
            my_curser.execute(
                f'SELECT user_id,name,booking_detail,finish_date FROM entertain_booking WHERE status="in_game"')
            for i in my_curser:
                datas.append(i)
            for s in datas:
                data.update({s[0]: [s[1], ast.literal_eval(s[2]), s[3]]})
            return data
        else:
            my_curser.execute(
                f'SELECT user_id,name,booking_detail,finish_date FROM entertain_booking WHERE (user_id =%s AND status="in_game")' % user_id)
            print(f"Gathering information of in game users(there is user parameter: {user_id})-database")
            for i in my_curser:
                datas.append(i)
            for s in datas:
                data.update({s[0]: [s[1], ast.literal_eval(s[2]), s[3]]})
            return data

    except:
        print("Error while searching and getting in_game users")



def search_user(card_id):

    try:
        my_curser.execute(
            f'''SELECT `card_type`, `owner_name`,`college_id`, `phone_number`, `role`, `rank`, `expiration_date`
        FROM user_cards WHERE card_id ='%s';
        '''%(card_id))
        x = []
        for i in my_curser:

            for g in i:
                x.append(g)
        if x ==[]:
            return False
        else:
            return x
    except:
        return False

start()
if __name__ == "__main__":
    #new_table("log_history",'id_num int PRIMARY KEY AUTO_INCREMENT,college_id VARCHAR(300),info VARCHAR(300), date VARCHAR(600)')
    #log_history("2103100", "dsfhsiudfhjskjd fhsjdfhs dkjfhsdkfjhs djfhksjdf ksjdhf")


    '''card_id = str(input("Card_id: "))
    card_type = str(input("Card_type: "))
    owner_name = str(input("Owner_name: "))
    college_id = str(input("Enter ID: "))
    phone_number = str(input("Phone_number: "))
    role = str(input("Role: "))
    rank = str(input("Rank: "))
    expiration_date=str(input("Expire date: "))
    
    add_new_crad('user_cards',card_id ,card_type,owner_name,college_id,phone_number,role, rank ,expiration_date)
    '''



    #new_table("user_cards",
    #          'id_num int PRIMARY KEY AUTO_INCREMENT,card_id VARCHAR(300),card_type VARCHAR(300),owner_name VARCHAR(300),role VARCHAR(300), rank VARCHAR(300) ,issue_date VARCHAR(300) ,phone_number VARCHAR(300) ,expiration_date VARCHAR(300)')




    #print(search_user(2103100))
    #print(add_new_booking(table='entertain_booking',user_id="11111",booking_type='d',booking_details="gfdgdfg",booking_time="10:22",finish_date="10/10/1001",name="ss",phone_number="33"))
    #print(get_all_data())
    #print(get_in_game_users())

    #print(search_user("2103100"))
    #while True:
        #name = input("Item name: ")
        #total = input("Total available: ")
        #add_new_available_status(table="entertain_quantities", item_name=name, total=total, used=0, available=total)

        #add_new_available_status(table="entertain_quantities",item_name="billiard_cue",total=50,used=0,available=50)



    #new_table("sale_log",
              #'sale_ID int PRIMARY KEY AUTO_INCREMENT,item_name VARCHAR(300),price VARCHAR(50) ,sale_type VARCHAR(50) ,date VARCHAR(150)')
    #new_table("entertain_quantities",'item_ID int PRIMARY KEY AUTO_INCREMENT,item_name VARCHAR(300),total VARCHAR(50) ,used VARCHAR(50) ,available VARCHAR(50)')





    '''    f = open('database_cache.txt', 'w')
    f.write(str(my_curser))
    f.close()

    #logger.debug(get_table_info('sale_log', False))



    # table_columns('vid') '''
