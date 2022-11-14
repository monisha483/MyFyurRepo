import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movies, Actors


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""  
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "postgres"
        self.user = 'postgres'
        self.password = 'admin'
        self.hostname = 'localhost:5432'
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.user, self.password, self.hostname, self.database_name)
        #postgresql://postgres:admin@localhost:5432/postgres
        ExecutiveProducerToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVQbjlaMnQwdTRhZUdsc0kzd0ZYZCJ9.eyJpc3MiOiJodHRwczovL21vbi1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMzkwMzUzMjk0OTk2MzAzNDU0NCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2Njg0Mjg2MzUsImV4cCI6MTY2ODQzNTgzNSwiYXpwIjoialNJQ1lIdzdkU3dSV2dDUDZvMG1FRm1RbWlzODkxVVkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.MEWOxP6kQb1KCJa6xLBeIoFyWamyOnzYJk_INKVtSwFkM3XFIGmQ0h4xi3m9U0mv0OPJLVtd5Htb0M4UTfyfBFNDacg0-liKWLUFipV02Vlj4mxutvFgEG9v8KuPVZ52UadL0jUSb_Cf5B0KkiLEjj4R--6ALflYygR7zX-J0oTjnDhSlUrllXkB-14VaM1pVx8vAf04LYbt4JcBab2yrfqIruv-bUxc-aMAJp_Dj_AQ_NgzwxSGYh6LYtWP2FfHU4lqAqXEo3BOptfD3_ho_PG4v0VBfckd9CNbz5NDOqYq_Fk8M9fRL-Dt5W6Fd6afNPORekp8BfrJyGQwBXTuLQ'
        CastingDirectorToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVQbjlaMnQwdTRhZUdsc0kzd0ZYZCJ9.eyJpc3MiOiJodHRwczovL21vbi1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzM1Yzg2ZmU0NzEwZjYyMjIyMjBiOWYiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjY4NDMxNDU2LCJleHAiOjE2Njg0Mzg2NTYsImF6cCI6ImpTSUNZSHc3ZFN3UldnQ1A2bzBtRUZtUW1pczg5MVVZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.OS_xbeYo5_TzJx64nv67-mbKc_N21T64Z94mg33Q_SAYZ8uoBqzFZ6li4gzsziHYd_NgVsdLprdlc2MoG3gNDs5lxS_gkRRLp03Re3COSQbTez5rdCBRaZhpcO9X2PR4K7FbQkU9myh6nmmD6bAMYnP3sfLWnbx6Preem2doVMZvqwfdKJrnA1kXYEU9eZN4d2gBdM92TDE_2e3E1GsQvtFFNSmElzfUgQX18tnA4oDEBduzQ_F8YeE6rOnfQ2WMb-eVUsXucbG-ETIX1HnXCV_PwI9QTtKZnX2ZVAeOOXODbl0RhHunSaKjpwO5fnuaBipJ2P66csKMTsRwgBq0ww'
        CastingAssistantToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVQbjlaMnQwdTRhZUdsc0kzd0ZYZCJ9.eyJpc3MiOiJodHRwczovL21vbi1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzMyZGM4YmJjZjQyOWZhYzhmMzc1ZWMiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjY4NDMyNjE0LCJleHAiOjE2Njg0Mzk4MTQsImF6cCI6ImpTSUNZSHc3ZFN3UldnQ1A2bzBtRUZtUW1pczg5MVVZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.uAevWQOQ62ldUtZ5clTh73OkEJyL0FMduy7MyzDS_GWOKXV8v92X8Kpmiqjkcivsi1eMcZqH3qf6egnp57wy5LitQRV_Rm_9ynmEvv2UAjnw_bvNEoVVKk7vrlQJxRuTmRzMqkVy4qw9SPHJiXyaBsiJCxYe_O70_OhhwTGp_JRr6sp0RwRfClOnPXPWUu2PN60iTLAkkzazgfxmHRyrXedNRV5AOFeEoMfY55ONNrA7wOXctYVs26Rk7I-uKQhE4W4XjaXGf4yHYjX_JqxOv-OvB91XI54BIVFNXc8Kn5_34tf9LMaNQwCfU5fcDY_FY7TUKEjNzAXGiNFo5J-QQA'
        self.ExecutiveProducerHeader = {'Authorization':'Bearer ' + ExecutiveProducerToken}
        self.CastingDirectorHeader = {'Authorization':'Bearer ' + CastingDirectorToken}
        self.CastingAssistantHeader = {'Authorization':'Bearer ' + CastingAssistantToken}
        setup_db(self.app, self.database_path)
        self.new_actor = {
            "age": 30,
            "gender": "M",
            "id": 1,
            "name ": "Chandler"
        }
        self.patch_actor = {
            "age": 30,
            "gender": "M",
            "id": 1,
            "name ": "Chandler Bing"
        }
        self.error_actor = {
            "age": "10",
            "gender": "M"
        }
        self.new_movie = {
            "id": 1,
            "releasedate": 2014,
            "title": "HP"
        }
        self.patch_movie = {
            "id": 1,
            "releasedate": 2015,
            "title": "HP"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

#positive Test cases
#get actor
    def test_retrieve_actors(self):
        res = self.client().get("/actors", headers=self.ExecutiveProducerHeader)
        data = json.loads(res.data)
        print("get actors!! ", data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])
#get movie
    def test_retrieve_movies(self):
        res = self.client().get("/movies", headers=self.ExecutiveProducerHeader)
        data = json.loads(res.data)
        print("get movie!! ", data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])
#post actor
    def test_create_new_actor(self):
        res = self.client().post("/actors", json=self.new_actor, headers=self.ExecutiveProducerHeader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["actors"])
#post movie
    def test_create_new_movie(self):
        res = self.client().post("/movies", json=self.new_movie, headers=self.ExecutiveProducerHeader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["movie"])
#patch actor
    def test_patch_new_actor(self):
        res = self.client().patch("/actors/3", json=self.patch_actor, headers=self.ExecutiveProducerHeader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        
#patch movie
    def test_patch_new_movie(self):
            res = self.client().patch("/movies/2", json=self.patch_movie, headers=self.ExecutiveProducerHeader)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
#delete actor
    def test_delete_actor(self):
            res = self.client().delete('/actors/1', headers=self.ExecutiveProducerHeader)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["success"], True)
#delete movie
    def test_delete_movie(self):
            res = self.client().delete('/movies/1', headers=self.ExecutiveProducerHeader)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["success"], True)

#Testcases for error behavior
#error behavior - get actor
    def test_failed_retrieve_actors(self):
        res = self.client().get("/actors")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

#error behavior - get movie
    def test_failed_retrieve_movies(self):
        res = self.client().get("/movies")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
#error behavior - post actor
    def test_failed_create_new_actor(self):
        res = self.client().post("/actors", json = {}, headers=self.ExecutiveProducerHeader)
        data = json.loads(res.data)
        self.assertEqual(data['error'], 400)
#error behavior - post movie
    def test_failed_create_new_movie(self):
        res = self.client().post("/movies", json={}, headers=self.ExecutiveProducerHeader)
        data = json.loads(res.data)
        self.assertEqual(data['error'], 500)
#error behavior - patch actor
    def test_failed_patch_new_actor(self):
        res = self.client().patch("/actors/777", json=self.patch_actor, headers=self.ExecutiveProducerHeader)
        data = json.loads(res.data)
        self.assertEqual(data['error'], 401)
        
#error behavior - patch movie
    def test_failed_patch_new_movie(self):
            res = self.client().patch("/movies/777", json=self.patch_movie, headers=self.ExecutiveProducerHeader)
            data = json.loads(res.data)
            self.assertEqual(data['error'], 401)
#error behavior - delete actor
    def test_failed_delete_actor(self):
            res = self.client().delete('/actors/777', headers=self.ExecutiveProducerHeader)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 422)
            
#error behavior - delete movie
    def test_failed_delete_movie(self):
            res = self.client().delete('/movies/777', headers=self.ExecutiveProducerHeader)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 422)

#RBAC TC Casting Director
    def test_rbac_delete_movie(self):
            res = self.client().delete('/movies/1', headers=self.CastingDirectorHeader)
            data = json.loads(res.data)
            self.assertEqual(data['error'], 403)
    def test_rbac_Assistant_retrieve_actors(self):
        res = self.client().get("/actors", headers=self.CastingDirectorHeader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

#RBAC TC Casting Assistant
    def test_rbac_Assistant_patch_new_movie(self):
            res = self.client().patch("/movies/2", json=self.patch_movie, headers=self.CastingAssistantHeader)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 403)

    def test_rbac_Assistant_retrieve_actors(self):
        res = self.client().get("/actors", headers=self.CastingAssistantHeader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
            
if __name__ == "__main__":
    unittest.main()