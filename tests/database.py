import pytest
from app.database import connect_db, close_db, get_db
from pymongo.errors import ConnectionFailure
from app.database import database
from bson import ObjectId
from datetime import datetime

@pytest.mark.asyncio
async def test_connect_db():
    """ Prueba para conectar a la base de datos """
    await connect_db()
    db = get_db()
    assert db is not None
    assert db.name == "concert_tickets"  # Verifica que estamos conectados a la base de datos correcta

@pytest.mark.asyncio
async def test_connect_db_fail():
    """ Simula un fallo de conexión """
    try:
        await connect_db(uri="mongodb://invaliduri")
    except ConnectionFailure as e:
        assert str(e) == "No se pudo conectar a la base de datos."

@pytest.mark.asyncio
async def test_close_db():
    """ Verifica el cierre de la base de datos """
    await connect_db()
    await close_db()
    try:
        get_db()
    except ConnectionError as e:
        assert str(e) == "No hay conexión con la base de datos. Llama a `connect_db()` primero."

@pytest.mark.asyncio
async def test_insert_concert():
    """ Prueba para insertar un concierto en la base de datos """
    concert_data = {
        "_id": ObjectId(),
        "name": "Test Concert",
        "date": datetime.utcnow().isoformat(),
        "venue": "Test Venue"
    }
    db = get_db()
    result = await db.concerts.insert_one(concert_data)
    assert result.inserted_id is not None
    concert = await db.concerts.find_one({"_id": result.inserted_id})
    assert concert["name"] == "Test Concert"
    assert concert["venue"] == "Test Venue"

@pytest.mark.asyncio
async def test_insert_ticket():
    """ Prueba para insertar un ticket en la base de datos """
    concert_data = {
        "_id": ObjectId(),
        "name": "Test Concert",
        "date": datetime.utcnow().isoformat(),
        "venue": "Test Venue"
    }
    db = get_db()
    concert = await db.concerts.insert_one(concert_data)

    ticket_data = {
        "concert_id": concert.inserted_id,
        "status": "available"
    }
    ticket = await db.tickets.insert_one(ticket_data)
    assert ticket.inserted_id is not None
    ticket_from_db = await db.tickets.find_one({"_id": ticket.inserted_id})
    assert ticket_from_db["status"] == "available"
    assert ticket_from_db["concert_id"] == concert.inserted_id

@pytest.mark.asyncio
async def test_insert_ticket_invalid_data():
    """ Prueba para insertar un ticket con datos inválidos """
    try:
        db = get_db()
        invalid_ticket_data = {
            "concert_id": "invalid_id",  # ID no válido
            "status": "invalid_status"  # Estatus inválido
        }
        await db.tickets.insert_one(invalid_ticket_data)
    except Exception as e:
        assert "Invalid data" in str(e)

@pytest.mark.asyncio
async def test_find_concert_by_id():
    """ Prueba para buscar un concierto por su ID """
    concert_data = {
        "_id": ObjectId(),
        "name": "Test Concert",
        "date": datetime.utcnow().isoformat(),
        "venue": "Test Venue"
    }
    db = get_db()
    concert = await db.concerts.insert_one(concert_data)
    found_concert = await db.concerts.find_one({"_id": concert.inserted_id})
    assert found_concert["name"] == "Test Concert"
    assert found_concert["venue"] == "Test Venue"

@pytest.mark.asyncio
async def test_find_ticket_by_concert_id():
    """ Prueba para buscar un ticket por el ID del concierto """
    concert_data = {
        "_id": ObjectId(),
        "name": "Test Concert",
        "date": datetime.utcnow().isoformat(),
        "venue": "Test Venue"
    }
    db = get_db()
    concert = await db.concerts.insert_one(concert_data)

    ticket_data = {
        "concert_id": concert.inserted_id,
        "status": "available"
    }
    ticket = await db.tickets.insert_one(ticket_data)
    found_ticket = await db.tickets.find_one({"concert_id": concert.inserted_id})
    assert found_ticket["status"] == "available"
    assert found_ticket["concert_id"] == concert.inserted_id

@pytest.mark.asyncio
async def test_delete_concert():
    """ Prueba para eliminar un concierto """
    concert_data = {
        "_id": ObjectId(),
        "name": "Test Concert",
        "date": datetime.utcnow().isoformat(),
        "venue": "Test Venue"
    }
    db = get_db()
    concert = await db.concerts.insert_one(concert_data)
    result = await db.concerts.delete_one({"_id": concert.inserted_id})
    assert result.deleted_count == 1
    concert = await db.concerts.find_one({"_id": concert.inserted_id})
    assert concert is None
