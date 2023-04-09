
from DAO.model_DAO import UserDAO

from service.service_user import UserService
from setup_db import db


user_dao = UserDAO(session=db.session)


user_service = UserService(dao=user_dao)
