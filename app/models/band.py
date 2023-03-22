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
            SELECT * FROM bands
            JOIN users ON users.id = bands.user_id;
        """
        results = mySQLconnect.connect(cls.db).run_query(query)
        bands = []
        if results:
            for info in results:
                band = cls(info)
                user_info = {
                    **info,
                    'id' : info["users.id"]
                }
                band.founder = user.User(user_info)
                bands.append(band)
        return bands
    
    @classmethod
    def get_membership(cls, data):
        query = """
            SELECT * FROM bands
            JOIN members ON members.band_id = bands.id
            WHERE bands.id=%(id)s;
        """
        results = mySQLconnect.connect(cls.db).run_query(query,data)
        membership = set()
        if results:
            for info in results:
                membership.add(info['members.user_id'])
        return membership
    
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
