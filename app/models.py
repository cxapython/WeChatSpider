import uuid
from flask import Flask, request, json, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import mysql.connector
from app import db
from config import Config
#flask的SQLAlchemy连接mysql的增删改查
#---------------------------------------------------------------------------------------------
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session=sessionmaker(bind=engine)
Base=declarative_base()
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True)
    username = Column(String(32))
    password = Column(String(80)) #可以设定长度

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def __repr(self):
        return "<User('%s','%s','%s')>"%(self.username,self.password)
Base.metadata.create_all(engine)#创建数据库表
# #插入新数据
# ed_User=User(name='ed',fullname="Ed Jones",password='edspwd')
# session=Session()
# # session.add(ed_User)
# session.add_all([
# User(name='wendy', fullname='Wendy Williams', password='foobar'),
# User(name='mary', fullname='Mary Contrary', password='xxg527'),
# User(name='fred', fullname='Fred Flinstone', password='blah')])
# # session.commit()
#---------------------------------------------------------------------------------------------
