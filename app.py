from flask import Flask, render_template, request, jsonify
import pickle

from flask.helpers import make_response

app = Flask(__name__)

with open("db.model", "rb") as f:
    model = pickle.load(f)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    req = request.get_json(force=True)
    data = req.get("queryResult")
    info = data.get("parameters")

    # geeting data from request body
    age = info.get("age")[0].get("amount")
    gender = info.get("gender")[0].lower()
    married = info.get("marital_status")[0].lower()
    dependents = info.get("dependants")[0]
    # print(type(dependents))
    education = info.get("education")[0].lower()
    employed = info.get("self_employment")[0].lower()
    Credit = info.get("credit_history")[0].lower()
    area = info.get("property_type")[0].lower()
    ApplicantIncome = float(info.get("income")[0])
    CoapplicantIncome = float(info.get("coapp_income")[0])
    LoanAmount = float(info.get("loan_amount")[0])
    Loan_Amount_Term = float(info.get("loan_amount_term")[0].get("amount"))
    # print(type(Loan_Amount_Term))

    if age <= 18 or age >= 60:
        res = {
            "fulfillmentText": "Sorry to keep you waiting, but we cannot process your application further as minimum age criteria for the loan is above 18 years.you're not eligible for the loan. Thanks for taking out the time",
        }
    elif ApplicantIncome <= 2000:
        res = {
            "fulfillmentText": "Sorry to keep you waiting, but we cannot process your application further as your income does not satisfy our minimum income criteria. Thanks for taking out the time"
        }
    elif age >= 18 and age < 60 and ApplicantIncome > 2000:
        if gender == "male":
            male = 1
        else:
            male = 0

        if married == "yes":
            married_yes = 1
        else:
            married_yes = 0

        if Credit == "yes":
            credit = float(1)
        else:
            credit = float(0)

        if education == "no":
            not_graduate = 1
        else:
            not_graduate = 0

        if employed == "yes":
            employed_yes = 1
        else:
            employed_yes = 0

        if area == "semiurban":
            semiurban = 1
            urban = 0
        elif area == "urban":
            semiurban = 0
            urban = 1
        else:
            semiurban = 0
            urban = 0

        if dependents == 1:
            dependents_1 = 1
            dependents_2 = 0
            dependents_3 = 0
        elif dependents == 2:
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 0
        elif dependents == 3:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 1
        else:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 1

        prediction = model.predict(
            [
                [
                    ApplicantIncome,
                    CoapplicantIncome,
                    LoanAmount,
                    Loan_Amount_Term,
                    credit,
                    male,
                    married_yes,
                    not_graduate,
                    employed_yes,
                    semiurban,
                    urban,
                    dependents_1,
                    dependents_2,
                    dependents_3,
                ]
            ]
        )

        if prediction == "N":
            res = {
                "fulfillmentText": "Sorry to keep you waiting, but we cannot process your application further as you're not eligible for the loan. Thanks for taking out the time",
            }
        else:
            res = {
                "fulfillmentText": "Congrats!!!, we have evaluated your application and you're eligible for loan.\nOur associate will contact you within 1-2 working days.\nPlease provide your personal mobile number",
                "outputContext": "projects/loaneligibilitychatbot-fxit/agent/sessions/c280bd6b-709e-b0bd-54b1-f805729db9e8/contexts/contact_details",
            }

    # response = make_response(res)
    # response.headers['Content-Type'] = 'application/json'

    print("-----------------------------------------------------------------")
    print(res)
    return jsonify(res)


if __name__ == "__main__":
    app.run(debug=True)
