import pytest
from app.models import ConcertModel, TicketModel
from datetime import datetime
from pydantic import ValidationError


# Prueba para ConcertModel usando AAA
def test_concert_model_valid():
    # Arrange: Datos válidos de entrada
    concert_data = {
        "_id": "674fc0099428a01e206e074a",  # ID válido
        "name": "Rock Fest",
        "date": datetime(2024, 12, 15, 20, 0),
        "venue": "National Stadium"
    }

    # Act: Crear una instancia de ConcertModel
    concert = ConcertModel(**concert_data)

    # Assert: Verificar que los datos se asignen correctamente
    assert concert.id == "674fc0099428a01e206e074a"
    assert concert.name == "Rock Fest"
    assert concert.date == datetime(2024, 12, 15, 20, 0)
    assert concert.venue == "National Stadium"


# Prueba para ConcertModel con datos inválidos
def test_concert_model_invalid_name():
    # Arrange: Datos inválidos (nombre vacío)
    concert_data = {
        "_id": "674fc0099428a01e206e074a",
        "name": "",
        "date": datetime(2024, 12, 15, 20, 0),
        "venue": "National Stadium"
    }

    # Act & Assert: Comprobar que se levanta una excepción de validación
    with pytest.raises(ValidationError):
        ConcertModel(**concert_data)


# Prueba para TicketModel usando AAA
def test_ticket_model_valid():
    # Arrange: Datos válidos de entrada
    ticket_data = {
        "id": 1,
        "concert_id": "674fc0099428a01e206e074a",  # Aquí concert_id debe ser un string
        "user_id": 123456,
        "status": "available",
        "reserved_until": datetime(2024, 12, 15, 22, 0)
    }

    # Act: Crear una instancia de TicketModel
    ticket = TicketModel(**ticket_data)

    # Assert: Verificar que los datos se asignen correctamente
    assert ticket.id == 1
    assert ticket.concert_id == "674fc0099428a01e206e074a"  # Asegurarse que sea un string
    assert ticket.user_id == 123456
    assert ticket.status == "available"
    assert ticket.reserved_until == datetime(2024, 12, 15, 22, 0)


# Prueba para TicketModel con un estado inválido
def test_ticket_model_invalid_status():
    # Arrange: Datos inválidos (estado inválido)
    ticket_data = {
        "id": 1,
        "concert_id": "674fc0099428a01e206e074a",  # Usar un string aquí también
        "user_id": 123456,
        "status": "sold",  # Este estado no es válido, debería ser "available", "reserved" o "purchased"
        "reserved_until": datetime(2024, 12, 15, 22, 0)
    }

    # Act & Assert: Comprobar que se levanta una excepción de validación
    with pytest.raises(ValidationError):
        TicketModel(**ticket_data)
