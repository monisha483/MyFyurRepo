import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Actors
from auth import AuthError, requires_auth

DATA_PER_PAGE = 10

# paginate 
def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * DATA_PER_PAGE
    end = start + DATA_PER_PAGE
    dataset = [data.format() for data in selection]
    page_data = dataset[start:end]
    return page_data

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    
    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting
    
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(self):
        selection = Actors.query.order_by(Actors.id).all()
        actors = paginate(request, selection)
        if (len(actors) == 0):
            abort(404)
        return jsonify({
            'success': True,
            'actors': actors,
            'total_actors': len(actors),
            })
    
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(self):
        selection = Movies.query.order_by(Movies.id).all()
        movies = paginate(request, selection)
        if (len(movies) == 0):
            abort(404)
        return jsonify({
            'success': True,
            'movies': movies,
            'total_movies': len(movies),
            })
    
    #endpoint to create a new actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def insert_Actor(self):
        body = request.get_json()
        print("actor post")
        print("body!!", body)
        new_name = body.get('name', None)
        print("new_name", new_name)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)
        if new_name is None:
            print("aborting!")
            abort(400)
        try:
            print("try!")
            actor = Actors(
            name=new_name,
            age=new_age,
            gender=new_gender
            )
            actor.insert()
            selection = Actors.query.order_by(Actors.id).all()
            current_actors = paginate(request, selection)
            return jsonify({
            'success': True,
            'actors': current_actors,
            'total_actors': len(Actors.query.all())
            })
        except Exception:
            abort(422)

    #endpoint to create a new movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def insert_Movie(self):
        body = request.get_json()
        print("hi!!")
        new_title = body.get('title', None)
        print("new_title!! ", new_title)
        new_releasedate = body.get('releasedate', None)
        print("new_releasedate!! ", new_releasedate)
        if new_title is None or new_releasedate is None:
            abort(500)
        try:
            movie = Movies(
            title=new_title,
            releasedate=new_releasedate
            )
            print("formate!! ", movie.format)
            movie.insert()
            selection = Movies.query.order_by(Movies.id).all()
            current_movies = paginate(request, selection)
            return jsonify({
            'success': True,
            'movie': current_movies,
            'total_movie': len(Movies.query.all())
            })
        except Exception:
            abort(422)

    #DELETE endpoint to delete a movie
    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    @requires_auth('delete:movies')
    def delete_question(self, movie_id):
        try:
            movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            movie.delete()
            selection = Movies.query.order_by(Movies.id).all()
            current_movies = paginate(request, selection)
            return jsonify(
                {
                    "success": True,
                    "deleted": movie_id,
                    "current_movies": current_movies,
                    "total_movies": len(selection),
                }
            )
        except:
            abort(422)

    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    @requires_auth('delete:actors')
    def delete_actor(self, actor_id):
        try:
            actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
            if actor is None:
                abort(404)
            actor.delete()
            selection = Actors.query.order_by(Actors.id).all()
            current_actors = paginate(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": actor_id,
                    "current_actors": current_actors,
                    "total_actors": len(selection),
                }
            )
        except:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(self, id):
        actor = Actors.query.get(id)
        if(actor is None):
            abort(401)
        body = request.get_json()
        print('body')
        new_name = body.get('name', None)
        new_gender = body.get('gender', None)
        new_age = body.get('age', None)
        try:
            actor.name = new_name
            actor.age = new_age
            actor.gender = new_gender
            actor.update()
            return jsonify(actor.format())
        except Exception:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(self, id):
        print("in patch movies")
        movie = Movies.query.get(id)
        if(movie is None):
            abort(401)
        body = request.get_json()
        print('body ', body)
        new_title = body.get('title', None)
        print('title!!patch ', new_title)
        new_releasedate = body.get('releasedate', None)
        try:
            movie.title = new_title
            movie.releasedate = new_releasedate
            movie.update()
            return jsonify(movie.format())
        except Exception:
            abort(422)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
            }), 422

    @app.errorhandler(404)
    def notfound(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "notfound"
        }), 404

    @app.errorhandler(401)
    def unauthorised(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorised"
        }), 401


    @app.errorhandler(500)
    def internalservererror(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500
    
    @app.errorhandler(400)
    def badrequest(error):
        print("error handler!")
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "forbidden"
        }), 403

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)