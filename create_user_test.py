import sender_stand_request
import data

# Prueba 1. Creación de un nuevo usuario o usuaria
def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1


# Prueba 1. Creación de un nuevo usuario o usuaria
# El parámetro "firstName" contiene dos caracteres
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")


# Prueba 2. Creación de un nuevo usuario o usuaria
# El parámetro "firstName" contiene 15 caracteres
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")

# Prueba 3. Preparacion - Función de prueba negativa
def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)

    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "El nombre que ingresaste es incorrecto. " \
                                         "Los nombres solo pueden contener caracteres latinos,  "\
                                         "los nombres deben tener al menos 2 caracteres y no más de 15 caracteres"
# Prueba 4. Usando un solo caracter
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

# Prueba 4. P. Negativa. 16 caracteres
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")

# Prueba 5. P. Negativa. Espacios
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("A aaa")

# Prueba 6. Negstiva con simbolos
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")

# Prueba 7. P. Negativa con numeros
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol(123)


# Prueba 8y9: Preaparacion
def negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "No se enviaron todos los parámetros requeridos"

# Prueba 8. No diligenciar campo primer nombre
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_firstname(user_body)

# Prueba 9. Campo vacio
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_firstname(user_body)


# Prueba 10. Numero
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400



