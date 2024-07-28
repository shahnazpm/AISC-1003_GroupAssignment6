from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Loading model
model = pickle.load(open('svm.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction', methods=['POST'])
def predict_churn():
    try:
        # Get input values from the form
        amount_rub_sup_prc = float(request.form.get('amount-rub-sup-prc', 0))
        rest_avg_cur = float(request.form.get('rest-avg-cur', 0))
        trans_count_atm_prc = float(request.form.get('trans-count-atm-prc', 0))
        amount_rub_atm_prc = float(request.form.get('amount-rub-atm-prc', 0))
        cnt_tran_clo_tendency3m = float(request.form.get('cnt-tran-clo-tendency3m', 0))
        rest_dynamic_cur_1m = float(request.form.get('rest-dynamic-cur-1m', 0))
        sum_tran_sup_tendency1m = float(request.form.get('sum-tran-sup-tendency1m', 0))
        cnt_tran_sup_tendency1m = float(request.form.get('cnt-tran-sup-tendency1m', 0))
        clnt_setup_tenor = float(request.form.get('clnt-setup-tenor', 0))
        trans_amount_tendency3m = float(request.form.get('trans-amount-tendency3m', 0))

        # Creating feature array for prediction
        features = np.array([[amount_rub_sup_prc, rest_avg_cur, trans_count_atm_prc,
                              amount_rub_atm_prc, cnt_tran_clo_tendency3m,
                              rest_dynamic_cur_1m, sum_tran_sup_tendency1m,
                              cnt_tran_sup_tendency1m, clnt_setup_tenor,
                              trans_amount_tendency3m] +
                             [0] * (171 - 10)])  # Filling remaining features with zeros

        # Making prediction
        prediction = model.predict(features)
        # Interpret the prediction
        if prediction[0] == 1:
            result = 'Client has churned.'
        else:
            result = 'Client has not churned.'

        result = f'Prediction: {prediction[0]}'


        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'result': 'Error: ' + str(e)})

if __name__ == '__main__':
    app.run(debug=True)
