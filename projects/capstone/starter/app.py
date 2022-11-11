import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Actors

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
    def get_actors():
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
    def get_movies():
        selection = Movies.query.order_by(Movies.id).all()
        movies = paginate(request, selection)
        if (len(movies) == 0):
            abort(404)
        return jsonify({
            'success': True,
            'actors': movies,
            'total_movies': len(movies),
            })
    
    #endpoint to create a new actor
    @app.route('/actors', methods=['POST'])
    def insert_Actor():
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)
        try:
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

    #endpoint to create a new actor
    @app.route('/movies', methods=['POST'])
    def insert_Movie():
        body = request.get_json()
        print("hi!!")
        new_title = body.get('title', None)
        print("new_title!! ", new_title)
        new_releasedate = body.get('releasedate', None)
        print("new_releasedate!! ", new_releasedate)
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
    def delete_question(movie_id):
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
    def delete_actor(actor_id):
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
    #@requires_auth('patch:drinks')
    def update_actor(id):
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
    #@requires_auth('patch:drinks')
    def update_movie(id):
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
    
    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)