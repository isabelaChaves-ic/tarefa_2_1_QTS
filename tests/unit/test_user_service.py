import pytest
from app.services import user_service


@pytest.fixture(autouse=True)
def reset():
    user_service.reset_users()


def test_criar_usuario():
    user = user_service.create_user("Alice")
    assert user["name"] == "Alice"
    assert user["id"] == 1


def test_criar_usuario_duplicado():
    user_service.create_user("Alice")
    resultado = user_service.create_user("Alice")
    assert resultado is None


def test_buscar_usuario_existente():
    user = user_service.create_user("Bob")
    encontrado = user_service.get_user_by_id(user["id"])
    assert encontrado["name"] == "Bob"


def test_buscar_usuario_inexistente():
    resultado = user_service.get_user_by_id(999)
    assert resultado is None


def test_listar_usuarios_vazio():
    resultado = user_service.get_all_users()
    assert resultado == []


def test_listar_usuarios_com_dados():
    user_service.create_user("Alice")
    user_service.create_user("Bob")
    resultado = user_service.get_all_users()
    assert len(resultado) == 2


def test_deletar_usuario_existente():
    user = user_service.create_user("Alice")
    removido = user_service.delete_user(user["id"])
    assert removido["name"] == "Alice"


def test_deletar_usuario_inexistente():
    resultado = user_service.delete_user(999)
    assert resultado is None


def test_atualizar_usuario_existente():
    user = user_service.create_user("Alice")
    atualizado = user_service.update_user(user["id"], "Alice Atualizada")
    assert atualizado["name"] == "Alice Atualizada"


def test_atualizar_usuario_inexistente():
    resultado = user_service.update_user(999, "Novo Nome")
    assert resultado is None


def test_id_incrementa_sequencialmente():
    u1 = user_service.create_user("Alice")
    u2 = user_service.create_user("Bob")
    assert u2["id"] == u1["id"] + 1


def test_criar_multiplos_usuarios_diferentes():
    user_service.create_user("Alice")
    user_service.create_user("Bob")
    user_service.create_user("Carlos")
    resultado = user_service.get_all_users()
    assert len(resultado) == 3


def test_deletar_usuario_remove_da_lista():
    user = user_service.create_user("Alice")
    user_service.delete_user(user["id"])
    resultado = user_service.get_all_users()
    assert len(resultado) == 0


def test_atualizar_para_nome_duplicado_retorna_none():
    user_service.create_user("Alice")
    u2 = user_service.create_user("Bob")
    resultado = user_service.update_user(u2["id"], "Alice")
    assert resultado is None


def test_reset_limpa_usuarios():
    user_service.create_user("Alice")
    user_service.reset_users()
    assert user_service.get_all_users() == []


def test_reset_reinicia_id():
    user_service.create_user("Alice")
    user_service.reset_users()
    novo = user_service.create_user("Bob")
    assert novo["id"] == 1


def test_usuario_tem_campo_id_e_nome():
    user = user_service.create_user("Alice")
    assert "id" in user
    assert "name" in user


def test_criar_usuario_com_nome_vazio_e_valido():
    user = user_service.create_user("")
    assert user is not None


def test_buscar_apos_deletar_retorna_none():
    user = user_service.create_user("Alice")
    user_service.delete_user(user["id"])
    resultado = user_service.get_user_by_id(user["id"])
    assert resultado is None


def test_atualizar_mantem_id():
    user = user_service.create_user("Alice")
    atualizado = user_service.update_user(user["id"], "Alice Nova")
    assert atualizado["id"] == user["id"]
