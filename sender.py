from flask import Flask,render_template, jsonify
import psycopg2
import pika
import os # talend ko job run garna ko lagi



app = Flask(__name__)


    # connection to db
connection= psycopg2.connect(
        host='localhost',
        database='soluvv_1',
        user='postgres',
        password='9865197446',
        port='5432'
    )

print(connection)
cur=connection.cursor()

# ingre='papaya'

# cur.execute("""select Search_Query, count(*) from stagetable where Search_Query=%s group by Search_Query""",[ingre])
# read =cur.fetchall()
# if read==[]:
#     Ingredient_name=ingre
#     count= 0
#     print(Ingredient_name)
#     print(count)
# else:
#     for lis in read :
#         a=lis
#         Ingredient_name=a[0]
#         count=a[1]
#         print(Ingredient_name)
#         print(count)
        



@app.route("/")
def hello_world():
    return render_template("index.html")# yeti garda ni templates directory bitra gaera index.html ma access garxa because of render_tempalte hai

@app.route('/count/<name>')
def hello_name(name):
    # return name
    connection= psycopg2.connect(
    host='localhost',
    database='soluvv_1',
    user='postgres',
    password='9865197446',
    port='5432'
    )

    cur=connection.cursor()
    cur.execute("""select Search_Query, count(*) from stagetable where Search_Query=%s group by Search_Query""",[name])
    read =cur.fetchall()
    if read==[]:
        count= 0
        result={
            "Ingredients_name": name,
            "count": count
        }
    else:
        for lis in read :
            a=lis
            count=a[1]
            result={
            "Ingredients_name": name,
            "count": count
        }
    return result

@app.route('/send/<name>')
def Send_task(name):
    # os.startfile("Task_1_0.1\Task_1\Task_1_run.sh")# yesley talend ko job chai run hunu paryo..
    str_1=name
    connect = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connect.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body=str_1)
    connect.close()
    return name + " is send for the check in our list"

if __name__=="__main__":#hamro program call garnu nabparna ko lagi yo run gareko ho
    app.run(debug=True)# hami lai port number change garnu parye ko khanda ma cahi (debug=True,port=8000)garney

cur.close()