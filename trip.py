import os
from flask import Flask, render_template, jsonify, request, Blueprint
import json
from database_connector import DatabaseConnector

trip_blueprint = Blueprint('trip', __name__)

supabase = DatabaseConnector().connection

## Get all trip
# @trip_blueprint.route('/get_all_trip', methods=['GET'])
# def get_all_trip():
#     response = supabase.table("trip").select("*").execute()
#     return json.dumps(response.data, ensure_ascii=False)

## Get trip by ID
@trip_blueprint.route('/get_trip', methods=['GET'])
def get_trip_by_id():
    try: 
        trip_id = request.args.get('id')

        if not trip_id:
            return jsonify({"error": "Missing required parameter"}), 400

        response = supabase.table("trip").select("id", "name", "departureplace", "arrivalplace", "departuredate", "arrivaldate").eq("id", trip_id).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

## Get trip by ID
@trip_blueprint.route('/get_trips_by_userid', methods=['GET'])
def get_trips_by_userid():
    try: 
        userid = request.args.get('userid')

        if not userid:
            return jsonify({"error": "Missing required parameter"}), 400

        response = supabase.table("trip").select("id", "name", "departuredate", "arrivaldate").eq("userid", userid).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
    
# Insert trip 
@trip_blueprint.route('/insert_trip', methods=['POST'])
def insert_trip():
    try:
        userid = request.args.get('userid');
        name = request.args.get('name');
        departureplace = request.args.get('departureplace');
        arrivalplace = request.args.get('arrivalplace');
        departuredate = request.args.get('departuredate');
        arrivaldate = request.args.get('arrivaldate');

        if not userid or not name or not departureplace or not arrivalplace or not departuredate or not arrivaldate:
            return jsonify({"error": "Missing required parameters"}), 400

        trip_data = {}
        trip_data['userid'] = userid
        trip_data['name'] = name
        trip_data['arrivalplace'] = arrivalplace

        if departureplace:
            trip_data['departureplace'] = departureplace
        if departuredate:
            trip_data['departuredate'] = departuredate
        if arrivaldate:
            trip_data['arrivaldate'] = arrivaldate

        response = supabase.table("trip").upsert([trip_data]).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        
## Delete trip by ID
@trip_blueprint.route('/delete_trip', methods=['DELETE'])
def delete_trip_by_id():
    try:
        trip_id = request.args.get('id')
        
        if not trip_id:
            return jsonify({"error": "Missing required parameters"}), 400
        
        response = supabase.table("trip").delete().eq("id", trip_id).execute()
        
        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
## Update trip by ID
@trip_blueprint.route('/update_trip', methods=['PUT'])
def update_trip_by_id():
    try:
        trip_id = request.args.get('id', type=int)
        name = request.args.get('name');
        departureplace = request.args.get('departureplace');
        arrivalplace = request.args.get('arrivalplace');
        departuredate = request.args.get('departuredate');
        arrivaldate = request.args.get('arrivaldate');

        if not trip_id:
            return jsonify({"error": "Missing required parameters"}), 400

        update_data = {}
        if name:
            update_data['name'] = name
        if departureplace:
            update_data['departureplace'] = departureplace
        if arrivalplace:
            update_data['arrivalplace'] = arrivalplace
        if departuredate:
            update_data['departuredate'] = departuredate
        if arrivaldate:
            update_data['arrivaldate'] = arrivaldate
        
        response = supabase.table("trip").update(update_data).eq('id', trip_id).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

