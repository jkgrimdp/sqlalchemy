from flask import Flask, request, jsonify
from db import *
from organization import Organization
from user import User

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://jacobgrimshaw@127.0.0.1:5432/alchemy"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app, db)


def create_all():
    with app.app_context():
        print("Creating Tables")
        db.create_all()
        print("All Done!")

# Get all

@app.route('/orgs/get', methods=['GET'])
def get_all_active_orgs():
    results = db.session.query(Organization).filter(Organization.active == True).all()

    return [{
            'org_id' : org.org_id,
            'name' : org.name,
            'phone': org.phone,
            'city': org.city,
            'state': org.state,
            'active': org.active,
        } for org in results]

@app.route('/users/get', methods=['GET'])
def get_all_active_users():
    results = db.session.query(User).filter(User.active == True).all()
    
    return [{
            'user_id' : user.user_id,
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'email': user.email,
            'phone': user.phone,
            'city': user.city,
            'state': user.state,
            'org_id': user.org_id,
            'active': user.active,
        } for user in results]
    
# Create / Add

@app.route("/user/add", methods=["POST"])
def add_user():
    post_data = request.json
    first_name = post_data.get("first_name")
    last_name = post_data.get('last_name')
    email = post_data.get('email')
    phone = post_data.get('phone')
    city = post_data.get('city')
    state = post_data.get('state')
    org_id = post_data.get('org_id')
    active = post_data.get('active')

    record = User(first_name, last_name, email, phone, city, state, org_id, active)

    db.session.add(record)
    db.session.commit()
    return jsonify("user added"), 200

@app.route('/org/add', methods=['POST'])
def add_org():
    post_data = request.json
    name = post_data.get('name')
    phone = post_data.get('phone')
    city = post_data.get('city')
    state = post_data.get('state')
    active = post_data.get('active')

    record = Organization(name, phone, city, state, active)
    db.session.add(record)
    db.session.commit()

    return jsonify("org created"), 200

# Update

@app.route('/user/update/<user_id>', methods=['POST', 'PUT'])
def user_update(user_id):
    post_data = request.json
    first_name = post_data.get("first_name")
    last_name = post_data.get("last_name")
    email = post_data.get('email')
    phone = post_data.get('phone')
    city = post_data.get('city')
    state = post_data.get('state')
    org_id = post_data.get('org_id')
    active = post_data.get('active')


    user_record = db.session.query(User).filter(User.user_id == user_id).first()

    if len(first_name) > 0:
        user_record.first_name = first_name
    if len(last_name) > 0:
        user_record.last_name = last_name
    if len(email) > 0:
        user_record.email = email
    if len(phone) > 0:
        user_record.phone = phone
    if len(city) > 0:
        user_record.city = city
    if len(state) > 0:
        user_record.state = state
    if len(org_id) > 0:
        user_record.org_id = org_id
    if active:
        user_record.active = active
    
    db.session.commit()
    return jsonify("user updated"), 200

@app.route('/org/update/<org_id>', methods=['POST', 'PUT'])
def org_update(org_id):
    post_data = request.json
    name = post_data.get("name")
    phone = post_data.get('phone')
    city = post_data.get('city')
    state = post_data.get('state')
    active = post_data.get('active')
    users = post_data.get('users')

    org_record = db.session.query(Organization).filter(Organization.org_id == org_id).first()

    if len(name) > 0:
        org_record.name = name
    if len(phone) > 0:
        org_record.phone = phone
    if len(city) > 0:
        org_record.city = city
    if len(state) > 0:
        org_record.state = state
    if active:
        org_record.active = active
    
    
    db.session.commit()
    return jsonify("org updated"), 200
    
# Get by ID

@app.route('/user/get/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = db.session.query(User).filter(User.user_id == user_id).first()
    
    return [{
            'user_id' : user.user_id,
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'email': user.email,
            'phone': user.phone,
            'city': user.city,
            'state': user.state,
            'org_id': user.org_id,
            'active': user.active,
        }]

@app.route('/org/get/<org_id>', methods=['GET'])
def get_org_by_id(org_id):
    org = db.session.query(Organization).filter(Organization.org_id == org_id).first()

    return [{
            'org_id' : org.org_id,
            'name' : org.name,
            'phone': org.phone,
            'city': org.city,
            'state': org.state,
            'active': org.active,
        }]

# Activate

@app.route('/user/activate/<user_id>', methods=['GET'])
def user_activate(user_id):
    user_changed = User.query.filter_by(user_id = user_id).update(dict(active=True))

    # user_record = db.session.query(User).filter(User.user_id == user_id).first()
    # user_record.active = True

    db.session.commit()
    return jsonify("user activated"), 200

@app.route('/org/activate/<org_id>', methods=['GET'])
def org_activate(org_id):
    org_changed = Organization.query.filter_by(org_id = org_id).update(dict(active=True))

    # user_record = db.session.query(User).filter(User.user_id == user_id).first()
    # user_record.active = True

    db.session.commit()
    return jsonify("org activated"), 200

# Deactivate

@app.route('/user/deactivate/<user_id>', methods=['GET'])
def user_deactivate(user_id):
    user_changed = User.query.filter_by(user_id = user_id).update(dict(active=False))

    # user_record = db.session.query(User).filter(User.user_id == user_id).first()
    # user_record.active = False
   
    db.session.commit()
    return jsonify("user deactivated"), 200

@app.route('/org/deactivate/<org_id>', methods=['GET'])
def org_deactivate(org_id):
    org_changed = Organization.query.filter_by(org_id = org_id).update(dict(active=False))

    # user_record = db.session.query(User).filter(User.user_id == user_id).first()
    # user_record.active = True

    db.session.commit()
    return jsonify("org deactivated"), 200

# Delete

@app.route('/user/delete/<user_id>')
def delete_user(user_id):
  db.session.query(User.user_id == user_id).delete()
  db.session.commit()
  return jsonify("User deleted"), 200

@app.route('/org/delete/<org_id>')
def delete_org(org_id):
  db.session.query(Organization.org_id == org_id).delete()
  db.session.commit()
  return jsonify("Org deleted"), 200

if __name__ == "__main__":
    create_all()
    app.run(port=8086, host="0.0.0.0")