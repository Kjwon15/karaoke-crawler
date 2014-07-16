from . import ky, tj
from ..database import Song, DbManager


def crawl(db_url):
    manager = DbManager(db_url)

    vendor_ky = manager.get_vendor('KY')
    songs = (Song(vendor_ky, r.number, r.title, r.singer) for r
             in ky.crawl())
    manager.add_songs(songs)

    vendor_tj = manager.get_vendor('TJ')
    songs = (Song(vendor_tj, r.number, r.title, r.singer) for r
             in tj.crawl())
    manager.add_songs(songs)
