
def replace_speciality_names(especialidad):
    if especialidad == "Pediatría y pediátricas articuladas":
        especialidad = "Pediatría"
    elif especialidad == "Ortopedia y traumatología":
        especialidad = 'Traumatología'
    elif especialidad == "Ortopedia y traumatología infantil":
        especialidad = 'Traumatología infantil'
    elif especialidad == "Diagnóstico por imágenes":
        especialidad = 'Dx por imágenes'
    elif especialidad == "Cirugía general":
        especialidad = 'Cirugía'
    elif especialidad == "Otorrinolaringología":
        especialidad = "ORL"
    elif especialidad == "Medicina general y/o medicina de familia":
        especialidad = "Familiar"
    elif especialidad == "Cirugía infantil (cirugía pediátrica)":
        especialidad = "Cx infantil"
    elif especialidad == "Anatomía patológica":
        especialidad = "Patología"
    elif especialidad == "Terapia intensiva":
        especialidad = "UTI"
    elif especialidad == "Cirugía cardiovascular":
        especialidad = "Cx cardiovascular"
    elif especialidad == "Cirugía plástica y reparadora":
        especialidad = "Cx plástica"
    elif especialidad == "Fisiatría (medicina física y rehabilitación)":
        especialidad = "Fisiatría"
    elif especialidad == "Radioterapia o terapia radiante":
        especialidad = "Radioterapia"
    elif especialidad == "Cirugía cardiovascular pediátrica":
        especialidad = "Cx cardiovascular infantil"
    elif especialidad == "Genética médica":
        especialidad = 'Genética'
    elif especialidad == "Alergia e inmunología":
        especialidad = 'Alergia'
    elif especialidad == "Medicina Aeronáutica y Espacial":
        especialidad = 'Aeronáutica y espacial'
    elif especialidad == "Inmunología . básica":
        especialidad = 'Inmunología'
    elif especialidad == "Farmacología clínica":
        especialidad = 'Farmacología'
    elif especialidad == "Cirugía de tórax":
        especialidad = 'Cx de tórax'
    elif especialidad == "Neurocirugía Pediátrica":
        especialidad = 'NeuroCx pediátrica'

    return especialidad
