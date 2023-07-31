import re


def remove_accent(x):
    dicc = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "Á": "A",
        "É": "E",
        "Í": "I",
        "Ó": "O",
        "Ú": "U",
    }
    for key in dicc.keys():
        x = re.sub(key, dicc[key], x)
    x = re.sub('(^\s+)|\s+$', '', x)
    return x


def replace_speciality_names(especialidad):
    especialidad = remove_accent(especialidad)

    if especialidad == "Pediatria y pediatricas articuladas":
        especialidad = "Pediatria"
    elif especialidad == "Ortopedia y traumatologia":
        especialidad = 'Traumatologia'
    elif especialidad == "Ortopedia y traumatologia infantil":
        especialidad = 'Traumatologia infantil'
    elif especialidad == "Diagnostico por imagenes":
        especialidad = 'Dx por imagenes'
    elif especialidad == "Cirugia general":
        especialidad = 'Cirugia'
    elif especialidad == "Otorrinolaringologia":
        especialidad = "ORL"
    elif especialidad == "Medicina general y/o medicina de familia":
        especialidad = "Familiar"
    elif especialidad == "Cirugia infantil (cirugia pediatrica)":
        especialidad = "Cx infantil"
    elif especialidad == "Anatomia patologica":
        especialidad = "Patologia"
    elif especialidad == "Terapia intensiva":
        especialidad = "UTI"
    elif especialidad == "Cirugia cardiovascular":
        especialidad = "Cx cardiovascular"
    elif especialidad == "Cirugia plastica y reparadora":
        especialidad = "Cx plastica"
    elif especialidad == "Fisiatria (medicina fisica y rehabilitacion)":
        especialidad = "Fisiatria"
    elif especialidad == "Radioterapia o terapia radiante":
        especialidad = "Radioterapia"
    elif especialidad == "Cirugia cardiovascular pediatrica":
        especialidad = "Cx cardiovascular infantil"
    elif especialidad == "Genetica medica":
        especialidad = 'Genetica'
    elif especialidad == "Alergia e inmunologia":
        especialidad = 'Alergia'
    elif especialidad == "Medicina Aeronautica y Espacial":
        especialidad = 'Aeronautica y espacial'
    elif especialidad == "Inmunologia . basica":
        especialidad = 'Inmunologia'
    elif especialidad == "Farmacologia clinica":
        especialidad = 'Farmacologia'
    elif especialidad == "Cirugia de torax":
        especialidad = 'Cx de torax'
    elif especialidad == "Neurocirugia Pediatrica":
        especialidad = 'NeuroCx pediatrica'
    elif especialidad == 'Neurocirugia':
        especialidad = 'NeuroCx'
    elif especialidad == "Ginecologia":
        especialidad = 'Tocoginecologia'
    elif especialidad == "Clinica medica":
        especialidad = 'Clinica'

    return especialidad
