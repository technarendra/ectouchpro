from flask import Flask, render_template, redirect, url_for, request, session, abort,flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from xml.etree import ElementTree as ET

from werkzeug import secure_filename
from flask_user import login_required, UserManager
from flask import send_from_directory
import os
#
app = Flask(__name__)


UPLOAD_FOLDER = 'F:/Flasktut/ectouchproject/data'


ALLOWED_EXTENSIONS = set(['txt', 'xml', 'jpeg'])

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

from app.models import Master, Organization, FixedTotalizer, Tax, PLU, Product, Department, Group, FreeFunction, FixedTotalizer, Clerk, Machine, Customer, Order, OrderLine, User



@app.route('/')
def hello():
    return render_template("home.html")
    # return "<h2>Welcome to ECTOUCH <br><br>\
    # <a href='/upload'><button >Upload File</button></a></h2>"



file = "Order1.XML"
Order_file = 'F:/Flasktut/ectouchproject/data/' + file

print('chhhheck',Order_file)


@app.route('/parse/<filename>')
def parse_xml(filename):
    Order_file = 'F:/Flasktut/ectouchproject/data/' + filename
    dom = ET.parse(Order_file)
    print(dom)
    data = dom.getroot()
    Number = data.find('Date').text
    Name = data.find('ClerkName').text
    Mode = data.find('Mode').text

    print('{} [{}] '.format(
                Number, Name
    ))
    # result = Clerk(
    #     ClerkName=Name
    #     )
    # db.session.add(result)
    # db.session.commit()
    return "ok done"

# parse_xml(Order_file)
 
# stretagy :
# if Order_file name == 1.XML
# save in fixed_totalizers

# if Order_file name == 2.XML 
# save in FreeFunction



# 1=Fixed Totaliser

# 2= Free Function

# 3=Department

# 4=Group

# 5=PLU (product)

# 21=Tax Table

# 25=Mix & Match

# 111=2nd PLU



Master_file = "1.XML"
# Master_file = '/home/narendra/narendra/ectouchproject/data/1.XML'
# print(Master_file)

def parse_xml(Master_file):
    dom = ET.parse(Master_file)
    data = dom.getroot()
    # print(data.tag)  #gives the root of xml
    # print(data.attrib) #gives the attrib of element
    # print(ET.tostring(data, encoding='utf8').decode('utf8'))

    # to fing all element with name
    # for Name in data.iter('Name'):
    #     print(Name.text)

    for Name in data.find("./Records/Record/[Number='3']"):
        print(Name.text)

# parse_xml(Master_file)



@app.route('/upload')
def file():
    return render_template('upload.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
    if request.method == "POST":
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('parse_xml',
                                    filename=filename))

            # return 'file upload successfully'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    filename = send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
    return redirect(url_for('parse_xml',
                                    filename=filename))
