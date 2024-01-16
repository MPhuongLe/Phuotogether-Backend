import os
from flask import Flask, render_template, jsonify, request, Blueprint
import json
from database_connector import DatabaseConnector

album_blueprint = Blueprint('album', __name__)

supabase = DatabaseConnector().connection

## Get album by ID
@album_blueprint.route('/get_album', methods=['GET'])
def get_album_by_id():
    try: 
        album_id = request.args.get('id')

        if not album_id:
            return jsonify({"error": "Missing required parameter"}), 400

        response = supabase.table("album").select().eq("id", album_id).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

## Get albums by trip ID
@album_blueprint.route('/get_albums_by_tripid', methods=['GET'])
def get_albums_by_tripid():
    try: 
        tripid = request.args.get('tripid')

        if not tripid:
            return jsonify({"error": "Missing required parameter"}), 400

        response = supabase.table("album").select().eq("tripid", tripid).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Insert album 
@album_blueprint.route('/insert_album', methods=['POST'])
def insert_album():
    try:
        name = request.get('name');
        tripid = request.get('tripid');
        passedpoint = request.get('passedpoint');

        if not name or not tripid or not passedpoint:
            return jsonify({"error": "Missing required parameters"}), 400

        album_data = {
            'name': name,
            'tripid': tripid,
            'passedpoint': passedpoint
        }

        response = supabase.table("album").upsert([album_data]).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        
## Delete album by ID
@album_blueprint.route('/delete_album', methods=['DELETE'])
def delete_album_by_id():
    try:
        album_id = request.get('id')
        
        if not album_id:
            return jsonify({"error": "Missing required parameters"}), 400
        
        response = supabase.table("album").delete().eq("id", album_id).execute()
        
        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
## Update album by ID
@album_blueprint.route('/update_album', methods=['PUT'])
def update_album_by_id():
    try:
        album_id = request.get('id', type=int)
        name = request.get('name');
        passedpoint = request.get('passedpoint');

        if not album_id:
            return jsonify({"error": "Missing required parameters"}), 400

        update_data = {}
        if name:
            update_data['name'] = name
        if passedpoint:
            update_data['passedpoint'] = passedpoint
        if passedpoint:
            update_data['passedpoint'] = passedpoint
        
        response = supabase.table("album").update(update_data).eq('id', album_id).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
