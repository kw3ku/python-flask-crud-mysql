from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

@app.route("/")
def home():
    users = User.query.all()
    return render_template("index.html", varlist = users)
    # try:
    #     # db.session.query(User).first()
    #     users = User.query.all()
    #     # somevalue = "Connected to Sql Successfully"
    #     # mylist = ["one", "two", "three"]
    #     return render_template("index.html", varlist = users)
       
    # except Exception as e:
    #     return f"Error: {str(e)}"

# create users
@app.route('/create_user', methods=['Get', 'Post'])

def create_user():
    if request.method == 'POST':
        username = request.form['username']
        new_user = User(username=username)

        try: #check by using try to catch some errors.
            db.session.add(new_user)
            db.session.commit()

                        # Check if the data is committed by querying the database
            user_from_db = User.query.filter_by(username=username).first()

            if user_from_db:
                response = f"user {username} created successfully"
                return render_template('create_user.html', result = response)
                # return f"User '{username}' created successfully with ID: {user_from_db.id}"
            else:
                return "Failed to retrieve user from the database. Check the commit."

        except Exception as e:
            db.session.rollback()  # Rollback changes in case of an exception
            return f"Error creating user: {str(e)}"

    return render_template('create_user.html')  # Assuming you have an HTML form template



@app.route('/update_user/<int:user_id>', methods=["POST"]) # pass the paramter in the url
def update_user(user_id): #you need a paramter of id here

    new_username = request.form.get('new_username') #get the new username and store it
    get_the_user = User.query.get(user_id) # get the user id use it to locate the user

    if get_the_user: #if user is found, now perform some actions
        get_the_user.username = new_username #update the existing username with the new one
        db.session.commit() # perform the action in the database

    else:
        return "some"
    
    return redirect(url_for('home')) #return back to the home page



@app.route('/delete_user/<int:user_id>', methods=["POST"])
def delete_user(user_id): #pass the paramter here
        
        user = User.query.get(user_id) #search for the user using the id

        if user: #if user is found, now perform the delete function 
            db.session.delete(user)
            db.session.commit() #the database will perform the action
            print(f"Deleting user with ID: {user_id}")
            # response = f"user {user} deleted"
            # return render_template('index.html', dataValue = response)
            return redirect(url_for("home"))
        
        else:
            return "user not found"
        
if __name__ == "__main__":
    app.run(debug=True)



