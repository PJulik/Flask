import pydantic

from flask import Flask, jsonify, request
from flask.views import MethodView

from models import Session, Ad
from schema import CreateAd, UpdateAd


app = Flask('app')


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

def validate(schema_class, json_data):
    try:
        model = schema_class(**json_data)
        return model.dict(exclude_none=True)
    except pydantic.ValidationError as er:
        raise HttpError(400, er.errors())


@app.error_handler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'status': 'error', 'message': error.message})
    response.status_code = error.status_code
    return response


def get_ad(session, ad_id: int):
    ad = session.get(Ad, ad_id)
    if ad is None:
        raise HttpError(404, 'ad not found')
    return ad


class AdView(MethodView):
    def get(self, ad_id):
        with Session as session:
            ad = get_ad(session, ad_id)
            return jsonify(
                {
                'id': ad.id,
                'name': ad.name,
                'description': ad.description,
                'creation_date': ad.creation_date.isoformat(),
            }
        )


    def post(self):
        json_data = validate(CreateAd, request.json)
        with Session() as session:
            ad = Ad(**json_data)
            session.add(ad)
            session.commit()
            return jsonify({'id': ad.id})

    def patch(self, ad_id):
        json_data = validate(UpdateAd, request.json)
        with Session() as session:
            ad = get_ad(session, ad_id)
            for k, v in json_data.items():
                setattr(ad, k, v)
            session.add(ad)
            session.commit()
            return jsonify({'id': ad.id})


    def delete(self, ad_id):
        with Session() as session:
            ad = get_ad(session, ad_id)
            session.delete(ad)
            session.commit()
            return jsonify({'status': 'deleted'})

ad_view = AdView.as_view('ad')

app.add_url_rule('/ad/', view_func=ad_view, methods=['POST'])
app.add_url_rule('/ad/<int:ad_id>', view_func=ad_view,
                 methods=['GET', 'PATCH', 'DELETE'])

if __name__ == "__main__":
    app.run()