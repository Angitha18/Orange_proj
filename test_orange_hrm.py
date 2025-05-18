from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pageObjects.login import LoginPage
from pageObjects.add_employees import AddEmployees
from pageObjects.personal_details import PersonalDetails
from pageObjects.employee_list import EmployeeListPage


employees = [
    {
        "firstName": "Shyma", "middleName": "S", "lastName": "Satheesh",
        "id": "0810", "nationality": "Indian", "maritalStatus": "Single", "dob": "1997-01-01"
    },
    {
        "firstName": "Shreya", "middleName": "Ram", "lastName": "Kumar",
        "id": "0111", "nationality": "Indian", "maritalStatus": "Single", "dob": "1996-02-02"
    },
    {
        "firstName": "Adhi", "middleName": "Roy", "lastName": "Acharya",
        "id": "0126", "nationality": "Indian", "maritalStatus": "Single", "dob": "1995-03-03"
    }
]


driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")


login_page = LoginPage(driver)
login_page.login("Admin", "admin123")


add_employee_page = AddEmployees(driver)
personal_details_page = PersonalDetails(driver)
employee_list_page = EmployeeListPage(driver)


WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//span[text()='Dashboard']"))
)


WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']"))
).click()

for emp in employees:
    print(f"\nAdding Employee: {emp['firstName']} {emp['middleName']} {emp['lastName']} (ID: {emp['id']})")
    add_employee_page.open_add_employee_form()
    add_employee_page.fill_employee_details(emp)
    personal_details_page.wait_for_page_load()
    personal_details_page.select_nationality(emp["nationality"])
    personal_details_page.select_marital_status(emp["maritalStatus"])
    personal_details_page.set_date_of_birth(emp["dob"])
    personal_details_page.save_personal_details()


employee_list_page.go_to_employee_list()

print("\nVerifying Employees in the Employee List:")
for emp in employees:
    full_name = f"{emp['firstName']} {emp['middleName']} {emp['lastName']}"
    employee_list_page.search_and_verify_employee(full_name)


print("\nTest completed: All employees added and verified.")
driver.quit()
