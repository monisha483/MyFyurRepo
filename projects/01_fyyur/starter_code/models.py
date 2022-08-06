from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime

db = SQLAlchemy()
class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genre = db.Column(db.String(120))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    shows = db.relationship('Shows', backref='venue',
                            lazy=True, cascade='all, delete')

    def getVenueString(self):
      return {'id': self.id, 'name': self.name, 'genres': self.genre.split(','), 'address': self.address, 'city': self.city, 'state': self.state, 'phone': self.phone, 'website_link': self.website, 'facebook_link': self.facebook_link, 'seeking_talent': self.seeking_talent, 'seeking_description': self.seeking_description, 'image_link': self.image_link}

    def makeVenueStringWithShowCount(self):

        return {'id': self.id, 'name': self.name, 'city': self.city, 'state': self.state, 'phone': self.phone, 'address': self.address, 'image_link': self.image_link, 'facebook_link': self.facebook_link, 'website': self.website, 'seeking_talent': self.seeking_talent, 'seeking_description': self.seeking_description, 'num_shows': len(self.getUpcomingShows())}

    def makeVenueStringForSearch(self):
        return {'id': self.id, 'name': self.name, 'num_upcoming_shows': len(self.getUpcomingShows())}

    def makeVenueStringForShowVenue(self):

        return {'id': self.id, 'name': self.name, 'genre': self.genre.split(','), 'address': self.address, 'city': self.city, 'state': self.state, 'phone': self.phone, 'website': self.website, 'facebook_link': self.facebook_link, 'seeking_talent': self.seeking_talent, 'seeking_description': self.seeking_description, 'image_link': self.image_link, 'past_shows': self.getPastShows(), 'upcoming_shows': self.getUpcomingShows(), 'past_shows_count': len(self.getPastShows()), 'upcoming_shows_count': len(self.getUpcomingShows())}

    def getPastShows(self):
        showList = Shows.query.join(Venue).filter(Shows.venue_id==self.id).filter(Shows.start_time<datetime.date.today()).all()
        past_shows = []
        for s in showList:
            past_shows.append({'artist_id': s.artist_id, 'artist_name': s.artist.name, 'artist_image_link': s.artist.image_link, 'start_time': (
                s.start_time).strftime("%Y-%m-%d, %H:%M:%S")})
        return past_shows

    def getUpcomingShows(self):
        showList = Shows.query.join(Venue).filter(Shows.venue_id==self.id).filter(Shows.start_time>datetime.date.today()).all()
        up_shows = []
        for s in showList:
            up_shows.append({'artist_id': s.artist_id, 'artist_name': s.artist.name, 'artist_image_link': s.artist.image_link, 'start_time': (
                s.start_time).strftime("%Y-%m-%d, %H:%M:%S")})
        return up_shows


    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Shows', backref='artist',
                            lazy=True, cascade='all, delete')

    def makeArtistStringForSearch(self):
        return {'id': self.id, 'name': self.name, 'num_upcoming_shows': len(self.getArtistUpcomingShows())}

    def getArtistPastShows(self):
        showList = Shows.query.join(Artist).filter(Shows.venue_id==self.id).filter(Shows.start_time<datetime.date.today()).all()
        past_shows = []
        for s in showList:
            past_shows.append({'venue_id': s.venue.id, 'venue_name': s.venue.name, 'venue_image_link': s.venue.image_link, 'start_time': (
                 s.start_time).strftime("%Y-%m-%d, %H:%M:%S")})
        return past_shows

    def getArtistUpcomingShows(self):
        showList = Shows.query.join(Artist).filter(Shows.venue_id==self.id).filter(Shows.start_time>datetime.date.today()).all()
        up_shows = []
        for s in showList:
            up_shows.append({'venue_id': s.venue.id, 'venue_name': s.venue.name, 'venue_image_link': s.venue.image_link, 'start_time': (
                 s.start_time).strftime("%Y-%m-%d, %H:%M:%S")})
        return up_shows

    def makeStringForShowArtist(self):
        return {'id': self.id, 'name': self.name, 'genres': self.genres.split(','), 'city': self.city, 'state': self.state, 'phone': self.phone, 'website': self.website, 'facebook_link': self.facebook_link, 'seeking_venue': self.seeking_venue, 'seeking_description': self.seeking_description, 'image_link': self.image_link, 'past_shows': self.getArtistPastShows(), 'upcoming_shows': self.getArtistUpcomingShows(), 'past_shows_count': len(self.getArtistPastShows()), 'upcoming_shows_count': len(self.getArtistUpcomingShows())}

    def getArtistString(self):
        return {'id': self.id, 'name': self.name, 'genres': self.genres.split(','), 'city': self.city, 'state': self.state, 'phone': self.phone, 'website_link': self.website, 'facebook_link': self.facebook_link, 'seeking_venue': self.seeking_venue, 'seeking_description': self.seeking_description, 'image_link': self.image_link}


class Shows(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime())
    artist_id = db.Column(
        db.Integer, db.ForeignKey('artist.id'), nullable=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=True)

    def getShowString(self):
        venue = Venue.query.get(self.venue_id)
        artist = Artist.query.get(self.artist_id)
        return {'venue_id':venue.id,'venue_name':venue.name,'artist_id':artist.id, 'artist_name': artist.name, 'artist_image_link':artist.image_link, 'start_time':(
                self.start_time).strftime("%Y-%m-%d, %H:%M:%S")}