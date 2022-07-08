from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

db = 'band_together'

class Band:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.genre = data['genre']
        self.home_city = data['home_city']
        # self.founding_member = data['founding_member']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @staticmethod
    def validate_band(band):
        is_valid = True 
        if len(band['name']) < 2:
            flash("Band Name must be at least 2 characters.")
            is_valid = False
        if len(band['genre']) < 2:
            flash("Genre must be at least 2 characters.")
            is_valid = False
        if len(band['home_city']) < 1:
            flash("Home City must be at filled out.")
            is_valid = False    
        return is_valid

    @classmethod
    def get_all(cls):
        query = "select * from bands;"
        all_bands = connectToMySQL(db).query_db(query)
        bands = []

        for band in all_bands:
            bands.append(cls(band))
        return bands

    @classmethod
    def add_new_band(cls, data):
        query = "insert into bands(name, genre, home_city, founding_member, user_id, created_at) values(%(name)s, %(genre)s, %(home_city)s, %(founding_member)s, %(user_id)s, now());"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def edit_band(cls, data):
        query = "update bands set name = %(name)s, genre = %(genre)s, home_city = %(home_city)s where id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "delete from bands where id = %(id)s"
        return connectToMySQL(db).query_db(query, data)