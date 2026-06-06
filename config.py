import os

# Store samples inside public/samples and use them directly to avoid duplicate copies
DEFAULT_SAMPLES_DIR = os.path.join('public', 'samples')

DB_FILES = {
    'colleges': os.path.join(DEFAULT_SAMPLES_DIR, 'colleges.csv'),
    'programs': os.path.join(DEFAULT_SAMPLES_DIR, 'programs.csv'),
    'students': os.path.join(DEFAULT_SAMPLES_DIR, 'students.csv')
}

DEFAULT_COLLEGES = [
    {"code": "CCS", "name": "College of Computer Studies"},
    {"code": "COE", "name": "College of Engineering"},
    {"code": "CEBA", "name": "College of Economics, Business and Accountancy"},
    {"code": "CHS", "name": "College of Health Sciences"},
    {"code": "CED", "name": "College of Education"},
    {"code": "CASS", "name": "College of Arts and Social Sciences"}
]

DEFAULT_PROGRAMS = [
    {"code": "BSCS", "name": "BS Computer Science", "collegeCode": "CCS"},
    {"code": "BSIT", "name": "BS Information Technology", "collegeCode": "CCS"},
    {"code": "BSCE", "name": "BS Civil Engineering", "collegeCode": "COE"},
    {"code": "BSBA", "name": "BS Business Administration", "collegeCode": "CEBA"},
    {"code": "BSN", "name": "BS Nursing", "collegeCode": "CHS"},
    {"code": "BSED", "name": "BS Education", "collegeCode": "CED"},
    {"code": "AB-EL", "name": "AB English Language", "collegeCode": "CASS"}
]

DEFAULT_STUDENTS = [
    {"id": "2021-0001", "firstname": "Juan", "lastname": "Dela Cruz", "programCode": "BSCS", "year": "3", "gender": "Male"},
    {"id": "2022-0042", "firstname": "Maria", "lastname": "Santos", "programCode": "BSIT", "year": "2", "gender": "Female"},
    {"id": "2020-0123", "firstname": "Jose", "lastname": "Reyes", "programCode": "BSCE", "year": "4", "gender": "Male"},
    {"id": "2023-0005", "firstname": "Ana", "lastname": "Garcia", "programCode": "BSBA", "year": "1", "gender": "Female"},
    {"id": "2021-0999", "firstname": "Antonio", "lastname": "Luna", "programCode": "BSN", "year": "3", "gender": "Male"}
]
