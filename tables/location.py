import os
from flask import Flask, render_template, jsonify, request, Blueprint
import json
from database_connector import DatabaseConnector

location_blueprint = Blueprint('location', __name__)

supabase = DatabaseConnector().connection

## Get location by ID
@location_blueprint.route('/get_location', methods=['GET'])
def get_location_by_id():
    try: 
        location_id = request.args.get('id')

        if not location_id:
            return jsonify({"error": "Missing required parameter"}), 400

        response = supabase.table("location").select().eq("id", location_id).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# Insert location 
@location_blueprint.route('/insert_location', methods=['POST'])
def insert_location():
    try:
        latitude = request.get('latitude');
        longitude = request.get('longitude');
        address = request.get('address');
        name = request.get('name');

        if not latitude or not longitude:
            return jsonify({"error": "Missing required parameters"}), 400

        location_data = {}
        location_data['latitude'] = latitude
        location_data['longitude'] = longitude

        if address:
            location_data['address'] = address
        if name:
            location_data['name'] = name

        response = supabase.table("location").upsert([location_data]).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        
## Delete location by ID
@location_blueprint.route('/delete_location', methods=['DELETE'])
def delete_location_by_id():
    try:
        location_id = request.get('id')
        
        if not location_id:
            return jsonify({"error": "Missing required parameters"}), 400
        
        response = supabase.table("location").delete().eq("id", location_id).execute()
        
        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
## Update location by ID
@location_blueprint.route('/update_location', methods=['PUT'])
def update_location_by_id():
    try:
        location_id = request.get('id', type=int)
        latitude = request.get('latitude');
        longitude = request.get('longitude');
        address = request.get('address');
        name = request.get('name');

        if not location_id:
            return jsonify({"error": "Missing required parameters"}), 400

        update_data = {}
        if longitude:
            update_data['longitude'] = longitude
        if latitude:
            update_data['latitude'] = latitude
        if address:
            update_data['address'] = address
        if name:
            update_data['name'] = name
        
        response = supabase.table("location").update(update_data).eq('id', location_id).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
