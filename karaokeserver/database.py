from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        UniqueConstraint, create_engine, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
import datetime
import dateutil.parser


Base = declarative_base()


class Vendor(Base):
    __tablename__ = 'vendors'
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class Song(Base):
    __tablename__ = 'songs'
    __table_args__ = (
        UniqueConstraint('vendor_id', 'number'),
    )
    id = Column(Integer, primary_key=True)
    number = Column(String(8), nullable=False)
    title = Column(String(30), nullable=False)
    singer = Column(String(30), nullable=False)
    vendor_id = Column(Integer, ForeignKey('vendors.id'))
    created = Column(DateTime, nullable=False, default=datetime.datetime.now)
    vendor = relationship('Vendor')

    def __init__(self, vendor, number, title, singer):
        self.vendor = vendor
        self.number = number
        self.title = title
        self.singer = singer


def init_db(url):
    engine = create_engine(url)
    session = scoped_session(
        sessionmaker(engine, autoflush=True, autocommit=True))
    Base.metadata.create_all(engine)
    Base.query = session.query_property()


def get_session(url):
        engine = create_engine(url)
        session = scoped_session(
            sessionmaker(engine, autoflush=True, autocommit=True))
        return session


def get_vendor(session, name):
    vendor = session.query(Vendor).filter_by(name=name).first()
    if not vendor:
        session.begin()
        vendor = Vendor(name)
        session.add(vendor)
        session.commit()

    return vendor


def get_all_vendors(session):
    return session.query(Vendor).all()


def get_songs(session, vendor=None, number=None, title=None, singer=None,
              query_str=None, after=None, limit=None):
    query = session.query(Song).order_by(Song.title)

    if vendor:
        query = query.filter(Song.vendor == vendor)

    if query_str:
        query = query.filter(
            (Song.number == query_str) |
            Song.title.like('%' + query_str + '%') |
            Song.singer.like('%' + query_str + '%'))
    else:
        if number:
            query = query.filter(Song.number.like(number + '%'))

        if title:
            query = query.filter(Song.title.like('%' + title + '%'))

        if singer:
            query = query.filter(Song.singer.like('%' + singer + '%'))

    if after:
        if not isinstance(after, datetime.date):
            after = dateutil.parser.parse(after)
        query = query.filter(Song.created > after)

    if limit:
        query = query.limit(limit)

    return query.all()


def add_song(session, song):
    session.begin(subtransactions=True)

    orig_song = session.query(Song).filter_by(
        vendor=song.vendor, number=song.number).first()
    if orig_song:
        orig_song.title = song.title
        orig_song.singer = song.singer
    else:
        session.add(song)

    session.commit()


def add_songs(session, songs):
    now = datetime.datetime.now()
    session.begin(subtransactions=True)
    for song in songs:
        song.created = now
        add_song(session, song)
    session.commit()
    session.close()


def get_last_updated(session):
    return session.query(func.max(Song.created)).one()[0]
