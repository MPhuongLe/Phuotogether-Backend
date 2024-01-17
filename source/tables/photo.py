import os
from flask import Flask, render_template, jsonify, request, Blueprint
import json
from database_connector import DatabaseConnector

photo_blueprint = Blueprint('photo', __name__)

supabase = DatabaseConnector().connection

## Get photo by ID
@photo_blueprint.route('/get_photo', methods=['GET'])
def get_photo_by_id():
    try: 
        photo_id = request.args.get('id')

        if not photo_id:
            return jsonify({"error": "Missing required parameter"}), 400

        response = supabase.table("photo").select().eq("id", photo_id).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

## Get photos by album ID
@photo_blueprint.route('/get_photos_by_albumid', methods=['GET'])
def get_photos_by_albumid():
    try: 
        albumid = request.args.get('albumid')

        if not albumid:
            return jsonify({"error": "Missing required parameter"}), 400

        response = supabase.table("photo").select().eq("albumid", albumid).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
## Get photos by user ID
@photo_blueprint.route('/get_photos_by_userid', methods=['GET'])
def get_photos_by_userid():
    try: 
        data = request.get_json()
        userid = data.args.get('userid')

        if not userid:
            return jsonify({"error": "Missing required parameter"}), 400
        
        trips_response = supabase.table("trip").select("id").eq("userid", userid).execute()
        trips_data = trips_response.data

        if 'error' in trips_data:
            return jsonify({"error": f"Supabase error: {trips_data['error']}"}), 500

        if not trips_data:
            return jsonify({"message": "No trips found for the user"}), 404

        # Extract trip IDs
        trip_ids = [trip['id'] for trip in trips_data]

        # Retrieve albums for the user's trips
        albums_response = supabase.table("album").select("id").in_("tripid", trip_ids).execute()
        albums_data = albums_response.data

        if 'error' in albums_data:
            return jsonify({"error": f"Supabase error: {albums_data['error']}"}), 500

        if not albums_data:
            return jsonify({"message": "No albums found for the user's trips"}), 404

        # Extract album IDs
        album_ids = [album['id'] for album in albums_data]

        # Retrieve photos for the user's albums
        photos_response = supabase.table("photo").select("*").in_("albumid", album_ids).execute()
        photos_data = photos_response.data

        if 'error' in photos_data:
            return jsonify({"error": f"Supabase error: {photos_data['error']}"}), 500

        if not photos_data:
            return jsonify({"message": "No photos found for the user's albums"}), 404

        return jsonify(photos_data)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Insert photo 
@photo_blueprint.route('/insert_photo', methods=['POST'])
def insert_photo():
    try:
        data = request.get_json()
        albumid = data.get('albumid');
        time = data.get('time');
        uri = data.get('uri');
        note = data.get('note');

        if not albumid or not time or not uri:
            return jsonify({"error": "Missing required parameters"}), 400

        photo_data = {
            'albumid': albumid,
            'time': time,
            'uri': uri
        }

        if uri:
            photo_data['note'] = note

        response = supabase.table("photo").upsert([photo_data]).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

## Delete photo by ID
@photo_blueprint.route('/delete_photo', methods=['DELETE'])
def delete_photo_by_id():
    try:
        data = request.get_json()
        photo_id = data.get('id')
        
        if not photo_id:
            return jsonify({"error": "Missing required parameters"}), 400
        
        response = supabase.table("photo").delete().eq("id", photo_id).execute()
        
        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    