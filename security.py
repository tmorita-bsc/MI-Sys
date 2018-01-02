from werkzeug.security import safe_str_cmp
from employee import Employee

def authenticate( username, password):
    employee = Employee.find_by_username( username)
    if employee and safe_str_cmp( employee.password, password):
        return employee

def identity(payload):
    emp_id = payload['identity']
    return Employee.find_by_id(emp_id)
