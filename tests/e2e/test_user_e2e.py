import time
import threading
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import create_app
from app.services import user_service


@pytest.fixture(scope="module")
def live_server():
    app = create_app()
    app.config["TESTING"] = True
    user_service.reset_users()
    server = threading.Thread(
        target=lambda: app.run(port=5099, use_reloader=False, debug=False)
    )
    server.daemon = True
    server.start()
    time.sleep(1)
    yield "http://localhost:5099"
    user_service.reset_users()


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    d = webdriver.Chrome(options=options)
    yield d
    d.quit()


@pytest.fixture(autouse=True)
def limpar_usuarios():
    user_service.reset_users()


def test_cadastrar_usuario_aparece_na_lista(live_server, driver):
    driver.get(live_server)
    wait = WebDriverWait(driver, 5)
    campo = wait.until(EC.presence_of_element_located((By.ID, "name")))
    campo.send_keys("Alice")
    driver.find_element(By.ID, "submit").click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "users"), "Alice"))
    lista = driver.find_element(By.ID, "users")
    assert "Alice" in lista.text


def test_cadastrar_dois_usuarios_aparecem_na_lista(live_server, driver):
    driver.get(live_server)
    wait = WebDriverWait(driver, 5)
    campo = wait.until(EC.presence_of_element_located((By.ID, "name")))
    campo.send_keys("Alice")
    driver.find_element(By.ID, "submit").click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "users"), "Alice"))
    campo = driver.find_element(By.ID, "name")
    campo.clear()
    campo.send_keys("Bob")
    driver.find_element(By.ID, "submit").click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "users"), "Bob"))
    lista = driver.find_element(By.ID, "users")
    assert "Alice" in lista.text
    assert "Bob" in lista.text


def test_titulo_da_pagina(live_server, driver):
    driver.get(live_server)
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    assert "Cadastro de Usuários" in driver.find_element(By.TAG_NAME, "h1").text


def test_campo_nome_presente(live_server, driver):
    driver.get(live_server)
    wait = WebDriverWait(driver, 5)
    campo = wait.until(EC.presence_of_element_located((By.ID, "name")))
    assert campo.is_displayed()
