from flask import Flask,render_template,request
#import csv
from db import validate_patient,validate_doctor_db,view_patient_history_db, validate_insurance_db,validate_hospital_db,get_medical_record_db,update_medical_record_db, get_payment_record_db, update_payment_record_db


app = Flask(__name__)

@app.route('/hello')
def hello():
  return "Hello World!\n"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/patient-login')
def patient():
    return render_template('patient-login.html')

@app.route('/doctor-login')
def doctor():
    return render_template('doctor-login.html')

@app.route('/hospital-login')
def hospital():
    return render_template('hospital-login.html')

@app.route('/insurance-login')
def insurance():
    return render_template('insurance-login.html')

@app.route('/validate', methods =['GET','POST'])
def validate():
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        password = request.form['password']
        print(password)
        password = password[5:7] + "/" + password[8:] + "/" + password[:4]
        print(password)
        
        dbreader = validate_patient(first_name, last_name, password)
        for row in dbreader:
            if row[1] == first_name and row[2] == last_name and row[3] == password:
                bp = row[12]
                heart_rate = row[11]
                return render_template('patient-db.html',first_name = first_name, last_name = last_name, bp=bp, heart_rate=heart_rate)
        error = "Invalid patient name or date of birth. Please try again."
        return render_template('patient-login.html',error=error)
    
@app.route('/validate-doctor', methods =['GET','POST'])
def validate_doctor():
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        doctor_name = 'Dr. ' + first_name + " " + last_name
        password = request.form['password']
        data = validate_doctor_db(doctor_name, password)
        if len(data) > 0:
            return render_template('doctor-view.html',doctor_name=doctor_name, data=data)
        error = "Invalid doctor name. Please try again."
        return render_template('doctor-login.html',error=error)
    
@app.route('/validate-insurance', methods =['GET','POST'])
def validate_insurance():
    if request.method == 'POST':
        insurance_name = request.form['insurance-name']
        password = request.form['password']
        data = validate_insurance_db(insurance_name)
        if password == '12345' and len(data) > 0:
            return render_template('insurance-view.html',insurance_name=insurance_name, data=data)
        error = "Invalid insurance name. Please try again."
        return render_template('insurance-login.html',error=error)

@app.route('/validate-hospital', methods =['GET','POST'])
def validate_hospital():
    if request.method == 'POST':
        hospital_name = request.form['hospital-name']
        password = request.form['password']
        data = validate_hospital_db(hospital_name)
        if password == '123456' and len(data) > 0:
            return render_template('hospital-view.html',hospital_name=hospital_name, data=data)
        error = "Invalid hospital name. Please try again."
        return render_template('hospital-login.html',error=error)
    
@app.route('/patient-history-view', methods =['GET','POST'])
def patient_history_view():
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        doctor_name = request.form['doctor-name']
        data = view_patient_history_db(doctor_name, first_name, last_name)
        query = "SELECT * FROM patients where doctor_name =\'"+doctor_name+"\'"+" and first_name=\'"+first_name+"\'" + " and last_name=\'"+last_name+"\';"
        if data:
            return render_template('patient-history-view.html',data=data)
        return(query)
    
@app.route('/medical-record-update', methods =['GET','POST'])
def medical_record_update():
    if request.method == 'POST':
        patient_id = request.form['patient-id']
        data = get_medical_record_db(patient_id)
        query = "SELECT * FROM patients where patient_id=\'"+patient_id+"\';"
        if data:
            return render_template('medical-record-update.html',data=data, message="")
        return(query)

@app.route('/update-medical-record', methods =['GET','POST'])
def update_medical_record():
    if request.method == 'POST':
        patient_id = request.form['patient-id']
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        dob = request.form['dob']
        sex = request.form['sex']
        blood_type = request.form['blood-type']
        height = request.form['height']
        weight = request.form['weight']
        allergies = request.form['allergies']
        medications = request.form['medications']
        medical_conditions = request.form['medical-conditions']
        heart_rate = request.form['heart-rate']
        blood_pressure = request.form['blood-pressure']
        data = update_medical_record_db(patient_id,first_name,last_name,dob,sex,blood_type,height,weight,allergies,medications,medical_conditions,heart_rate,blood_pressure)
        if data:
            return render_template('medical-record-update.html',data=data, message="medical record successfully updated")
        return data
        
@app.route('/payment-record-update', methods =['GET','POST'])
def payment_record_update():
    if request.method == 'POST':
        patient_id = request.form['patient-id']
        data = get_payment_record_db(patient_id)
        query = "SELECT * FROM patients where patient_id=\'"+patient_id+"\';"
        if data:
            return render_template('payment-record-update.html',data=data, message="")
        return(query)

@app.route('/update-payment-record', methods =['GET','POST'])
def update_payment_record():
    if request.method == 'POST':
        patient_id = request.form['patient-id']
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        doctor_name = request.form['doctor-name']
        doctor_phone = request.form['doctor-phone']
        hospital_name = request.form['hospital-name']
        hospital_phone = request.form['hospital-phone']
        insurance_provider = request.form['insurance-provider']
        insurance_id = request.form['insurance-id']
        data = update_payment_record_db(patient_id,first_name,last_name,doctor_name,doctor_phone,hospital_name,hospital_phone,insurance_provider,insurance_id)
        if data:
            return render_template('payment-record-update.html',data=data, message="payment record successfully updated")
        return data
                        

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port = 8080)
