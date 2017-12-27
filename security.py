from werkzeug.security import safe_str_cmp
from employee import Employee

def authenticate( e_name, e_password):
    employee = Employee.find_by_username( e_name)
    if employee and safe_str_cmp( employee.password, e_password):
        return employee

def identity(payload):
    e_id = payload['identity']
    return Employee.find_by_name['e_id']
