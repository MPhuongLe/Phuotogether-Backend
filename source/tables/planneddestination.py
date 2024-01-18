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
        tripid = data.get('tripid');
        locationid = data.get('locationid');
        begintime = data.get('begintime');
        endtime = data.get('endtime');
        note = data.get('note');

        if not tripid or not locationid:
            return jsonify({"error": "Missing required parameters"}), 400
        planned_destination_data = {}

        planned_destination_data['tripid'] = tripid

        current_destinations_response = supabase.table("planneddestination").select("*").eq("tripid", tripid).order('destinationno', desc=True).execute()
        
        if current_destinations_response.data and len(current_destinations_response.data) > 0:
            max_destination_no = current_destinations_response.data[0]['destinationno']
        else:
            max_destination_no = 0
            
        planned_destination_data['destinationno'] = max_destination_no + 1
        planned_destination_data['locationid'] = locationid

        if begintime:
            planned_destination_data['begintime'] = begintime
        if endtime:
            planned_destination_data['endtime'] = endtime
        if note:
            planned_destination_data['note'] = note

        response = supabase.table("planneddestination").upsert(planned_destination_data).execute()

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
        tripid = data.get('tripid')
        destinationno = data.get('destinationno')
        
        if not tripid or not destinationno:
            return jsonify({"error": "Missing required parameters"}), 400
        
        response = supabase.table("planneddestination").delete().eq("tripid", tripid).eq("destinationno", destinationno).execute()
        
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
        tripid = data.get('tripid');
        destinationno = data.get('destinationno');
        locationid = data.get('locationid');
        begintime = data.get('begintime');
        endtime = data.get('endtime');
        note = data.get('note');

        if not tripid or not destinationno:
            return jsonify({"error": "Missing required parameters"}), 400
        update_data = {}

        update_data['tripid'] = tripid
        update_data['destinationno'] = destinationno
        if locationid:
            update_data['locationid'] = locationid
        if begintime:
            update_data['begintime'] = begintime
        if endtime:
            update_data['endtime'] = endtime
        if note:
            update_data['note'] = note
        
        response = supabase.table("planneddestination").update(update_data).eq('tripid', tripid).eq('destinationno', destinationno).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
