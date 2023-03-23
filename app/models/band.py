from app.models import base, user
from app.config import mySQLconnect
from flask import flash

class Band(base.Base):
    db='band_db'
    tbl_name='bands'
    def __init__(self, data) -> None:
        super().__init__(data)
        self.name = data['name']
        self.genre = data['genre']
        self.home_city = data['home_city']
    
    @classmethod
    def get_all(cls):
        query = """
            SELECT bands.*, 
            json_object(
                "id", creator.id,
                "first_name", creator.first_name,
                "last_name", creator.last_name,
                "email", creator.email,
                "password", creator.password,
                "mumbo_jumbo", creator.mumbo_jumbo,
                "created_at", creator.created_at,
                "updated_at", creator.updated_at
            ) as creator_obj,
            if(
                count(members.id) = 0, 
                json_array(),
                json_arrayagg(
                    json_object(
                        "id", member.id,
                        "first_name", member.first_name,
                        "last_name", member.last_name,
                        "email", member.email,
                        "password", member.password,
                        "mumbo_jumbo", member.mumbo_jumbo,
                        "created_at", member.created_at,
                        "updated_at", member.updated_at
                    )
                )
            ) as member_list
            FROM bands
            JOIN users as creator ON bands.user_id = creator.id
            LEFT JOIN members ON members.band_id = bands.id 
            LEFT JOIN users as member ON members.user_id = member.id
            GROUP BY bands.id;
        """
        results = mySQLconnect.connect(cls.db).run_query(query)
        bands = []
        if results:
            for info in results:
                band = cls(info)
                band.founder = user.User(eval(info['creator_obj']))
                band.members = [user.User(member) for member in eval(info['member_list'])]
                bands.append(band)
        return bands
    
    @staticmethod
    def is_valid(data:dict):
        error = {}
        if len(data['name']) < 2:
            error['name'] = 'Name cannot be less than 2 character'
        
        if len(data['genre']) < 2:
            error['genre'] = 'Genre cannot be less than 2 character'
            
        if len(data['home_city']) < 2:
            error['home_city'] = 'Home city cannot be less than 2 character'
            
        for catagory, message in error.items():
            flash(message)
        
        return not bool(error)
