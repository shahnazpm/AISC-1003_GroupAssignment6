@app.route('/')
def home():
    return 'Welcome to the Flask Model Integration Example!'

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract data from the request
        data = request.get_json()
        
        if 'features' not in data:
            return jsonify({'error': 'Missing features'}), 400
        
        features = data['features']
        
        # Convert features to DataFrame for processing
        df = pd.DataFrame([features])
        
        # Example preprocessing steps
        # 1. Handle missing values
        df.fillna(0, inplace=True)
        
        # 2. Scale numerical features
        numeric_features = df.select_dtypes(include=[np.number])
        df[numeric_features.columns] = scaler.transform(numeric_features)
        
        # 3. Encode categorical features
        categorical_features = df.select_dtypes(include=[object])
        df = pd.get_dummies(df, columns=categorical_features.columns)
        
        # Ensure that the DataFrame has the same number of columns as during training
        df = df.reindex(columns=encoder.get_feature_names_out(), fill_value=0)
        
        # Make a prediction
        prediction = model.predict(df)
        
        # Return the result as JSON
        return jsonify({'prediction': prediction.tolist()})

    except Exception as e:
        return jsonify({'error': str(e)}), 500