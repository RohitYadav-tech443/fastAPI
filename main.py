from fastapi import FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,computed_field,Field
from typing import Annotated,Literal,Optional
class Patient(BaseModel):

    id:Annotated[str,Field(...,description='ID of the patient',examples=['p001'])]
    name:Annotated[str,Field(...,description='Name of the patient')]
    city:Annotated[str,Field(...,description='city of the patient')]
    age:Annotated[int,Field(...,gt=0,lt=120,description='age of the patient')]
    gender:Annotated[Literal['male','female','others'],Field(...,description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height in meters')]
    weight: Annotated[float, Field(..., gt=0, description='Weight in kgs')]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi<18.5:
            return 'Underwweight'
        elif self.bmi<25:
            return 'Normal'
        elif self.bmi<30:
            return 'Normal'
        else:
            return 'Obese'
        
class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[str],Field(default=None, gt=0)]
    gender:Annotated[Optional[Literal['male','female','others']],Field(default=None)]
    height:Annotated[Optional[str],Field(default=None, gt=0)]
    weight: Annotated[Optional[str],Field(default=None, gt=0)]

app=FastAPI()
# this is creating of the FastApi object

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    
    return data

def save_data(data):
    with open('patient.json','w') as f:
        json.dump(data,f)

@app.get("/")
def hello():
    return {'message':'Patient Management System API'}

@app.get('/about')
def about():
    return {'message':'A fully functional api to manage the patients records'}

@app.get('/view')
def view():
    data=load_data()

    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str= Path(...,description='THE ID OF THE PATIENT IN THE DB' , examples='p001')):
    # load all the patients
    data=load_data()

    if patient_id in data:
        return data[patient_id]    
    raise HTTPException(status_code=404, detail='Patient not found')

#  ... -> this indicates that the particular query parameter is required and must be provided by the client when making a request to this endpoint. If the client does not provide a value for this parameter, FastAPI will return an error indicating that the required parameter is missing.

@app.get('/sort')
def sort_patients(sort_by:str=Query(...,description='Sort on the basis of the height,weight or bmi'),order: str=Query('asc', description='Sort order (asc or desc)', examples='asc')):
    valid_fields=['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'Invalid field select from {valid_fields}')
    
    if order not in['asc','desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between ascending and descending')
    
    data=load_data()

    sort_order= True if order=='desc' else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0), reverse=True)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    #  load the data
    data=load_data()

    # check if the patient already exist in the database
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exist')
    
    # if not then add teh new patient
    data[patient.id]=patient.model_dump(exclude=['id'])

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str, patient_update:PatientUpdate):
    
    data=load_data()

    # data already exists or not
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info=data[patient_id]

    # now update the model
    updated_patient_info= patient_update.model_dump(exclude_unset= True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key]= value

    # create the pydantic object of the existing_patient_info

    # existing_patient_info -> pydantic onject -> updated 
    existing_patient_info['id']= patient_id
    patient_pydantic_obj=Patient(**existing_patient_info)
    # bmi + verdict -> pydantic object -> dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')
    
    # add this dict to the data
    data[patient_id]= existing_patient_info

    # save the data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})

@app.delete('/patient/{patient_id}')
def delete_patient(patient_id: str):

    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient deleted successfully'})