from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

# Modelo para conciertos
# Modelo actualizado para conciertos
class ConcertModel(BaseModel):
    id: str = Field(..., alias="_id", description="ID del concierto en formato string")
    name: str = Field(..., min_length=3, max_length=100, description="Nombre del concierto")
    date: datetime = Field(..., description="Fecha y hora del concierto")
    venue: str = Field(..., min_length=3, max_length=100, description="Lugar del concierto")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

# Modelo para tickets
class TicketModel(BaseModel):
    id: int
    concert_id: int = Field(..., description="ID del concierto asociado")
    user_id: Optional[int] = Field(None, description="ID del usuario que realizó la reserva o compra")
    status: str = Field(
        ...,
        regex="^(available|reserved|purchased)$",
        description="Estado del ticket: 'available', 'reserved', o 'purchased'"
    )
    reserved_until: Optional[datetime] = Field(
        None, description="Fecha y hora límite para una reserva (si aplica)"
    )

    class Config:
        orm_mode = True
