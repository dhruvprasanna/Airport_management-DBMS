from flask import Flask, render_template,current_app,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField,TextAreaField,DateField
from wtforms.validators import DataRequired
from sqlalchemy.ext.automap import automap_base
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost:3305/test'
app.config['SECRET_KEY']='root'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_PORT']=3305
app.config['MYSQL_DB']='test'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'




mysql=MySQL(app)
db = SQLAlchemy(app)
app.app_context().push()
res={}
Base = automap_base()
Base.prepare(db.engine,reflect=True)


Airline=Base.classes.airline
air=db.session.query(Airline).all()
Employee=Base.classes.employee1
emp=db.session.query(Employee).all()
Flights=Base.classes.flight
fl=db.session.query(Flights).all()
Passenger=Base.classes.passenger2
ps=db.session.query(Passenger).all()
Ticket=Base.classes.ticket1
tck=db.session.query(Ticket).all()


class QueryForm(FlaskForm):
    query = StringField("Enter Query")
    o=TextAreaField("Output")
    submit= SubmitField("Enter")    

class AForm(FlaskForm):
    aln= StringField("Airline Name")
    aid= StringField("ID",validators=[DataRequired()])
    three= IntegerField("Code")
    submit= SubmitField("Enter")
    delete = SubmitField("Delete")
    update = SubmitField("Update")

class EForm(FlaskForm):
    ssn= IntegerField("SSN",validators=[DataRequired()])
    fname= StringField("First Name")
    m= StringField("M")
    lname= StringField("Last Name")
    address= StringField("Address")
    phone= StringField("Phone Number")
    sex= StringField("Gender")
    job= StringField("Job ")
    age= IntegerField("Age")
    #apname= StringField("AP Name")
    submit= SubmitField("Enter")
    delete = SubmitField("Delete")
    update = SubmitField("Update")

class FForm(FlaskForm):
    fcode= StringField("Flight Code",validators=[DataRequired()])
    source= StringField("Source")
    dest= StringField("Destination")
    arr= StringField("Arrival")
    dep= StringField("Departure")
    status= StringField("Status")
    dur= StringField("Duration")
    ftype= StringField("Flight Type")
    ltime= StringField("Layover Time")
    stops= IntegerField("Stops")
    aid= StringField("Airline ID",validators=[DataRequired()])
    submit= SubmitField("Enter")
    delete = SubmitField("Delete")
    update = SubmitField("Update")

class PForm(FlaskForm):
    pno= StringField("Passport Number",validators=[DataRequired()])
    fname= StringField("First Name")
    lname= StringField("Last Name")
    address= StringField("Address")
    phone= StringField("Phone")
    age= IntegerField("Age")
    sex= StringField("Gender")
    pid= IntegerField("PID",validators=[DataRequired()])
    submit= SubmitField("Enter")
    delete = SubmitField("Delete")
    update = SubmitField("Update")

class TForm(FlaskForm):
    tno= StringField("Ticket Number",validators=[DataRequired()])
    source= StringField("Source")
    dest= StringField("Destination")
    date= DateField("Date",format='%Y-%m-%d')
    seat= StringField("Seat Number")
    cls= StringField("Class")
    pid= IntegerField("PID")
    pno= StringField("Passport Number")
    submit= SubmitField("Enter")
    delete = SubmitField("Delete")
    update = SubmitField("Update")



@app.route('/')
def index():
    return render_template("base.html")





@app.route('/airline',methods=['GET','POST'])
def airlines():
    global air    
    reg_airlines=air
    alrt="primary"
    form=AForm()
    if form.validate_on_submit and form.submit.data:
        airln=Airline(AL_NAME=form.aln.data,THREE_DIGIT_CODE=form.three.data,AIRLINEID=form.aid.data)
        db.session.add(airln)
        db.session.commit()
        alrt="success"
        flash("Added To Database")
        air=db.session.query(Airline).all() 
        return redirect(url_for('airlines'))
    elif form.validate_on_submit and form.delete.data:
        airln=db.session.query(Airline).get(form.aid.data)         
        db.session.delete(airln)
        db.session.commit()
        alrt="alert alert-danger"
        flash("Deleted Row From Database")
        air=db.session.query(Airline).all()
        return redirect(url_for('airlines'))
    elif form.validate_on_submit() and form.update.data:
        airln=db.session.query(Airline).get(form.aid.data)
        airln.AL_NAME=form.aln.data
        airln.THREE_DIGIT_CODE=form.three.data
        db.session.commit()  
        flash("Updated Database")
        air=db.session.query(Airline).all()
        return redirect(url_for('airlines'))
    return render_template("form.html",form=form,reg_airlines=reg_airlines,alrt=alrt)
    
@app.route('/tickets',methods=['GET','POST'])
def tickets():
    global tck    
    reg_tick=tck
    alrt="primary"
    form=TForm()

    if form.validate_on_submit and form.submit.data:
        ticket=Ticket(TICKET_NUMBER=form.tno.data,SOURCE=form.source.data,DESTINATION=form.dest.data,DATE_OF_TRAVEL=str(form.date.data),
        SEATNO=form.seat.data,PID=form.pid.data,PASSPORTNO=form.pno.data,CLASS=form.cls.data)
        db.session.add(ticket)
        db.session.commit()
        alrt="success"
        flash("Added To Database")
        tck=db.session.query(Ticket).all() 
        return redirect(url_for('tickets'))
    elif form.validate_on_submit and form.delete.data:
        ticket=db.session.query(Ticket).get(form.tno.data)         
        db.session.delete(ticket)
        db.session.commit()
        alrt="alert alert-danger"
        flash("Deleted Row From Database")
        tck=db.session.query(Ticket).all()
        return redirect(url_for('tickets'))
    elif form.validate_on_submit() and form.update.data:
        ticket=db.session.query(Ticket).get(form.tno.data)
        ticket.SOURCE=form.source.data
        ticket.DESTINATION=form.dest.data
        ticket.DATE_OF_TRAVEL=str(form.date.data)
        ticket.SEATNO=form.seat.data
        ticket.CLASS=form.cls.data
        db.session.commit()  
        flash("Updated Database")
        tck=db.session.query(Ticket).all()
        return redirect(url_for('tickets'))
    return render_template("form6.html",form=form,reg_tick=reg_tick)

@app.route('/employee',methods=['GET','POST'])
def employees():
    global emp  
    reg_emp=emp
    form=EForm()
    if form.validate_on_submit() and form.submit.data:
        emp=Employee(SSN=form.ssn.data,FNAME=form.fname.data,LNAME=form.lname.data,ADDRESS=form.address.data,
        PHONE=form.phone.data,AGE=form.age.data,SEX=form.sex.data,JOBTYPE=form.job.data)
        db.session.add(emp)
        db.session.commit()
        flash("completed")
        emp=db.session.query(Employee).all()
        return redirect(url_for('employees'))
    elif form.validate_on_submit and form.delete.data:
        emp=db.session.query(Employee).get(form.ssn.data)
        db.session.delete(emp)
        db.session.commit()
        flash("Row Deleted From Database")
        emp=db.session.query(Employee).all()
        return redirect(url_for('employees'))
    elif form.validate_on_submit and form.update.data:
        emp=db.session.query(Employee).get(form.ssn.data)
        emp.NAME=form.fname.data
        emp.LNAME=form.lname.data
        emp.ADDRESS=form.address.data,
        emp.PHONE=form.phone.data
        emp.AGE=form.age.data
        emp.SEX=form.sex.data
        emp.JOBTYPE=form.job.data
        #emp.AP_NAME=form.apname.data
        db.session.commit()
        flash("Updated Database")
        emp=db.session.query(Employee).all()
        return redirect(url_for('employees'))       
    return render_template("form2.html",form=form,reg_emp=reg_emp)

@app.route('/flights',methods=['GET','POST'])
def flights():
    global fl  
    reg_fl=fl
    form=FForm()
    if form.validate_on_submit and form.submit.data:
        flight=Flights(FLIGHT_CODE=form.fcode.data,SOURCE=form.source.data,DESTINATION=form.dest.data,ARRIVAL=form.arr.data,DEPARTURE=form.dep.data,
        STATUS=form.status.data,DURATION=form.dur.data,FLIGHTTYPE=form.ftype.data,LAYOVER_TIME=form.ltime.data,NO_OF_STOPS=form.stops.data,AIRLINEID=form.aid.data)
        db.session.add(flight)
        db.session.commit()
        flash("Added to Database")
        fl=db.session.query(Flights).all()
        return redirect(url_for('flights'))
    elif form.validate_on_submit and form.delete.data:
        fl=db.session.query(Flights).get(form.fcode.data)
        db.session.delete(fl)
        db.session.commit()
        flash("Deleted Row From Database")
        fl=db.session.query(Flights).all()
        return redirect(url_for('flights'))
    elif form.validate_on_submit and form.update.data:
        fl=db.session.query(Flights).get(form.fcode.data)
        fl.SOURCE=form.source.data
        fl.DESTINATION=form.dest.data
        fl.ARRIVAL=form.arr.data
        fl.DEPARTURE=form.dep.data
        fl.STATUS=form.status.data
        fl.DURATION=form.dur.data
        fl.FLIGHTTYPE=form.ftype.data
        fl.LAYOVER_TIME=form.ltime.data
        fl.NO_OF_STOPS=form.stops.data
        fl.AIRLINEID=form.aid.data
        db.session.commit()
        flash("Updated Database")
        fl=db.session.query(Flights).all()
        return redirect(url_for('flights'))
    return render_template("form3.html",form=form,reg_fl=reg_fl)

@app.route('/passenger',methods=['GET','POST'])
def passenger():
    global ps  
    reg_ps=ps
    form=PForm()
    if form.validate_on_submit() and form.submit.data:
        passenger=Passenger(PASSPORTNO=form.pno.data,FNAME=form.fname.data,LNAME=form.lname.data,ADDRESS=form.address.data,
        PHONE=form.phone.data,AGE=form.age.data,SEX=form.sex.data,PID=form.pid.data)
        db.session.add(passenger)
        db.session.commit()
        flash("completed")
        ps=db.session.query(Passenger).all()
        return redirect(url_for('passenger'))
    elif form.validate_on_submit and form.delete.data:
        passenger=db.session.query(Passenger).get((form.pid.data,form.pno.data))
        db.session.delete(passenger)
        db.session.commit()
        flash("Deleted Row From Database")
        ps=db.session.query(Passenger).all()
        return redirect(url_for('passenger'))
    elif form.validate_on_submit and form.update.data:
        passenger=db.session.query(Passenger).get((form.pid.data,form.pno.data))
        passenger.FNAME=form.fname.data
        passenger.LNAME=form.lname.data
        passenger.ADDRESS=form.address.data
        passenger.PHONE=form.phone.data
        passenger.AGE=form.age.data
        passenger.SEX=form.sex.data
        db.session.commit()
        flash("Updated Database")
        ps=db.session.query(Passenger).all()
        return redirect(url_for('passenger'))        
    return render_template("form4.html",form=form,reg_ps=reg_ps)

    
@app.route('/query',methods=['GET','POST'])
def query():
    global res
    cur = mysql.connection.cursor()
    form =QueryForm()
    if form.validate_on_submit():  
        cur.execute(form.query.data)
        res=cur.fetchall()
        mysql.connection.commit()
        form.query.data=''
    return render_template("form5.html",form=form,res=res)
