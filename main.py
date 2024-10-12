from telebot import TeleBot,types
from conection import * 

bot = TeleBot("7771884657:AAHyx-rWFJDp7tZOVhsa7wxOsBybOvg83PM")

def create_tables():
    conn=connection_database()
    cur=conn.cursor()
    try:
        cur.execute("""
                create table if not exists users(
                    id serial  ,
                    user_id  
                    username varchar(50),
                    first_name varchar(50)
                )
                """)
        cur.execute("""
                    create table if not exists cars(
                    id serial primary key,
                    model varchar(50),
                    price varchar(50)
                )
                    
                    """)    
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        close_con(conn,cur)

def add_user(username,first_name):
    conn=connection_database()
    cur=conn.cursor()
    cur.execute(f"""
                insert into users(username,first_name) values('{username}','{first_name}')
               
                """)
    conn.commit()
    close_con(conn,cur)

car_dict={}
def add_car(message):
    car_dict[message.chat.id]={
        'model':'',
        'price':''
    }
    bot.send_message(message.chat.id,"Enter car model")
    bot.register_next_step_handler(message,get_cars_model)


def get_cars_model(message):
    car_dict[message.chat.id]['model']=message.text
    bot.send_message(message.chat.id,'enter car price ')
    bot.register_next_step_handler(message,get_price)

def get_price(message):
    car_dict[message.chat.id]['price']=message.text
    conn=connection_database()
    cur=conn.cursor()
    cur.execute(f"""
                insert into cars (model,price) values('{car_dict[message.chat.id]['model']}','{car_dict[message.chat.id]['price']}')
                """)
    conn.commit()
    bot.send_message(message.chat.id,'car added sucsessifully')
    close_con(conn,cur)

def get_cars(message):
    conn=connection_database()
    cur=conn.cursor()
    cur.execute("select * from cars")
    cars=cur.fetchall()
    if cars:
        for car in cars:
            bot.send_message(message.chat.id,f"""
model:{car[1]}
price:{car[2]}
                             """)
    close_con(conn,cur)

def up_car(message):
    get_cars(message)
    bot.send_message(message.chat.id,"id baroi update kardanro dokhil kuned")
    bot.register_next_step_handler(message,get_id_up)

def get_id_up(message):
    car_dict[message.chat.id]={
        'id':'',
        'model':'',
        'price':''
    }
    car_dict[message.chat.id]['id']=message.text
    bot.send_message(message.chat.id,"modek baroi update kardanro dokhil kuned")
    bot.register_next_step_handler(message,get_model_up)
    
def get_model_up(message):
    car_dict[message.chat.id]['model']=message.text
    bot.send_message(message.chat.id,"price baroi update kardanro dokhil kuned")
    bot.register_next_step_handler(message,get_price_up)
      
    
def get_price_up(message):
    car_dict[message.chat.id]['price']=message.text
    conn=connection_database()
    cur=conn.cursor()
    cur.execute(f"update cars set model='{car_dict[message.chat.id]['model']}' , price='{car_dict[message.chat.id]['price']}' where id='{car_dict[message.chat.id]['id']}'")
    conn.commit()
    close_con(conn,cur)
    
    bot.send_message(message.chat.id,"update shud")
    


@bot.message_handler(commands=['start'])
def start(message):
    create_tables()
    add_user(message.chat.username,message.chat.first_name)
    bot.send_message(message.chat.id,"hello")
    add_car(message)


@bot.message_handler(commands=['get'])
def get(message):
    get_cars(message) 
    
    
@bot.message_handler(commands=['update'])
def get(message):
    up_car(message)

@bot.message_handler
def all(message):
    if message=='get':
        get_cars(message)

bot.infinity_polling()