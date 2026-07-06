from pydantic import BaseModel

# Serialization in Pydantic means converting a Pydantic model into a format that can be easily stored, transmitted, or returned, such as a Python dictionary or a JSON string.

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str = 'Male'
    age: int
    address: Address

address_dict = {'city': 'gurgaon', 'state': 'haryana', 'pin': '122001'}

address1 = Address(**address_dict)

patient_dict = {'name': 'nitish', 'age': 35, 'address': address1}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump(exclude_unset=True)
# exclude unset keeps only those values of basemodel which were mentioned while defining the model only 

print(temp)
print(type(temp)) 