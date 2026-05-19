def test_criar_usuario(client):
    response = client.post("/users", json={"name": "Alice"})
    assert response.status_code == 201
    assert response.get_json()["name"] == "Alice"


def test_criar_usuario_sem_nome(client):
    response = client.post("/users", json={})
    assert response.status_code == 400


def test_buscar_usuario(client):
    post = client.post("/users", json={"name": "Bob"})
    user_id = post.get_json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Bob"


def test_buscar_usuario_inexistente(client):
    response = client.get("/users/999")
    assert response.status_code == 404


def test_deletar_usuario(client):
    post = client.post("/users", json={"name": "Alice"})
    user_id = post.get_json()["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200


def test_atualizar_usuario(client):
    post = client.post("/users", json={"name": "Alice"})
    user_id = post.get_json()["id"]
    response = client.put(f"/users/{user_id}", json={"name": "Alice Atualizada"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "Alice Atualizada"


def test_listar_usuarios(client):
    client.post("/users", json={"name": "Alice"})
    client.post("/users", json={"name": "Bob"})
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_criar_usuario_duplicado_retorna_409(client):
    client.post("/users", json={"name": "Alice"})
    response = client.post("/users", json={"name": "Alice"})
    assert response.status_code == 409


def test_deletar_usuario_inexistente(client):
    response = client.delete("/users/999")
    assert response.status_code == 404


def test_atualizar_usuario_inexistente(client):
    response = client.put("/users/999", json={"name": "Novo"})
    assert response.status_code == 404


def test_status_endpoint(client):
    response = client.get("/status")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_hello_endpoint(client):
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Hello World"


def test_atualizar_sem_nome_retorna_400(client):
    post = client.post("/users", json={"name": "Alice"})
    user_id = post.get_json()["id"]
    response = client.put(f"/users/{user_id}", json={})
    assert response.status_code == 400


def test_listar_usuarios_vazio(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert response.get_json() == []


def test_criar_usuario_retorna_id(client):
    response = client.post("/users", json={"name": "Alice"})
    data = response.get_json()
    assert "id" in data
