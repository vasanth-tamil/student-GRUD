#! /usr/bin/env python3

from flask import Flask, redirect, render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy

# custom import 
from config import *

web = Flask(__name__)
web.config["SECRET_KEY"] = config.get("secret_key")
web.config["SQLALCHEMY_DATABASE_URI"] = config.get("database_file")

# create database 
db = SQLAlchemy(web)

class students(db.Model) : 
	Id = db.Column("id", db.Integer, primary_key=True)
	Name = db.Column(db.String(20))
	Address = db.Column(db.String(20))
	Course = db.Column(db.String(20))

	def __init__(self, Name, Address, Course) : 
		self.Name = Name 
		self.Address = Address
		self.Course = Course

# end database 
@web.route("/showDatas")
def showDatas() :
	student_list = students.query.all() 
	return render_template("showDatas.html", datas=student_list)

@web.route("/")
def home() : 
	return render_template("sqlalchemy_home.html")

@web.route("/saveData", methods=['GET', 'POST'])
def saveData() : 
	if request.method == 'POST' : 
		if not request.form["student_name"] or not request.form["address"] or not request.form["course"] : 
			flash("Please Fill All Fields", "error")
			return redirect(url_for("home"))
		else :

			if students.query.filter_by(Name = request.form["student_name"]).first() : 
				flash("Not Available Username", "error")
				return redirect("/")
			else : 
				student = students(request.form["student_name"], request.form["address"], request.form["course"]) 
				# add database and commit 
				db.session.add(student)
				db.session.commit()
				flash("DataSaved Successfully", "success")
				return redirect(url_for("home"))

# delete Data
@web.route('/deleteData/<ID>')
def deleteData(ID) : 
	student = students.query.filter_by(Id=ID).first()
	db.session.delete(student)
	db.session.commit()

	return redirect("/showDatas")
	
# update data 
@web.route("/updateDatas", methods=['GET', 'POST'])
def updateData() : 
	if request.method == 'POST' : 
		if not request.form['ID'] or not request.form['student_name'] or not request.form['address'] or not request.form['course'] : 
			flash("Please Fill All Fields", error)
			return redirect("/showDatas")
		else : 
			student = students.query.filter_by(Id=request.form["ID"]).first()
			
			if len(students.query.filter_by(Name=request.form["student_name"]).all()) == 1 : 
				student.Id = student.Id
				student.Name = request.form['student_name']
				student.Address = request.form["address"]
				student.Course = request.form["course"]

				db.session.commit()

				flash("Data Updated Successfully", "success")
				return redirect(f"/editData/{student.Id}")
				
			else : 
				flash("User Already Exist", "error")
				return redirect(f"/editData/{student.Id}")

# edit datas
@web.route("/editData/<ID>")
def editData(ID) : 
	student = students.query.filter_by(Id=ID).first()
	
	return render_template("sqlalchemy_update.html", data=student)

# 404 page not found error
@web.errorhandler(404)
def pageNotFound(error):
	return render_template("404.html");

if __name__ == "__main__" :
	db.create_all() 
	web.run(debug=True, port=config.get('port'))