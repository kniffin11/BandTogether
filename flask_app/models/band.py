from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import member
from flask import flash

db = 'band_together'

class Band:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.genre = data['genre']
        self.home_city = data['home_city']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.members = []
    
# ---------- Validate Bands ----------

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

# ---------- Get Bands ----------

    @classmethod
    def get_one(cls, data):
        query = "select * from bands where id = %(id)s;"
        band = connectToMySQL(db).query_db(query, data)
        return band

    @classmethod
    def get_all(cls):
        query = "select * from bands;"
        all_bands = connectToMySQL(db).query_db(query)
        bands = []

        for band in all_bands:
            bands.append(band)
        return bands

    @classmethod
    def get_joined_bands(cls, data):
        # gets all member ids for specific user -- correct
        query = "select id from members where user_id = %(id)s;"
        all_member_ids = connectToMySQL(db).query_db(query, data)

        # gets the band_ids based on member_ids
        band_ids = []
        for member_id in all_member_ids:
            # must query db each iteration as the member_id auto increments for all instances of the same user
            query2 = "select band_id from band_members where member_id = %(member_id)s"
            data2 = {"member_id": member_id.get('id')}
            # returns a band id
            band_id = connectToMySQL(db).query_db(query2, data2)
            band_ids.append(band_id)

        # gets bands based on band ids
        joined_bands = []
        for band_id in band_ids:
            query3 = "select name from bands where id = %(band_id)s;"
            data3 = {"band_id": band_id[0].get('band_id')}
            band = connectToMySQL(db).query_db(query3, data3)
            joined_bands.append(band[0].get('name'))
        print(joined_bands)
        return joined_bands

    @classmethod
    def get_band_with_members(cls, data):
        query = "select * from bands left join band_members on band_members.band_id = bands.id left join members on band_members.member_id = members.id WHERE bands.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        # results will be a list of member objects with the band attached to each row. 
        band = cls(results[0])
        for row_from_db in results:
            # Now we parse the member data to make instances of members and add them into our list.
            member_data = {
                "id" : row_from_db["members.id"],
                "member_id" : row_from_db["member_id"],
                "created_at" : row_from_db["members.created_at"],
                "updated_at" : row_from_db["members.updated_at"]
            }
            band.members.append(member.Member(member_data))
        return band

# ---------- Add a Band ----------

    @classmethod
    def add_new_band(cls, data):
        query = "insert into bands(name, genre, home_city, founding_member, user_id, created_at) values(%(name)s, %(genre)s, %(home_city)s, %(founding_member)s, %(user_id)s, now());"
        return connectToMySQL(db).query_db(query, data)

# ---------- Edit a Band ----------

    @classmethod
    def edit_band(cls, data):
        query = "update bands set name = %(name)s, genre = %(genre)s, home_city = %(home_city)s where id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

# ---------- Delete a Band ----------

    @classmethod
    def delete(cls, data):
        query = "delete from bands where id = %(id)s"
        return connectToMySQL(db).query_db(query, data)