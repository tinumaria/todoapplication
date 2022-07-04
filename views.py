from Basic_django.Todo.models import users,todos

def authenticate(*args,**kwargs):
    username=kwargs.get("username")
    password=kwargs.get("password")
    user_data=[user for user in users if user["username"]==username and user["password"]==password]
    return user_data

session={}

def loginrequired(fn):
    def wrapper(*args,**kwargs):
        if "user" in session:
            return fn(*args,**kwargs)
        else:
            print("u must login")
    return wrapper

class Login:
    def post(self,*args,**kwargs):
        username=kwargs.get("username")
        password=kwargs.get("password")
        user_login=authenticate(username=username,password=password)
        if user_login:
            session["user"]=user_login[0]
            print("login success")
        else:
            print("invalid credentials")

class Alltodo:
    @loginrequired
    def get(self,*args,**kwargs):
        return todos

class Createtodo:
    @loginrequired
    def post(self,*args,**kwargs):
        userId=session["user"]["id"]
        kwargs["userId"]=userId
        print(kwargs)
        todos.append(kwargs)
        print(todos)

class Mytodo:
    @loginrequired
    def get(self,*args,**kwargs):
        userId=session["user"]["id"]
        my_todo=[todo for todo in todos if todo["userId"]==userId]
        return my_todo

class TodoDetails:
    def get_object(self,todoid):
        todo_details=[todo for todo in todos if todo["todoId"]==todoid]
        return todo_details

    @loginrequired
    def get(self,*args,**kwargs):
        todo_id=kwargs.get("todoId")
        todo_spec=self.get_object(todo_id)
        return todo_spec

    @loginrequired
    def put(self,*args,**kwargs):
        todo_id=kwargs.get("todo_id")
        data=kwargs.get("data")
        todo_update_data=self.get_object(todo_id)
        if todo_update_data:
            todo_update=todo_update_data[0]
            todo_update.update(data)
            return todo_update

    @loginrequired
    def delete(self,*args,**kwargs):
        todo_id=kwargs.get("todo_id")
        todo_delete_data=self.get_object(todo_id)
        if todo_delete_data:
            todo_delete=todo_delete_data[0]
            todos.remove(todo_delete)
            print("todo removed")
            print(len(todos))

def logout(*args,**kwargs):
    session.pop("user")
    print("user has been logged out")


login=Login()
login.post(username="richard", password="Password@123")
print(session)

alltodo=Alltodo()
print(alltodo.get())

createtodo=Createtodo()
createtodo.post(todoId=9,
                task_name="ibill",
                completed="true"
                )

mytodo=Mytodo()
print(mytodo.get())

todo_details=TodoDetails()
print(todo_details.get(todoId=5))

data={
    "task_name":"zbill",
    "completed":"false"
}

print(todo_details.put(todoId=3,data=data))

todo_details.delete(todoId=4)

logout()
print(session)




