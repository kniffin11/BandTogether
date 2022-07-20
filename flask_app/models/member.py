from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import band
db = 'band_together'

# many to many relationship -- had issues with deletion see /quit app route in controllers/for explanation
class Member: 
    def __init__(self, db_data):
        self.id = db_data['id']
        self.member_id = db_data['member_id']
        self.members_in_band = []
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
    
    @classmethod
    def join(cls, data): 
        query = "insert into members(user_id, created_at) values(%(user_id)s, now());"
        # this returns the id of the members column 
        member_id = connectToMySQL(db).query_db(query, data)

        # create new data group for insertion into band_members table
        data2 = {
            # cast dict object to string
            "band_id": str(data.get('band_id')),
            "member_id": member_id
        }

        # insert into the connection table for the many to many relationship
        query2 = "insert into band_members(band_id, member_id) values(%(band_id)s, %(member_id)s);"
        return connectToMySQL(db).query_db(query2, data2)
    
    @classmethod
    def quit(cls, data): 
        query = "delete from members where id = %(member_id)s;"
        connectToMySQL(db).query_db(query, data)
        query2 = "delete from band_members where member_id = %(member_id)s;"
        return connectToMySQL(db).query_db(query2, data)
    
    @classmethod
    def get_members_in_band(cls, data):
        query = "select * from members left join band_members ON band_members.member_id = members.id left join bands ON band_members.band_id = bands.id WHERE members.id = %(id)s;"
        results = connectToMySQL(db).query_db( query , data )
        # results will be a list of member objects with the band attached to each row. 
        member = cls(results[0])
        for row_from_db in results:
            # Now we parse the topping data to make instances of members 
            band_data = {
                "id" : row_from_db["bands.id"],
                "name" : row_from_db["name"],
                "founding_member" : row_from_db["founding_member"],
                "genre" : row_from_db["genre"],
                "home_city" : row_from_db["home_city"],
                "created_at" : row_from_db["members.created_at"],
                "updated_at" : row_from_db["members.updated_at"]
            }
            member.members_in_band.append(band.Band(band_data))
        return member