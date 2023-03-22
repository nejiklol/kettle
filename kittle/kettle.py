import sqlite3 as sl
from flask import Flask, render_template, request

app = Flask(__name__)

# Global boolean value
VKL = False                                     #VKL variables - on/off
temperaturaMAX = 100                            #temperaturaMAX - maximum temperature
temperatura = 0                                 #temperatura - current temperature
power = 1                                       #power - kettle power

@app.route('/', methods=['POST','GET'])
def index():                                    #Function on/off
    global VKL                                  # in case the kettle is on variables are taken
    global temperaturaMAX                       #from the fields temperaturaMAX and power
    global temperatura                          # if they are absent they are set to 10 and 1 correspondingly
    global power                                # in case of switching off the parameters are reset
    if  request.method == 'POST':
        if VKL:
            VKL = not VKL
            temperaturaMAX = 10
            temperatura = 0
            power = 1
        else:
            VKL = not VKL

        print(VKL)
    return render_template('index.html', VKL=VKL,temperaturaMAX = temperaturaMAX,power = power)


@app.route('/get_data', methods=['GET'])
def get_data():                                     
    global temperaturaMAX                             #this function simulates water heating
    global temperatura                                # every second by adding the values of power and temperatura
    global power                                      # if the temperature after adding
    global VKL                                        # is greater than or equal to temperaturaMAX
    if VKL:                                           #then the maximum temperature is set

        if temperatura+power < temperaturaMAX:        
            temperatura+=power                       
        elif temperatura+power >= temperaturaMAX:
            temperatura=temperaturaMAX               
            VKL = not VKL                             
        
        else:
            temperatura = 0
    insert_into([temperatura, temperaturaMAX, power])
    return str(temperatura)

@app.route('/copy_text', methods=['POST'])
def copy_text():                            #this function takes the values temperaturaMAX and power
    global temperaturaMAX                   #from the corresponding fields
    global power                            # if the data is not correct
    MaxTemp = request.form['MaxTemp']       #then 10 and 1 will be entered respectively
    Power = request.form['Power']
    if temperaturaMAX==10 or power==1:
        try:
            power = int(Power)
            temperaturaMAX = int(MaxTemp)
        except:
            temperaturaMAX = 10
            power = 1
    print('Power-----',power,'/n','MaxTemp-----',temperaturaMAX)
    
    return 'OK'


# Logging to a DB
def createDB():                             

    con = sl.connect('kettle.db')              #

    with con:
        con.execute("""
            CREATE TABLE LOG (
                temperatura INTEGER,
                temperaturaMAX INTEGER,
                power INTEGER
            );
        """)
def Drop_Table():
    con = sl.connect('kettle.db')
    with con:
        con.execute("""
            DROP TABLE LOG;
        """)
def Select_from_db():
    a = []
    con = sl.connect('kettle.db')

    with con:
        data = con.execute("SELECT * FROM LOG ")
        data = data.fetchall()
        for row in data:
            a.append(row)
        print(a)
    return a
def insert_into(data):
    con = sl.connect('kettle.db')
    with con:

        sql = "INSERT INTO LOG (temperatura, temperaturaMAX, power) values(?, ?, ?)"

        con.execute(sql,data)
if __name__ == '__main__':

    Drop_Table()
    createDB()

    app.run(debug=False)
    Select_from_db() #prints data that was logged while programm is running