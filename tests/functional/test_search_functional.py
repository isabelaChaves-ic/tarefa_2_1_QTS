def test_fluxo_criar_e_buscar_por_nome(client):
    client.post("/users", json={"name": "Alice"})
    client.post("/users", json={"name": "Bob"})
    client.post("/users", json={"name": "Alberto"})

    response = client.get("/users/search?name=al")
    resultado = response.get_json()
    nomes = [u["name"] for u in resultado]
    assert "Alice" in nomes
    assert "Alberto" in nomes
    assert "Bob" not in nomes


def test_fluxo_busca_apos_deletar(client):
    post = client.post("/users", json={"name": "Alice"})
    user_id = post.get_json()["id"]

    client.delete(f"/users/{user_id}")

    response = client.get("/users/search?name=Alice")
    assert response.get_json() == []


def test_fluxo_busca_apos_atualizar(client):
    post = client.post("/users", json={"name": "Alice"})
    user_id = post.get_json()["id"]

    client.put(f"/users/{user_id}", json={"name": "Alice Nova"})

    response_antiga = client.get("/users/search?name=Alice")
    nomes_antiga = [u["name"] for u in response_antiga.get_json()]
    assert "Alice Nova" in nomes_antiga

    response_nova = client.get("/users/search?name=Nova")
    assert len(response_nova.get_json()) == 1
