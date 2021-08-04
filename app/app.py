from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SelectField,SubmitField
from wtforms.validators import DataRequired

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine


app = Flask(__name__)
# the connection string is as a result of mysql-connector-python
app.config[
    "SQLALCHEMY_DATABASE_URI"
# ] = "mysql://root:@localhost/election_results"
] = "mysql+mysqlconnector://root:@localhost/election_results"
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"
app.config['SECRET_KEY'] = 'any secret string'
db = SQLAlchemy(app)
Base = automap_base(db.Model)

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base.prepare(engine, reflect=True)


States = Base.classes.states
Party = Base.classes.party
PollingUnit = Base.classes.polling_unit
LGA = Base.classes.lga
Ward = Base.classes.ward
AnnouncedPUResult = Base.classes.announced_pu_results
AnnouncedLgaResult = Base.classes.announced_lga_results


# import pdb; pdb.set_trace()


data= LGA.query.all()
class NamerForm(FlaskForm):
	name = SelectField(u"Select Local Government", choices=[x.lga_name for x in data])
	submit = SubmitField("Submit")




@app.route('/index',methods=['GET', 'POST'])
def index():
    form= NamerForm()
    total_result=0
    estimated_result=0


    if form.validate_on_submit():
        data=form.name.data
        lga = LGA.query.filter(LGA.lga_name == data).first()
        lga_polling_units = PollingUnit.query.filter(PollingUnit.lga_id == lga.lga_id).all()
        polling_ids = [x.uniqueid for x in lga_polling_units]
        results = AnnouncedPUResult.query.filter(
        AnnouncedPUResult.polling_unit_uniqueid.in_(polling_ids)
    ).all()
        total_result = sum([x.party_score for x in results])
        estimated_result = AnnouncedLgaResult.query.filter(AnnouncedLgaResult.lga_name == lga.lga_id
    ).first()
        print(type(total_result))
        # print(total_result)
        print(estimated_result.party_score)
        # form.name.data = 
    return render_template("index.html",form=form,calculated_total=total_result,
    # estimated_total = estimated_result.party_score,
    # data=data
    )


# import pdb; pdb.set_trace(),


def poling_unit():
    polling_units = PollingUnit.query.all()
    columns_header=polling_units[0]

    print(columns_header)


@app.route('/',methods=['GET', 'POST'])
def home():
    lga = LGA.query.all()
    data=""

    if request.method=='POST':
        data = request.form['comp_select']
        return(data)
        


    return render_template('home.html',lgas=lga,data=data)


# import pdb; pdb.set_trace()
@app.route('/pu')
def poling_unit():
    polling_units = PollingUnit.query.all()
    columns_header=polling_units.__dict__.keys()
    

    

    return render_template('pollingUnit.html',polling_units=polling_units)



def send_result(lga):
    lga_polling_units = PollingUnit.query.filter(PollingUnit.lga_id == lga.lga_id).all()
    polling_ids = [x.uniqueid for x in lga_polling_units]
    results = AnnouncedPUResult.query.filter(
        AnnouncedPUResult.polling_unit_uniqueid.in_(polling_ids)
    ).all()
    total_result = sum([x.party_score for x in results])
    estimated_result = AnnouncedLgaResult.query.filter(
        AnnouncedLgaResult.lga_name == lga.lga_id
    ).first()
    return {
        "lga": lga.lga_name,
        "calculated_total": total_result,
        "estimated_total": estimated_result.party_score,
    }


@app.route("/result", methods=["GET","POST"])
def total_result():
    lgabs = LGA.query.all()
    data=""

    if request.method=='POST':
        data = request.form['comp_select']
        return(data)
        

    lga = LGA.query.filter(LGA.lga_name == data).first()
    lga_polling_units = PollingUnit.query.filter(PollingUnit.lga_id == lga.lga_id).all()
    polling_ids = [x.uniqueid for x in lga_polling_units]
    results = AnnouncedPUResult.query.filter(
        AnnouncedPUResult.polling_unit_uniqueid.in_(polling_ids)
    ).all()
    total_result = sum([x.party_score for x in results])
    estimated_result = AnnouncedLgaResult.query.filter(
        AnnouncedLgaResult.lga_name == lga.lga_id
    ).first()
    lgas = LGA.query.all()
    results = [send_result(x) for x in lgas]
    return render_template("home.html",lgabs=lgabs ,lga= lga.lga_name,
        calculated_total= total_result,
        )
 




# poling_unit()

















































if __name__=="__main__":
    app.run(debug=True)