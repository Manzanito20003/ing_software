from fastapi import APIRouter, HTTPException
from app.schemas import TicketCreate, TicketResponse
from app.database import get_db, connect_db
from bson import ObjectId

router = APIRouter()

# No es necesario llamar a connect_db() aquí, ya que lo manejamos en main.py con los eventos de "startup" y "shutdown".

@router.post("/tickets/reserve", response_model=TicketResponse)
async def reserve_ticket(ticket: TicketCreate):
    """
    Reserva un ticket disponible para un concierto.
    """
    db = get_db()

    # Verificar si hay tickets disponibles
    available_ticket = await db.tickets.find_one({"concert_id": ticket.concert_id, "status": "available"})
    if not available_ticket:
        raise HTTPException(status_code=400, detail="No hay tickets disponibles para reservar.")

    # Actualizar el ticket a estado "reserved"
    result = await db.tickets.update_one(
        {"_id": available_ticket["_id"]},
        {"$set": {"status": "reserved"}}
    )

    if result.modified_count == 1:
        available_ticket["status"] = "reserved"
        return {
            "id": str(available_ticket["_id"]),  # Convertir el ObjectId a string para la respuesta
            "concert_id": available_ticket["concert_id"],
            "status": "reserved"
        }
    else:
        raise HTTPException(status_code=500, detail="No se pudo reservar el ticket.")


@router.post("/tickets/purchase", response_model=TicketResponse)
async def purchase_ticket(ticket: TicketCreate):
    """
    Compra un ticket reservado o disponible para un concierto.
    """
    db = get_db()

    # Buscar un ticket reservado o disponible
    ticket_to_purchase = await db.tickets.find_one(
        {"concert_id": ticket.concert_id, "status": {"$in": ["reserved", "available"]}}
    )
    if not ticket_to_purchase:
        raise HTTPException(status_code=400, detail="No hay tickets disponibles para comprar.")

    # Actualizar el ticket a estado "purchased"
    result = await db.tickets.update_one(
        {"_id": ticket_to_purchase["_id"]},
        {"$set": {"status": "purchased"}}
    )

    if result.modified_count == 1:
        ticket_to_purchase["status"] = "purchased"
        return {
            "id": str(ticket_to_purchase["_id"]),  # Convertir el ObjectId a string para la respuesta
            "concert_id": ticket_to_purchase["concert_id"],
            "status": "purchased"
        }
    else:
        raise HTTPException(status_code=500, detail="No se pudo completar la compra del ticket.")


@router.post("/tickets/cancel", response_model=TicketResponse)
async def cancel_ticket(ticket_id: str):
    """
    Cancela un ticket reservado y lo vuelve a poner disponible.
    """
    db = get_db()

    # Verificar si el ticket está reservado
    ticket = await db.tickets.find_one({"_id": ObjectId(ticket_id), "status": "reserved"})
    if not ticket:
        raise HTTPException(status_code=404, detail="No se encontró un ticket reservado para cancelar.")

    # Actualizar el ticket a estado "available"
    result = await db.tickets.update_one(
        {"_id": ObjectId(ticket_id)},
        {"$set": {"status": "available"}}
    )

    if result.modified_count == 1:
        ticket["status"] = "available"
        return {
            "id": str(ticket["_id"]),  # Convertir el ObjectId a string para la respuesta
            "concert_id": ticket["concert_id"],
            "status": "available"
        }
    else:
        raise HTTPException(status_code=500, detail="No se pudo cancelar el ticket.")
