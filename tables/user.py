import os
from flask import Flask, render_template, jsonify, request, Blueprint
import json
from database_connector import DatabaseConnector

user_blueprint = Blueprint('user', __name__)

supabase = DatabaseConnector().connection

## Get all user
# @user_blueprint.route('/get_all_user', methods=['GET'])
# def get_all_user():
#     response = supabase.table("user").select("*").execute()
#     return json.dumps(response.data, ensure_ascii=False)

## Get user by ID
@user_blueprint.route('/get_user', methods=['GET'])
def get_user_by_id():
    try: 
        user_id = request.args.get('id')

        if not user_id:
            return jsonify({"error": "Missing required parameter"}), 400

        response = supabase.table("user").select("*").eq("id", user_id).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
## Get user by ID
@user_blueprint.route('/get_user_by_account', methods=['POST'])
def get_user_by_account():
    try: 
        emailortel = request.args.get('emailortel')
        password = request.args.get('password')

        if not emailortel or not password:
            return jsonify({"error": "Missing required parameter"}), 400

        response = supabase.table("user").select("*").eq("emailortel", emailortel).execute()

        user_data = response.data[0]
        if 'password' in user_data and user_data['password'] == password:
            return json.dumps(response.data, ensure_ascii=False)
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": "Invalid credentials"}), 500

# Insert user 
@user_blueprint.route('/insert_user', methods=['POST'])
def insert_user():
    try:
        emailortel = request.args.get('emailortel');
        logintype = request.args.get('logintype', type=bool);
        password = request.args.get('password');
        fullname = request.args.get('fullname');

        if not emailortel or not logintype or not password:
            return jsonify({"error": "Missing required parameters"}), 400

        user_data = {
            "emailortel": emailortel,
            "logintype": logintype,
            "password": password,
            "fullname": fullname,
        }

        response = supabase.table("user").upsert([user_data]).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
## Delete user by ID
@user_blueprint.route('/delete_user', methods=['DELETE'])
def delete_user_by_id():
    try:
        print(request)
        user_id = request.args.get('id')
        
        if not user_id:
            return jsonify({"error": "User ID is missing"}), 400
        
        response = supabase.table("user").delete().eq("id", user_id).execute()
        
        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
## Update user by ID
@user_blueprint.route('/update_user', methods=['PUT'])
def update_user_by_id():
    updated = []
    try:
        user_id = request.args.get('id', type=int)
        password = request.args.get('password')
        fullname = request.args.get('fullname')

        if not user_id or (not password and not fullname):
            return jsonify({"error": "Missing required parameters"}), 400

        update_data = {}
        if password:
            update_data['password'] = password
            updated.append('password')
        if fullname:
            update_data['fullname'] = fullname
            updated.append('fullname')

        response = supabase.table("user").update(update_data).eq('id', user_id).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
