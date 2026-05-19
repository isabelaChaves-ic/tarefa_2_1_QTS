def test_busca_retorna_usuario_encontrado(client):
    client.post("/users", json={"name": "Alice"})
    response = client.get("/users/search?name=Ali")
    assert response.status_code == 200
    resultado = response.get_json()
    assert len(resultado) == 1
    assert resultado[0]["name"] == "Alice"


def test_busca_retorna_vazio_quando_nao_encontrado(client):
    client.post("/users", json={"name": "Alice"})
    response = client.get("/users/search?name=xyz")
    assert response.status_code == 200
    assert response.get_json() == []


def test_busca_sem_parametro_retorna_todos(client):
    client.post("/users", json={"name": "Alice"})
    client.post("/users", json={"name": "Bob"})
    response = client.get("/users/search")
    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_busca_case_insensitive(client):
    client.post("/users", json={"name": "Alice"})
    response = client.get("/users/search?name=alice")
    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_busca_retorna_multiplos_resultados(client):
    client.post("/users", json={"name": "Alice"})
    client.post("/users", json={"name": "Alberto"})
    client.post("/users", json={"name": "Bob"})
    response = client.get("/users/search?name=al")
    assert response.status_code == 200
    assert len(response.get_json()) == 2
