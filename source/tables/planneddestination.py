import os
from flask import Flask, render_template, jsonify, request, Blueprint
import json
from database_connector import DatabaseConnector

planned_destination_blueprint = Blueprint('planned_destination', __name__)

supabase = DatabaseConnector().connection

## Get planned_destination by ID
@planned_destination_blueprint.route('/get_planned_destination', methods=['GET'])
def get_planned_destination_by_id():
    print('Hello')
    try: 
        trip_id = request.args.get('tripid')
        destination_no = request.args.get('destination_no')

        if not trip_id or not destination_no:
            return jsonify({"error": "Missing required parameter"}), 400

        response = supabase.table("planneddestination").select("*").eq("tripid", trip_id).eq("destinationno", destination_no).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

## Get planned_destinations by trip ID
@planned_destination_blueprint.route('/get_planned_destinations_by_tripid', methods=['GET'])
def get_planned_destinations_by_tripid():
    try: 
        tripid = request.args.get('tripid')

        if not tripid:
            return jsonify({"error": "Missing required parameter"}), 400

        response = supabase.table("planneddestination").select("*").eq("tripid", tripid).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
    
# Insert planned_destination 
@planned_destination_blueprint.route('/insert_planned_destination', methods=['POST'])
def insert_planned_destination():
    try:
        data = request.get_json()
        userid = data.get('userid');
        name = data.get('name');
        departureplace = data.get('departureplace');
        arrivalplace = data.get('arrivalplace');
        departuredate = data.get('departuredate');
        arrivaldate = data.get('arrivaldate');

        if not userid or not name or not departureplace or not arrivalplace or not departuredate or not arrivaldate:
            return jsonify({"error": "Missing required parameters"}), 400

        planned_destination_data = {}
        planned_destination_data['userid'] = userid
        planned_destination_data['name'] = name
        planned_destination_data['arrivalplace'] = arrivalplace

        if departureplace:
            planned_destination_data['departureplace'] = departureplace
        if departuredate:
            planned_destination_data['departuredate'] = departuredate
        if arrivaldate:
            planned_destination_data['arrivaldate'] = arrivaldate

        response = supabase.table("planneddestination").upsert([planned_destination_data]).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        
## Delete planned_destination by ID
@planned_destination_blueprint.route('/delete_planned_destination', methods=['DELETE'])
def delete_planned_destination_by_id():
    try:
        data = request.get_json()
        planned_destination_id = data.get('id')
        
        if not planned_destination_id:
            return jsonify({"error": "Missing required parameters"}), 400
        
        response = supabase.table("planneddestination").delete().eq("id", planned_destination_id).execute()
        
        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
## Update planned_destination by ID
@planned_destination_blueprint.route('/update_planned_destination', methods=['PUT'])
def update_planned_destination_by_id():
    try:
        data = request.get_json()
        planned_destination_id = data.get('id', type=int)
        name = data.get('name');
        departureplace = data.get('departureplace');
        arrivalplace = data.get('arrivalplace');
        departuredate = data.get('departuredate');
        arrivaldate = data.get('arrivaldate');

        if not planned_destination_id:
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
        
        response = supabase.table("planneddestination").update(update_data).eq('id', planned_destination_id).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
