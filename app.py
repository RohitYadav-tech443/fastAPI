from fastapi import FastAPI
from pydantic import BaseModel,Field, computed_field
from typing import Literal,Annotated
import pickle
import pandas as pd
from fastapi.responses import JSONResponse

# import the model
with open('model.pkl','rb') as f:
    model =pickle.load(f)

app=FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

# build the pydantic model to validate the incoming data
#  ... -> means that the field has no defualt value and it is the required field
# Literals -> this means that we can choose either from the given specified values and not anything else from that 
class UserInput(BaseModel):
    age:Annotated[int, Field(...,gt=0,lt=120,description='Age of the user')]
    weight:Annotated[float, Field(...,gt=0,description='Weight of the user')]
    height:Annotated[float, Field(...,gt=0,lt=2.5,description='Height of the user in meters')]
    income_lpa:Annotated[float, Field(...,gt=0,description='Annual Salary of the user')]
    smoker:Annotated[bool, Field(...,description='Is user a smoker')]
    city:Annotated[str, Field(...,description='The city to which the user belongs')]
    occupation:Annotated[Literal['retired','freelancer','student','government_job','business_owner','unemployed','private_job'],Field(...,description='Occupation of the user')]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi>30:
            return 'high'
        elif self.smoker or self.bmi>27:
            return 'medium'
        else:
            return 'low'
        
    @computed_field
    @property
    # - > str - this defines the return type of the fucntion 
    def age_group(self) -> str:
        if self.age <25:
            return 'young'
        elif self.age<45:
            return'adult'
        elif self.age <60:
            return 'middle_aged'
        return 'senior'
    

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        
# crreating the predict endpoint
@app.get("/")
def home():
    return {"message": "Insurance Premium Prediction API is running"}

@app.post('/predict')
def predict_premium(data: UserInput):

    input_df=pd.DataFrame([{
        'bmi':data.bmi,
        'age_group':data.age_group,
        'lifestyle_risk':data.lifestyle_risk,
        'city_tier':data.city_tier,
        'income_lpa':data.income_lpa,
        'occupation':data.occupation
    }])

    prediction=model.predict(input_df)[0]

    probabilities = model.predict_proba(input_df)[0]
    classes = model.classes_

    class_probabilities = {
        str(cls): round(float(prob), 4)
        for cls, prob in zip(classes, probabilities)
    }

    confidence = round(float(max(probabilities)), 4)

    return JSONResponse(
        status_code=200,
        content={
            "response": {
                "predicted_category": prediction,
                "confidence": confidence,
                "class_probabilities": class_probabilities
            }
        }
    )