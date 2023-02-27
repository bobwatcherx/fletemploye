from flet import *
import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host="172.17.0.2",
  user="root",
  password="admin12345",
  database="dbfood"
)
mycursor = mydb.cursor()

class MyLogin(UserControl):
	"""docstring for MyLogin"""
	def __init__(self):
		super(MyLogin, self).__init__()
		self.username = TextField(label="username",
					bgcolor="white",

			)
		self.password = TextField(label="password",
					bgcolor="white",
					filled=True,
					border=InputBorder.UNDERLINE,
					 can_reveal_password=True,
					 password=True
			)
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
	def build(self):
		return Column([
		Container(
			border_radius=30,
			bgcolor="black",
			width=300,
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
				on_click=self.loginnow
					)

					],alignment="center"),
				Divider(),
				Row([
					ElevatedButton("Sign With Google",
					bgcolor="white",color="black",
					on_click=self.signwithgoogle
						)
					],alignment="center")

				])

				)

		])

	# CHECK USER IF EXISTS
	def check_user(username, password):
	    sql = "SELECT * FROM users WHERE username = %s AND password = %s"
	    val = (username, password)
	    mycursor.execute(sql, val)
	    myresult = mycursor.fetchall()
	    if mycursor.rowcount > 0:
	        return True
	    else:
	        return False

	def loginnow(self,e):
		username = self.username.value
		password = self.password.value
		login_with = "manual"

		if MyLogin.check_user(username, password):
			sql = "UPDATE users SET login_with = %s, time_login = NOW() WHERE username = %s"
			val = (login_with, username)
			mycursor.execute(sql, val)
			mydb.commit()
			print(mycursor.rowcount, "record(s) updated.")
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
			print(self.page.route)
			self.page.update()
		else:
			print("Invalid username or password.")
			self.page.snack_bar = SnackBar(
				Text("Invalid Login Guys!!",size=30),
				bgcolor="red"
				)
			self.page.snack_bar.open = True

		self.page.update()

	def forgotpassword(self,e):
		print("forgot")
	def signwithgoogle(self,e):
		print("google")

	def processregister(self,e):
		username = self.username.value
		password = self.password.value
		login_with = "manual"
		try:
			sql = "INSERT INTO users (username, password, login_with, time_login) VALUES (%s, %s, %s, NOW())"
			val = (username, password, login_with)
			mycursor.execute(sql, val)
			mydb.commit()
			print(mycursor.rowcount, "record inserted.")
			self.page.snack_bar = SnackBar(
				Text("Success Created Account",size=30),
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
		self.employe_in_date = TextField(label="employe in",
			hint_text="dd-mm-yy"
			)
		self.employe_out_date = TextField(
			label="employe out",
			hint_text="dd-mm-yy"
			)
		self.cnic = TextField(label="cnic")
		self.gender = RadioGroup(
			content=Column([
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




	def build(self):

		return ResponsiveRow([
			Column(col=12,controls=[
				Row([
				Text("Employee System",weight="bold",size=25),
				Text(f"Date : {self.now.strftime('%Y-%m-%d')}",
					size=25
					),
				Text(f"TIme : {self.now.strftime('%H:%M:%S')}",
					size=25
					),
				ElevatedButton("Logout",icon="logout",
					bgcolor="red",color="white"
					)
				],alignment="spaceBetween")
				]),	
			Column(col=4,
				scroll="always",
				controls=[
				Container(
				bgcolor="blue200",
				border_radius=30,
				padding=10,
				content=Column([
						Text("Employee Details",weight="bold",size=25),
				Row([
					Text("EMP_ID"),
					self.emp_id,
					ElevatedButton("search",
						bgcolor="blue",icon="search",
						color="white"
						)
					],alignment="spaceBetween"),
				Row([
					Text("Name"),
					self.full_name
					],alignment="spaceBetween"),
				Row([
					Text("F/Name"),
					self.first_name
					],alignment="spaceBetween"),
				Row([
					Text("D.O.B"),
					self.employe_in_date
					],alignment="spaceBetween"),
				Row([
					Text("D.O.J"),
					self.employe_out_date
					],alignment="spaceBetween"),
				Row([
					Text("CNIC"),
					self.cnic
					],alignment="spaceBetween"),
				Row([
					Text("Gender"),
					self.gender
					],alignment="spaceBetween"),
				Row([
					Text("Desig"),
					self.design
					],alignment="spaceBetween"),
				Row([
					Text("High Edu"),
					self.education
					],alignment="spaceBetween"),
				Row([
					Text("Contact"),
					self.contact
					],alignment="spaceBetween"),
				Row([
					Text("Email"),
					self.email
					],alignment="spaceBetween"),
				Row([
					Text("Salary"),
					self.salary
					],alignment="spaceBetween"),
				Row([
					Text("Address"),
					self.address
					],alignment="spaceBetween"),

						],scroll="always")
					)
				
				])


			])
		


def main(page:Page):
	mylogin = MyLogin()
	employee = EmployePage()


	page.vertical_alignment="center"
	page.horizontal_alignment="center"
	

	def route_change(route):
		page.views.clear()
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
				page.scroll = "auto"
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


flet.app(target=main)
