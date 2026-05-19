import pytest
from app.services import user_service


@pytest.fixture(autouse=True)
def reset():
    user_service.reset_users()


def test_buscar_por_nome_retorna_usuario_correto():
    user_service.create_user("Alice")
    user_service.create_user("Bob")
    resultado = user_service.search_users_by_name("Ali")
    assert len(resultado) == 1
    assert resultado[0]["name"] == "Alice"


def test_buscar_por_nome_case_insensitive():
    user_service.create_user("Alice")
    resultado = user_service.search_users_by_name("alice")
    assert len(resultado) == 1


def test_buscar_por_nome_sem_resultado():
    user_service.create_user("Alice")
    resultado = user_service.search_users_by_name("xyz")
    assert resultado == []


def test_buscar_por_nome_vazio_retorna_todos():
    user_service.create_user("Alice")
    user_service.create_user("Bob")
    resultado = user_service.search_users_by_name("")
    assert len(resultado) == 2


def test_buscar_multiplos_resultados():
    user_service.create_user("Alice")
    user_service.create_user("Alberto")
    user_service.create_user("Bob")
    resultado = user_service.search_users_by_name("al")
    assert len(resultado) == 2
