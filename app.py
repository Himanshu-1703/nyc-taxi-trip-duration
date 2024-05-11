import joblib
import uvicorn
import pandas as pd
from pathlib import Path
from fastapi import FastAPI
from sklearn.pipeline import Pipeline
from data_models import PredictionDataset

app = FastAPI()

model_file = "rf.joblib"

root_path = Path(__file__).parent
model_path = root_path / "models" / "models" / model_file
preprocessor_path = model_path.parent.parent / "transformers" / "preprocessor.joblib"
output_transformer_path = preprocessor_path.parent / "output_transformer.joblib"

preprocessor = joblib.load(filename=preprocessor_path)
model = joblib.load(filename=model_path)
output_transformer = joblib.load(output_transformer_path)

model_pipe = Pipeline(
    steps= [
        ('preprocessor',preprocessor),
        ('regressor',model)
    ]
)
                      

@app.get('/')
def home():
    return 'Welcome to the taxi trip duration prediction App'


# Model Prediction to predict the trip duration of taxis in New York City
@app.post('/predictions')
def do_predictions(input_data: PredictionDataset):
    X_test = pd.DataFrame(
        data = {
            'vendor_id':input_data.vendor_id,
            'passenger_count':input_data.passenger_count,
            'pickup_longitude':input_data.pickup_longitude,
            'pickup_latitude':input_data.pickup_latitude,
            'dropoff_longitude':input_data.dropoff_longitude,
            'dropoff_latitude':input_data.dropoff_latitude,
            'pickup_hour':input_data.pickup_hour,
            'pickup_date':input_data.pickup_date,
            'pickup_month':input_data.pickup_month,
            'pickup_day':input_data.pickup_day,
            'is_weekend':input_data.is_weekend,
            'haversine_distance':input_data.haversine_distance,
            'euclidean_distance':input_data.euclidean_distance,
            'manhattan_distance':input_data.manhattan_distance
         }, index=[0]
    )
    
    prediction = model_pipe.predict(X_test).reshape(-1,1)
    
    output_inverse_trans = output_transformer.inverse_transform(prediction)[0].item()
    
    return f'The trip duration of your taxi is {output_inverse_trans:.2f} minutes'


if __name__ == "__main__":
    uvicorn.run(app='app:app',host="127.0.0.1")
    
    