from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audio.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class AudioFile(Resource):
    @staticmethod
    def get(audio_file_type, audio_file_id=None):
        status = 200
        if audio_file_type.lower() == 'song':
            if audio_file_id:
                data = Song.query.get(audio_file_id)
                if data:
                    response = {'Id': data.Id, 'songName': data.SongName, 'duration': data.Duration,
                                'date': str(data.UploadedTimestamp)}
                else:
                    response = "Song not found"
                    status = 400
            else:
                data = Song.query.all()
                response = [{'Id': i.Id, 'songName': i.SongName, 'duration': i.Duration,
                             'date': str(i.UploadedTimestamp)} for i in data]
        elif audio_file_type.lower() == 'podcast':
            if audio_file_id:
                data = Podcast.query.get(audio_file_id)
                if data:
                    response = {'Id': data.Id, 'podcastName': data.PodcastName, 'duration': data.Duration,
                                'host': data.Host, 'date': str(data.UploadedTimestamp),
                                'participants': data.Participants.split(', ')}
                else:
                    response = "Podcast not found"
                    status = 400
            else:
                data = Podcast.query.all()
                response = [{'Id': i.Id, 'podcastName': i.PodcastName, 'duration': i.Duration, 'host': i.Host,
                             'date': str(i.UploadedTimestamp), 'participants': i.Participants.split(', ')}
                            for i in data]
        elif audio_file_type.lower() == 'audiobook':
            if audio_file_id:
                data = AudioBook.query.get(audio_file_id)
                if data:
                    response = {'Id': data.Id, 'title': data.Title, 'author': data.Author, 'narrator': data.Narrator,
                                'duration': data.Duration, 'date': str(data.UploadedTimestamp)}
                else:
                    response = "Audio Book not found"
                    status = 400
            else:
                data = AudioBook.query.all()
                response = [{'Id': i.Id, 'title': i.Title, 'author': i.Author, 'narrator': i.Narrator,
                             'duration': i.Duration, 'date': str(i.UploadedTimestamp)} for i in data]
        else:
            response = "Invalid Audio Type"
            status = 400
        return {'response': response}, status

    @staticmethod
    def post(audio_file_type):
        payload = request.json
        if audio_file_type.lower() == 'song':
            record = Song(payload)
        elif audio_file_type.lower() == 'podcast':
            record = Podcast(payload)
        elif audio_file_type.lower() == 'audiobook':
            record = AudioBook(payload)
        else:
            return {"response": "Invalid Audio Type"}, 400
        db.session.add(record)
        db.session.commit()
        return {'response': f'record has been added successfully, Id is {record.Id}'}

    @staticmethod
    def put(audio_file_type, audio_file_id):
        payload = request.json
        if audio_file_type.lower() == 'song':
            record = Song.query.get(audio_file_id)
            if not record:
                return {"response": "Song not found"}, 400
            if payload.get('songName'):
                record.SongName = payload.get('songName')
            if payload.get('duration'):
                record.Duration = payload.get('duration')
        elif audio_file_type.lower() == 'podcast':
            record = Podcast.query.get(audio_file_id)
            if not record:
                return {"response": "Podcast not found"}, 400
            if payload.get('podcastName'):
                record.PodcastName = payload.get('podcastName')
            if payload.get('duration'):
                record.Duration = payload.get('duration')
            if payload.get('host'):
                record.Duration = payload.get('host')
            if payload.get('participants'):
                record.Duration = ", ".join(payload.get('participants'))
        elif audio_file_type.lower() == 'audiobook':
            record = AudioBook.query.get(audio_file_id)
            if not record:
                return {"response": "Audio Book not found"}, 400
            if payload.get('title'):
                record.PodcastName = payload.get('title')
            if payload.get('duration'):
                record.Duration = payload.get('duration')
            if payload.get('author'):
                record.Author = payload.get('author')
            if payload.get('narrator'):
                record.Narrator = payload.get('narrator')
        else:
            return {"response": "Invalid Audio Type"}, 400

        db.session.commit()
        return {"response": f"{audio_file_type}-{audio_file_id} has been updated successfully."}

    @staticmethod
    def delete(audio_file_type, audio_file_id):
        if audio_file_type.lower() == 'song':
            status = Song.query.filter(Song.Id == audio_file_id).delete()
        elif audio_file_type.lower() == 'podcast':
            status = Podcast.query.filter(Podcast.Id == audio_file_id).delete()
        elif audio_file_type.lower() == 'audiobook':
            status = AudioBook.query.filter(AudioBook.Id == audio_file_id).delete()
        else:
            return {"response": "Invalid Audio Type"}, 400

        if status:
            db.session.commit()
            return {"response": f"{audio_file_type} has been deleted successfully."}
        else:
            return {"response": "Given Audio Id is not found"}, 400


class Song(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    SongName = db.Column(db.String(100), nullable=False)
    Duration = db.Column(db.Integer, nullable=False)
    UploadedTimestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, payload):
        self.SongName = payload.get('songName')
        self.Duration = payload.get('duration')
        self.UploadedTimestamp = func.now()


class Podcast(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    PodcastName = db.Column(db.String(100), nullable=False)
    Duration = db.Column(db.Integer, nullable=False)
    UploadedTimestamp = db.Column(db.DateTime, nullable=False)
    Host = db.Column(db.String(100), nullable=False)
    Participants = db.Column(db.Text, nullable=True)

    def __init__(self, payload):
        self.PodcastName = payload.get('podcastName')
        self.Duration = payload.get('duration')
        self.UploadedTimestamp = func.now()
        self.Host = payload.get('host')
        self.Participants = ", ".join(payload.get('participants', []))


class AudioBook(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(100), nullable=False)
    Author = db.Column(db.String(100), nullable=False)
    Narrator = db.Column(db.String(100), nullable=False)
    Duration = db.Column(db.Integer, nullable=False)
    UploadedTimestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self, payload):
        self.Title = payload.get('title')
        self.Author = payload.get('author')
        self.Narrator = payload.get('narrator')
        self.Duration = payload.get('duration')
        self.UploadedTimestamp = func.now()


api.add_resource(AudioFile, '/<audio_file_type>', '/<audio_file_type>/<audio_file_id>')

if __name__ == '__main__':
    app.run(debug=True)