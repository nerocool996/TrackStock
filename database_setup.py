import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

import psycopg2
import urlparse

Base = declarative_base()
##Config Ends##
class User(Base):
	__tablename__='user'
	name = Column(String(40),nullable=False)
	id = Column(Integer,primary_key = True)
	picture = Column(String(200))
	email = Column(String(100),nullable=False)
	stockItems = relationship("Stock",cascade="all, delete-orphan")

class  Stock(Base):
	__tablename__= 'stock'
	name = Column(String(80),nullable= False)
	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)
	@property
	def serialize(self):
		return {
		'name' : self.name,
		'id' : self.id,
		}

##END OF FILE##
engine = create_engine('sqlite:///stock.db')

Base.metadata.create_all(engine)
