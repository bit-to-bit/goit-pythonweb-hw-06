from src.database.db import session
from src.database.models import Student
from src.database.seeds import generate_data
from src.database.my_select import execute_all_selects

if __name__ == "__main__":
    print("Hello")
    generate_data()
    execute_all_selects()
