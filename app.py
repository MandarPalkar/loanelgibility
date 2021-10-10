from flask import Flask,render_template,request
import pickle

app=Flask(__name__)
@app.route("/",methods=["GET","POST"])
def home():
	return render_template("home.html")

with open("db.model","rb") as f:
	model=pickle.load(f)

@app.route("/predict",methods=['GET', 'POST'])
def predict():
	if request.method ==  'POST':
		gender = request.form['gender']
		married = request.form['married']
		dependents = request.form['dependents']
		education = request.form['education']
		employed = request.form['employed']
		credit = float(request.form['credit'])
		area = request.form['area']
		ApplicantIncome = float(request.form['ApplicantIncome'])
		CoapplicantIncome = float(request.form['CoapplicantIncome'])
		LoanAmount = float(request.form['LoanAmount'])
		Loan_Amount_Term = float(request.form['Loan_Amount_Term'])
		
		if (gender == "Male"):
            		male=1
		else:
            		male=0
        
        	# married
		if(married=="Yes"):
            		married_yes = 1
		else:
            		married_yes=0

        # dependents
		if(dependents=='1'):
            		dependents_1 = 1
            		dependents_2 = 0
            		dependents_3 = 0
		elif(dependents == '2'):
            		dependents_1 = 0
            		dependents_2 = 1
            		dependents_3 = 0
		elif(dependents == '3+'):
            		dependents_1 = 0
            		dependents_2 = 0
            		dependents_3 = 1
		else:
            		dependents_1 = 0
            		dependents_2 = 0
            		dependents_3 = 0  

        # education
		if (education=="Not Graduate"):
            		not_graduate=1
		else:
            		not_graduate=0

        # employed
		if (employed == "Yes"):
            		employed_yes=1
		else:
            		employed_yes=0

        # property area

		if(area=="Semiurban"):
            		semiurban=1
            		urban=0
		elif(area=="Urban"):
            		semiurban=0
            		urban=1
		else:
            		semiurban=0
            		urban=0

		prediction = model.predict([[ApplicantIncome,CoapplicantIncome,LoanAmount,Loan_Amount_Term,credit,male,married_yes,not_graduate,employed_yes,semiurban,urban,dependents_1,dependents_2,dependents_3]])

        # print(prediction)

		if(prediction=="N"):
            		prediction="No"
		else:
            		prediction="Yes"

		return render_template("prediction.html", msg=prediction)



	else:
        	return render_template("prediction.html")











if __name__=="__main__":
	app.run(debug=True)