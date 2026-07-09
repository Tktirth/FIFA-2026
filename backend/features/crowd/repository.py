from infrastructure.firestore.repository import BaseRepository
from .models import ZoneDensity

class CrowdRepository(BaseRepository[ZoneDensity]):
    collection_name = "crowd_data"
    model_class = ZoneDensity
