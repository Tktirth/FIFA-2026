from infrastructure.firestore.repository import BaseRepository
from .models import Incident

class IncidentRepository(BaseRepository[Incident]):
    collection_name = "incidents"
    model_class = Incident
