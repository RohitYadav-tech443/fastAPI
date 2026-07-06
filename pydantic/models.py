# def insert_patient_data(name:str,age:int):

#     # print(name)
#     # print(age)
#     # print('Inserted into Database')

#     if type(name) == str and type(age) == int:
#         if age<0:
#             raise ValueError('Age cant be zero')
#         else:
#             print(name)
#             print(age)
#             print('Inserted into Database')
#     else:
#         raise TypeError("Incorrect Data Type")


# insert_patient_data('Rohit',22)

# def update_patient_data(name: str,age:int ):

#     if type(name) == str and type(age) == int:
#         print(name)
#         print(age)
#         print('updated')
#     else:
#         raise TypeError('Incorrect data type')
    
# insert_patient_data('RohitY',22)

# {{using the pydantic}}
from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Optional,Annotated
# building the pydantic model

class Patient(BaseModel):
    # these created fields are by default Required
    # Annotated is used to add the metadata to the fields of the pydantic model
    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the pateint in less than 50 chars', examples=['Rohit','Mohit'])]
    email:EmailStr
    linkedIN:AnyUrl
    # Field is used to add the metadata to the fields of the pydantic model
    age: int = Field(gt=0, lt=120)
    weight: float = Field(gt=0)
    married: Optional[bool] = None
    allergies: Annotated[Optional[List[str]],Field(default=None,max_length=5)]
    contact_details: Optional[Dict[str, str]] = None

# creating the object of the class
def insert_patient_data(patient:Patient):

    print(patient.name)
    print(patient.email)
    print(patient.linkedIN)
    print(patient.age)
    print(patient.weight)
    print(patient.allergies)
    print(patient.married)
    print('inserted')

patient_info={'name':'nitish','email':'abc@gmail.com','linkedIN':'https://www.linkedin.com/in/rohit','age':'30','weight':75.2,'married':True,'allergies':['pollen','dust'],'contact_details':{'phone':'9087654321'}}

def update_patient_data(patient:Patient):

    print(patient.name)
    print(patient.age)
    print('inserted')

patient_info={'name':'nitish','age':'30','email':'abc@gmail.com','linkedIN':'https://www.linkedin.com/in/rohit','weight':75.22}

patient1=Patient(**patient_info)

insert_patient_data(patient1)
# update_patient_data(patient1)

# {{Field Validator -> It's used for the custom validation in the pydantic like the person should belong to the particular group only then only he is valid}}





