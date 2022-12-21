from app.models import Director
from app.schemas import DirectorSchema
from app.setup.db import db

from .dao.director import DirectorDao
from .services.director import DirectorService

director_schema = DirectorSchema()
director_schemas = DirectorSchema(many=True)

director_dao = DirectorDao(Director, db)
director_service = DirectorService(director_dao)
