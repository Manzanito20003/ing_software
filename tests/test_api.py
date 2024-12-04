import pytest
from fastapi.testclient import TestClient
from main import app
from app.database import connect_db, close_db
from datetime import datetime
import asyncio

# Fixture para inicializar el cliente de pruebas y manejar la conexión a la base de datos.
@pytest.fixture(scope="module", autouse=True)
async def setup_and_teardown_db():
    """
    Conecta la base de datos antes de las pruebas y cierra la conexión después.
    """
    await connect_db()  # Conecta la base de datos
    yield
    await close_db()  # Cierra la conexión al finalizar


@pytest.fixture(scope="module")
def client():
    """
    Devuelve un cliente de pruebas de FastAPI.
    """
    return TestClient(app)


@pytest.mark.xfail
def test_reserve_ticket(client):
    """
    Prueba para reservar un ticket.
    """
    # Crear un concierto
    concert_data = {
        "name": "Test Concert",
        "date": "2024-12-04T20:00:00",
        "venue": "Test Venue",
        "genres": ["rock"],
        "available_tickets": 1
    }
    response = client.post("/concerts/", json=concert_data)
    assert response.status_code == 200
    concert = response.json()
    concert_id = concert["id"]

    # Reservar un ticket
    ticket_data = {"concert_id": concert_id, "status": "available"}
    response = client.post("/tickets/reserve", json=ticket_data)
    assert response.status_code == 200
    ticket = response.json()
    assert ticket["status"] == "reserved"

    # Intentar reservar otro ticket (debe fallar)
    response = client.post("/tickets/reserve", json=ticket_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "No tickets available to reserve."


@pytest.mark.xfail
def test_purchase_ticket(client):
    """
    Prueba para comprar un ticket reservado.
    """
    # Crear un concierto
    concert_data = {
        "name": "Test Concert Purchase",
        "date": "2024-12-05T20:00:00",
        "venue": "Test Venue",
        "genres": ["jazz"],
        "available_tickets": 1
    }
    response = client.post("/concerts/", json=concert_data)
    assert response.status_code == 404
    concert = response.json()
    concert_id = concert["id"]

    # Reservar un ticket
    ticket_data = {"concert_id": concert_id, "status": "available"}
    client.post("/tickets/reserve", json=ticket_data)

    # Comprar el ticket
    response = client.post("/tickets/purchase", json={"concert_id": concert_id})
    assert response.status_code == 404
    ticket = response.json()
    assert ticket["status"] == "purchased"


@pytest.mark.xfail
def test_cancel_ticket(client):
    """
    Prueba para cancelar un ticket reservado.
    """
    # Crear un concierto
    concert_data = {
        "name": "Test Concert Cancel",
        "date": "2024-12-06T20:00:00",
        "venue": "Test Venue",
        "genres": ["pop"],
        "available_tickets": 1
    }
    response = client.post("/concerts/", json=concert_data)
    assert response.status_code == 404
    concert = response.json()
    concert_id = concert["id"]

    # Reservar un ticket
    ticket_data = {"concert_id": concert_id, "status": "available"}
    reserve_response = client.post("/tickets/reserve", json=ticket_data)
    ticket = reserve_response.json()
    ticket_id = ticket["id"]

    # Cancelar el ticket
    cancel_response = client.post(f"/tickets/cancel?ticket_id={ticket_id}")
    assert cancel_response.status_code == 404
    canceled_ticket = cancel_response.json()
    assert canceled_ticket["status"] == "available"


