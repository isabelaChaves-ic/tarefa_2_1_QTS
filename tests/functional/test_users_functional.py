def test_fluxo_completo_usuario(client):
    post = client.post("/users", json={"name": "Alice"})
    assert post.status_code == 201
    user_id = post.get_json()["id"]

    get = client.get(f"/users/{user_id}")
    assert get.status_code == 200
    assert get.get_json()["name"] == "Alice"

    put = client.put(f"/users/{user_id}", json={"name": "Alice Atualizada"})
    assert put.status_code == 200
    assert put.get_json()["name"] == "Alice Atualizada"

    delete = client.delete(f"/users/{user_id}")
    assert delete.status_code == 200

    get_depois = client.get(f"/users/{user_id}")
    assert get_depois.status_code == 404


def test_criar_multiplos_e_listar(client):
    client.post("/users", json={"name": "Alice"})
    client.post("/users", json={"name": "Bob"})
    client.post("/users", json={"name": "Carlos"})

    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.get_json()) == 3


def test_fluxo_duplicado_bloqueado(client):
    r1 = client.post("/users", json={"name": "Alice"})
    assert r1.status_code == 201

    r2 = client.post("/users", json={"name": "Alice"})
    assert r2.status_code == 409

    lista = client.get("/users")
    assert len(lista.get_json()) == 1


def test_criar_buscar_deletar_verificar(client):
    post = client.post("/users", json={"name": "Bob"})
    user_id = post.get_json()["id"]

    client.delete(f"/users/{user_id}")

    lista = client.get("/users")
    nomes = [u["name"] for u in lista.get_json()]
    assert "Bob" not in nomes


def test_atualizar_e_verificar_na_lista(client):
    post = client.post("/users", json={"name": "Alice"})
    user_id = post.get_json()["id"]

    client.put(f"/users/{user_id}", json={"name": "Alice Nova"})

    lista = client.get("/users")
    nomes = [u["name"] for u in lista.get_json()]
    assert "Alice Nova" in nomes
    assert "Alice" not in nomes


def test_fluxo_com_tres_usuarios_deletar_um(client):
    client.post("/users", json={"name": "Alice"})
    r2 = client.post("/users", json={"name": "Bob"})
    client.post("/users", json={"name": "Carlos"})

    user_id = r2.get_json()["id"]
    client.delete(f"/users/{user_id}")

    lista = client.get("/users")
    nomes = [u["name"] for u in lista.get_json()]
    assert len(nomes) == 2
    assert "Bob" not in nomes
    assert "Alice" in nomes
    assert "Carlos" in nomes
