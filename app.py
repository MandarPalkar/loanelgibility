from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


with open("db.model", "rb") as f:
    model = pickle.load(f)


@app.route("/predict", methods=["GET", "POST"])
def predict():

    req = request.get_json(force=True)

    info = req.queryResult.parameters

    # geeting data from request body
    age = info.age[0].amount
    gender = info.gender[0].lower()
    married = info.marital_status[0].lower()
    dependents = info.dependants[0]
    education = info.education[0].lower()
    employed = info.self_employment[0].lower()
    credit = info.credit_history[0].lower()
    area = info.property_type[0].lower()
    ApplicantIncome = float(info.income[0])
    CoapplicantIncome = float(info.coapp_income[0])
    LoanAmount = float(info.loan_amount[0])
    Loan_Amount_Term = float(info.loan_amount_term[0].amount)

    if age <= 18 or age >= 60:
        res = {
            "fulfillmentText": "Sorry to keep you waiting, but we cannot process your application further as minimum age criteria for the loan is above 18 years.you're not eligible for the loan. Thanks for taking out the time",
        }

    elif ApplicantIncome <= 8000:
        res = {
            "fulfillmentText": "Sorry to keep you waiting, but we cannot process your application further as your income does not satisfy our minimum income criteria. Thanks for taking out the time"
        }

    elif age >= 18 and age <= 60 and ApplicantIncome > 8000:
        if gender == "male":
            male = 1
        else:
            male = 0

        if married == "yes":
            married_yes = 1
        else:
            married_yes = 0

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

        # education
        if education == "no":
            not_graduate = 1
        else:
            not_graduate = 0

        # employed
        if employed == "yes":
            employed_yes = 1
        else:
            employed_yes = 0

        # property area
        if area == "semiurban":
            semiurban = 1
            urban = 0

        elif area == "urban":
            semiurban = 0
            urban = 1

        else:
            semiurban = 0
            urban = 0

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
                "fulfillmentText": "COngrats, we have evaluated your application and you're eligible for loan. Our associate will contact you within 1-2 working days"
            }
    return res


if __name__ == "__main__":
    app.run(debug=True)
