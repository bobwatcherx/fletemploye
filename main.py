from flet import *
import sqlite3
import datetime

conn = sqlite3.connect('db/dbmain.db',check_same_thread=False)
cursor = conn.cursor()

class MyLogin(UserControl):
	"""docstring for MyLogin"""
	def __init__(self,width):
		super(MyLogin, self).__init__()
		self.widthsrc = width
		self.username = TextField(label="username",
					bgcolor="white",

			)
		self.password = TextField(label="password",
					bgcolor="white",
					filled=True,
					border=InputBorder.UNDERLINE,
					 can_reveal_password=True,
					 password=True,

			)
		self.resetid = Text()
		self.dialog = AlertDialog(
			title=Text("Register account",size=30),
			content=Column([
				self.username,
				self.password,
				
				]),
			actions=[
				TextButton("Register Now",
					on_click=self.processregister
					)
				],
			actions_alignment="end"
			)

		self.dialogForgotPassword = AlertDialog(
			title=Text("Forgot Password ",weight="bold"),
			content=Container(
				content=Column([
				Text("Insert Username If You Have",weight="bold"),
				self.username,
				])
				),
			actions=[
			ElevatedButton("Find User ",
				bgcolor="red",color="white",
				on_click=self.finduser
				)
			],
			actions_alignment="end"
			)
		self.dialogResetPassword = AlertDialog(
			title=Container(
				bgcolor="red",
				padding=10,
				width=400,
				content=Text("Reset Password ",weight="bold",
					color="white"
					)
				),
			content=Column([
				Text("username Found",size=25,weight="bold"),
				self.password,
				ElevatedButton("Reset Now",
					bgcolor="red",color="white",
					on_click=self.resetpassword
					)
				])
			)


	def build(self):
		return Column(
			alignment=alignment.center,
			controls=[
		Container(
			border_radius=30,
			bgcolor="black",
			margin=margin.only(top=100,left=30,right=30),
			padding=10,
			content=Column([
				Row([
					Text("Login Here",size=25,
				color="white"
					),
					IconButton("person_add",
						icon_color="white",
						tooltip="Register now",
						on_click=self.registeraccount
						)
					],alignment="spaceBetween"),
				self.username,
				self.password,
				Row([
					TextButton("Forgot Password",
						style=ButtonStyle(
							color={
							MaterialState.DEFAULT:"white"
							}
							),
						on_click=self.forgotpassword
						)

					],alignment="end"),
				Row([
					ElevatedButton("login",
				bgcolor="blue",color="white",
				width=150,
				on_click=self.loginnow
					)

					],alignment="center"),
				

				])

				)

		])

	# CHECK USER IF EXISTS
	def check_user(username, password):
		sql = "SELECT * FROM users WHERE username = ? AND password = ?"
		val = (username, password)
		cursor.execute(sql, val)
		myresult = cursor.fetchall()
		if len(myresult) > 0:
			return True
		else:
			return False

	def loginnow(self,e):
		username = self.username.value
		password = self.password.value
		login_with = "manual"

		if MyLogin.check_user(username, password):
			sql = "UPDATE users SET login_with = ?, time_login = datetime('now') WHERE username = ?"
			val = (login_with, username)
			cursor.execute(sql, val)
			conn.commit()
			print(cursor.rowcount, "record(s) updated.")
			self.page.snack_bar = SnackBar(
            Text("Success Login",size=30),
            bgcolor="blue"
            )
			self.page.snack_bar.open = True
			now = datetime.datetime.now()
			logindata = {
            "value":True,
            "username":username,
            "day_login":now.strftime("%Y-%m-%d"),
            "time_login":now.strftime("%H:%M:%S")
            }
			self.page.session.set("login", logindata)
			self.page.go("/employee")
			self.username.value = ""
			self.password.value = ""
			print(self.page.route)
			self.page.update()
		else:
			self.username.value = ""
			self.password.value = ""
			print("Invalid username or password.")
			self.page.snack_bar = SnackBar(
            Text("Invalid Login Guys!!",size=30),
            bgcolor="red"
            )
			self.page.snack_bar.open = True
			self.update()
		self.page.update()

	def resetpassword(self,e):
		try:
			new_password = self.password.value
			user_id = self.resetid.value
			query = f"UPDATE users SET password='{new_password}' WHERE user_id={user_id}"
			cursor.execute(query)
			conn.commit()
			print("Success Change password")
			self.page.window_close()
			self.page.update()
			self.page.snack_bar = SnackBar(
            Text("Password Success Change",size=30),
            bgcolor="green"
            )
			self.page.snack_bar.open = True
			self.page.go("/")
			self.page.update()
		except Exception as e:
			print(e)
			print("Error CHECK !!!")

	def finduser(self,e):
		print("find user")
		username = self.username.value
		cursor.execute("SELECT username,user_id FROM users WHERE username=?", (username,))
		result = cursor.fetchone()
		if result is None:
			self.dialogForgotPassword.open = False
			self.username.value = ""
			self.page.snack_bar = SnackBar(
            Text("Username Not Found",size=30),
            bgcolor="red"
            )
			self.page.snack_bar.open = True
			self.page.update()
		else:
			print(result[1])
			self.resetid.value = result[1]
			self.page.dialog = self.dialogResetPassword
			self.dialogResetPassword.open = True
			self.page.update()
			self.dialogForgotPassword.open = False
			self.page.update()

	def forgotpassword(self,e):
		self.page.dialog = self.dialogForgotPassword
		self.dialogForgotPassword.open = True
		self.page.update()

	def signwithgoogle(self,e):
		self.page.login(self.provider)



	def processregister(self, e):
		username = self.username.value
		password = self.password.value
		login_with = "manual"
		if username == "" and password == "":
			self.dialog.open = False
			self.page.snack_bar = SnackBar(
	            Text("Not Empty username and password", size=30),
	            bgcolor="red"
	        )
			self.page.snack_bar.open = True
			self.page.update()
		else:
			try:
				sql = "INSERT INTO users (username, password, login_with, time_login) VALUES (?, ?, ?, ?)"
				val = (username, password, login_with, datetime.datetime.now())
				cursor.execute(sql, val)
				conn.commit()
				print(cursor.rowcount, "record inserted.")
				self.page.snack_bar = SnackBar(
	            Text("Success Created Account", size=30),
	            bgcolor="green"
	        )
				self.page.snack_bar.open = True
				self.dialog.open = False
				self.username.value = ""
				self.password.value = ""
				self.page.update()
			except Exception as e:
				print(e)
				print("error Check !!!!")


	

	def registeraccount(self,e):
		
		self.page.dialog = self.dialog
		self.dialog.open = True
		self.page.update()




class EmployePage(UserControl):
	def __init__(self):
		super(EmployePage, self).__init__()

		self.now = datetime.datetime.now()
		self.emp_id = TextField(label="emp_id")
		self.full_name = TextField(label="fullname")
		self.first_name = TextField(label="firstname")
		self.employe_in_date = TextField(label="Birth Day",
			hint_text="dd-mm-yy"
			)
		self.employe_out_date = TextField(
			label="employe out",
			hint_text="dd-mm-yy"
			)
		self.cnic = TextField(label="cnic")
		self.gender = RadioGroup(
			content=Row([
				Text("Gender"),
				Radio(value="male",label="male"),
				Radio(value="female",label="female"),

				])
			)
		self.design = TextField(label="desig")
		self.education = TextField(label="hight education")
		self.contact = TextField(label="contact")
		self.email = TextField(label="email")
		self.salary = TextField(label="salary")
		self.address = TextField(label="address")

		self.searchtable = TextField("",on_change=lambda e:self.carinama(e))
		self.mytable = DataTable(
			data_row_color={"hovered": "0x30FF0000"},
			divider_thickness=0,
			horizontal_lines=border.BorderSide(1, "white"),
				columns=[
					DataColumn(Text("emp_id")),
					DataColumn(Text("Name")),
					DataColumn(Text("F/Name")),
					DataColumn(Text("Date of Birth")),
					DataColumn(Text("Date of ")),
					DataColumn(Text("Cnic ")),
					DataColumn(Text("Gender")),
					DataColumn(Text("Desig")),
					DataColumn(Text("Education")),
					DataColumn(Text("Contact")),
					DataColumn(Text("Email")),
					DataColumn(Text("Salary")),
					DataColumn(Text("Address")),
						],
						rows=[]

								)
		self.addnewDialog = AlertDialog(
			title=Text("Add new data",weight="bold"),
			content=Container(
				width=1000,
				content=Column([
				Row([
					self.full_name,
					self.first_name,
					self.employe_in_date
					],alignment="spaceBetween"),
				Row([
					self.employe_out_date,
					self.cnic,
					self.gender
					],alignment="spaceBetween"),
				Row([
					self.design,
					self.education,
					self.contact
					],alignment="spaceBetween"),
				Row([
					self.email,
					self.salary,
					self.address
					],alignment="spaceBetween")
				])
				),
			actions=[
			ElevatedButton("Add new",
				on_click=lambda e:self.addnewdata(e)
				)
			],
			actions_alignment="end"
			)

		self.detailDialogOpen = AlertDialog(
			shape=CountinuosRectangleBorder(),
			title=Container(
				bgcolor="blue",
				padding=10,
				content=Text("Details Data",weight="bold",color="white")
				),
			content=Container(
				bgcolor="yellow200",
				width=1000,
				padding=10,
				content=Column([
						Row([
							Text(f"Emp ID :",size=25,weight="bold"),
						self.emp_id
						]),
						Divider(),
						Row([
							self.full_name,
							self.first_name,
							self.employe_in_date
							],alignment="spaceBetween"),
						Row([
							self.employe_out_date,
							self.cnic,
							self.gender
							],alignment="spaceBetween"),
						Row([
							self.design,
							self.education,
							self.contact
							],alignment="spaceBetween"),
						Row([
							self.email,
							self.salary,
							self.address
							],alignment="spaceBetween")
						])
						),
				actions=[
					IconButton("delete",bgcolor="red",
						icon_size=60,icon_color="white",
						on_click=self.deletetabledata
						),
					ElevatedButton("Save and Close",
						bgcolor="blue",color="white",
						on_click=self.updatedatatable
						)
					
					],
					actions_alignment="spaceEvenly"
					)
			
	

	def build(self):

		return Column([
				Row([
				Text("Employee System",weight="bold",size=25),
				Text(f"Date : {self.now.strftime('%d-%m-%Y')}",
					size=25
					),
				ElevatedButton("Logout",icon="logout",
					bgcolor="red",color="white",
					on_click=self.logoutbtn
					)
				],alignment="spaceBetween"),
					
				Container(
					border_radius=30,
					padding=20,
				bgcolor="blue200",
				content=Column([
					Row([
					Text("Search",size=25,weight="bold"),
					self.searchtable,
					ElevatedButton("Add New Data",
						bgcolor="yellow",
						color="black",
						icon="add",
						on_click=self.opennewdata
						)
					]),
					Column([
						Row([self.mytable],scroll="always")
						],scroll="always")
					])
					)				

				])

	def logoutbtn(self,e):
		self.page.session.clear()
		self.page.go("/")
		self.page.update()
	def carinama(self,e):
		prefix = self.searchtable.value
		try:
			cursor.execute(f"SELECT * FROM tblemployee WHERE full_name LIKE '{prefix}%'")
			rows = cursor.fetchall()
			self.mytable.rows.clear()
			columns = [description[0] for description in cursor.description]
			for row in rows:
				x = dict(zip(columns, row))
				self.mytable.rows.append(
					DataRow(
						on_select_changed=lambda e:self.onclicktable(e),
						cells=[
							DataCell(Text(x['emp_id'])),
							DataCell(Text(x['full_name'])),
							DataCell(Text(x['first_name'])),
							DataCell(Text(x['tgl_masuk_kerja'])),
							DataCell(Text(x['tgl_keluar_kerja'])),
							DataCell(Text(x['cnic'])),
							DataCell(Text(x['gender'])),
							DataCell(Text(x['desig'])),
							DataCell(Text(x['high_edu'])),
							DataCell(Text(x['contact'])),
							DataCell(Text(x['email'])),
							DataCell(Text(x['salary'])),
							DataCell(Text(x['address'])),
							]
						)
					)
				self.update()

		except Exception as e:
			print(e)
			print("Error occurred while searching data!")


	def deletetabledata(self,e):
		try:
			cursor.execute("DELETE FROM tblemployee WHERE emp_id = ?", (self.emp_id.value,))
			conn.commit()
			print(cursor.rowcount, "record(s) deleted.")
			self.detailDialogOpen.open = False
			self.page.snack_bar = SnackBar(
            Text("Data Success Deleted",size=30),
            bgcolor="red"
            )
			self.page.snack_bar.open = True
			self.mytable.rows.clear()
			self.loadfromdatabase()
			self.page.update()
		except Exception as e:
			print(e)
			print("Error: failed to delete record.")

	def updatedatatable(self,e):
		try:
			emp_id = self.emp_id.value
			full_name = self.full_name.value
			first_name = self.first_name.value
			employe_in_date = self.employe_in_date.value
			employe_out_date = self.employe_out_date.value
			cnic = self.cnic.value
			gender = self.gender.value
			design = self.design.value
			education = self.education.value
			contact = self.contact.value
			email = self.email.value
			salary = self.salary.value
			address = self.address.value
			sql = """UPDATE tblemployee SET full_name=?, first_name=?, tgl_masuk_kerja=?, 
                tgl_keluar_kerja=?, cnic=?, gender=?, desig=?, high_edu=?, contact=?, 
                email=?, salary=?, address=? WHERE emp_id=?"""
     
			val = (full_name, first_name, employe_in_date, employe_out_date, cnic, gender, 
               design, education, contact, email, salary, address, emp_id)
			cursor.execute(sql, val)
			conn.commit()
			print(cursor.rowcount, "record updated successfully.")
			self.mytable.rows.clear()
			self.loadfromdatabase()
			self.detailDialogOpen.open = False
			self.page.snack_bar = SnackBar(
            Text("Data Success Edited",size=30),
            bgcolor="green"
            )
			self.page.snack_bar.open = True
			self.page.update()
		except Exception as e:
			print(e)
			print("Error: could not update data. Please check log.")



	def did_mount(self):
		self.mytable.rows.clear()
		self.loadfromdatabase()

	def loadfromdatabase(self):
		try:
			cursor.execute("SELECT * FROM tblemployee")
			rows = cursor.fetchall()
			print(rows)
			result = []
			columns = [description[0] for description in cursor.description]
			for row in rows:
				x = dict(zip(columns, row))
				self.mytable.rows.append(
					DataRow(
						on_select_changed=lambda e:self.onclicktable(e),
						cells=[
							DataCell(Text(x['emp_id'])),
							DataCell(Text(x['full_name'])),
							DataCell(Text(x['first_name'])),
							DataCell(Text(x['tgl_masuk_kerja'])),
							DataCell(Text(x['tgl_keluar_kerja'])),
							DataCell(Text(x['cnic'])),
							DataCell(Text(x['gender'])),
							DataCell(Text(x['desig'])),
							DataCell(Text(x['high_edu'])),
							DataCell(Text(x['contact'])),
							DataCell(Text(x['email'])),
							DataCell(Text(x['salary'])),
							DataCell(Text(x['address'])),
							]
						)
					)
				self.update()
		except Exception as e:
			print(e)
			print("Error CHECK LOG !!!")
		  
	def onclicktable(self,e):
		print("jalan")

		self.emp_id.value  = e.control.cells[0].content.value
		print(self.emp_id.value)
		self.full_name.value  = e.control.cells[1].content.value
		self.first_name.value  = e.control.cells[2].content.value
		self.employe_in_date.value = e.control.cells[3].content.value
		self.employe_out_date.value  = e.control.cells[4].content.value
		self.cnic.value  = e.control.cells[5].content.value
		self.gender.value  = e.control.cells[6].content.value
		self.design.value  = e.control.cells[7].content.value
		self.education.value  = e.control.cells[8].content.value
		self.contact.value  = e.control.cells[9].content.value
		self.email.value  = e.control.cells[10].content.value
		self.salary.value  = e.control.cells[11].content.value
		self.address.value  = e.control.cells[12].content.value
		
		self.update()
		self.page.dialog = self.detailDialogOpen
		self.detailDialogOpen.open = True
		self.page.update()

		

	def opennewdata(self,e):
			self.emp_id.value  = ""
			self.full_name.value  = ""
			self.first_name.value  = ""
			self.employe_in_date.value = ""
			self.employe_out_date.value  = ""
			self.cnic.value  = ""
			self.gender.value  = ""
			self.design.value  = ""
			self.education.value  = ""
			self.contact.value  = ""
			self.email.value  =  ""
			self.salary.value  =  ""
			self.address.value  =  ""
			self.update()
			self.page.dialog = self.addnewDialog
			self.addnewDialog.open = True
			self.page.update()
	def addnewdata(self,e):
		try:
			sql = "INSERT INTO tblemployee (full_name, first_name, tgl_masuk_kerja, tgl_keluar_kerja, cnic, gender, desig, high_edu, contact, email, salary, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
			val = (self.full_name.value, self.first_name.value, self.employe_in_date.value, self.employe_out_date.value, self.cnic.value, self.gender.value, self.design.value, self.education.value, self.contact.value, self.email.value, int(self.salary.value), self.address.value)
			cursor.execute(sql, val)
			conn.commit()
			print(cursor.rowcount, "record inserted.EMPLOYEe !!!")
			self.mytable.rows.clear()
			self.loadfromdatabase()
			self.addnewDialog.open = False
			self.page.snack_bar = SnackBar(
            Text("Data Success added",size=30),
            bgcolor="green"
            )
			self.page.snack_bar.open = True
			self.full_name.value = ""
			self.first_name.value = ""
			self.employe_in_date.value = ""
			self.employe_out_date.value = ""
			self.cnic.value = ""
			self.gender.value = ""
			self.design.value = ""
			self.education.value = ""
			self.contact.value = ""
			self.email.value = ""
			self.salary.value = ""
			self.address.value = ""
			self.page.update()
		except Exception as e:
			print(e)
			print("CHECK ERROR !!!")



def main(page:Page):
	widthsrc = page.window_width

	mylogin = MyLogin(width=widthsrc)
	employee = EmployePage()
	page.scroll = "always"

	page.vertical_alignment="center"
	page.horizontal_alignment="center"
	

	def route_change(route):
		page.views.clear()
		page.scroll="always"
		page.views.append(
            View(
                "/",
                [
                mylogin
                ],
            )
	        )
		if page.route == "/employee":
			if page.session.get("login") == None:
				page.go("/")
			else:
				page.views.append(
	                View(
	                    "/employee",
	                    [
	                    employee
	                    
	                    ],
	                )
	            	)
		page.update()

	

	page.on_route_change = route_change
	page.go(page.route)


flet.app(target=main,port=8550)
