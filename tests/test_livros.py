import pytest
from unittest.mock import patch
from app import app


@pytest.fixture
def client():
    return app.test_client()

def test_cadastro_livro(client):
    mock_livro = type("Livro", (), {
        "id": "1",
        "titulo": "Livro Mockado",
        "autor": "Autor X",
        "genero": "Aventura",
        "ano_publicacao": "2020"
    })()

    with patch("controllers.livros_controller.bd.cadastrarLivro", return_value=mock_livro):
        response = client.post("/livros/", json={
            "titulo": "Livro Mockado",
            "autor": "Autor X",
            "genero": "Aventura",
            "ano_publicacao": "2020"
        })

        assert response.status_code == 201
        data = response.get_json()
        assert data["titulo"] == "Livro Mockado"
        assert data["autor"] == "Autor X"
        assert data["genero"] == "Aventura"

def test_listar_todos_livros(client):
    mock_livros = [
        type("Livro", (), {"titulo": "A", "autor": "B"})(),
        type("Livro", (), {"titulo": "C", "autor": "D"})()
    ]

    with patch("controllers.livros_controller.bd.livros", {1: mock_livros[0], 2: mock_livros[1]}):
        response = client.get("/livros/")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["titulo"] == "A"
        assert data[1]["autor"] == "D"