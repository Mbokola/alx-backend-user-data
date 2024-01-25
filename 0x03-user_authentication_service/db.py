#!/usr/bin/env python3
"""DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User
from typing import Dict, Any, Union


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()  # type: ignore
        return self.__session  # type: ignore

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Saves user to database and returns the user object
        """
        user = User(
            email=email,
            hashed_password=hashed_password
        )
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs: Union[int, str]) -> User:
        """ Finds a user from the database based on kwargs """
        try:
            records = self._session.query(User).filter_by(**kwargs).first()
            if not records:
                raise NoResultFound
            return records
        except InvalidRequestError as e:
            raise e

    def update_user(self, user_id: int, **kwargs: Dict[str, Any]) -> None:
        """ Updates user records
        """
        user_recods = self.find_user_by(id=user_id)

        for key, new_value in kwargs.items():
            if hasattr(user_recods, key):
                setattr(user_recods, key, new_value)
                self._session.commit()
            else:
                raise ValueError
