from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Dict

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    # @model_validator(mode='after')
    # def validate_weight(self):
    #     if self.weight>100:
    #         raise ValueError('This much fat people should loose their weight first')
    #     return self

    @model_validator(mode='after')
    def validate_emergency_contact(self):
        if self.age>60  and 'emergency' not in self.contact_details:
            raise ValueError('Patients older than 60 years must have an ')
        return self


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

patient_info = {'name':'nitish', 'email':'abc@icici.com', 'age': '65', 'weight':75.5, 'married': True, 'allergies': ['pollen', 'dust'], 'contact_details':{'phone':'2353462', 'emergency':'235236'}}

patient1 = Patient(**patient_info) 

update_patient_data(patient1)