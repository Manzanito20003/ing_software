from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import asyncio

# Configuración de conexión
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "concert_tickets"

async def insert_data():
    """
    Inserta datos básicos en las colecciones 'concerts' y 'tickets' con IDs como strings.
    """
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]

    # Limpia las colecciones antes de insertar (opcional)
    await db.concerts.delete_many({})
    await db.tickets.delete_many({})

    # Datos para la colección 'concerts'
    concert_data = [
        {"_id": str(ObjectId()), "name": "Rock Fest", "date": "2024-12-15T20:00:00", "venue": "National Stadium"},
        {"_id": str(ObjectId()), "name": "Jazz Night", "date": "2024-11-20T19:00:00", "venue": "Jazz Hall"}
    ]

    # Insertar conciertos
    await db.concerts.insert_many(concert_data)
    print(f"Inserted concerts: {[c['_id'] for c in concert_data]}")

    # Datos para la colección 'tickets'
    ticket_data = [
        {"_id": str(ObjectId()), "concert_id": concert_data[0]["_id"], "status": "available"},
        {"_id": str(ObjectId()), "concert_id": concert_data[0]["_id"], "status": "available"},
        {"_id": str(ObjectId()), "concert_id": concert_data[1]["_id"], "status": "available"},
        {"_id": str(ObjectId()), "concert_id": concert_data[1]["_id"], "status": "available"},
    ]

    # Insertar tickets
    await db.tickets.insert_many(ticket_data)
    print(f"Inserted tickets: {[t['_id'] for t in ticket_data]}")

    # Cerrar la conexión
    client.close()

# Ejecutar el script
if __name__ == "__main__":
    asyncio.run(insert_data())
