from pydantic import BaseModel

# in nested models the data from the one model is passed on the other model

class address(BaseModel):

    city:str
    state: str
    pin:str

class Patient(BaseModel):

    name:str
    gender:str
    age:int
    address:address

address_dict={'city':'gurgaon','state': 'haryana','pin':'122001'}

address1=address(**address_dict)

patient_dict={'name':'Rohit','gender':'male','age':35,'address':address1}

patient1=Patient(**patient_dict)

print(patient1)
print(patient1.address.city)
print(patient1.address.state)

# better organization of teh related data
# Reusability of the Data: use Vitals in multiple models
# Readability: Easier for developers and API consumers to understand
# Validation: Nested models are validated automatically-no extra word needed