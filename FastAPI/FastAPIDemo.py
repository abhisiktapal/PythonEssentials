from fastapi import FastAPI

api = FastAPI()

all_todos = [
    {'todo_id': 1, 'todo_name': 'Buy groceries', 'todo_description': 'Purchase milk, bread, eggs, and vegetables'},
    {'todo_id': 2, 'todo_name': 'Call dentist', 'todo_description': 'Schedule a dental check-up'},
    {'todo_id': 3, 'todo_name': 'Finish report', 'todo_description': 'Complete and submit the monthly progress report'},
    {'todo_id': 4, 'todo_name': 'Go for a walk', 'todo_description': 'Take a 30-minute walk in the evening'},
    {'todo_id': 5, 'todo_name': 'Read a book', 'todo_description': 'Read at least one chapter before bedtime'}
]

@api.get('/')
def index():
    return {'message':'Hello World'}

# for example : localhost:9999/todos/2
@api.get('/todos/{todo_id}') #{todo_id} is the path parameter
def get_todo(todo_id: int): #the function will get this 'todo_id' value from the above {}.
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            return {'result':todo}

# for example : localhost:9999/todos?first_n=2 This is called a query parameter
@api.get('/todos')
def get_todo(first_n: int=None): #the function will get this parameter value from filter like in example above
                                #also we have to specify type of 'first_n' as int , otherwise it will be read an a string
    if(first_n):
        return all_todos[:first_n] #Return the first n todos, like first 2 todos in above example.
    else:
        return all_todos

@api.post('/todos') #This is to create a new todo item
def create_todo(todo: dict): #Passing the details of new todo item except the id which is dynamically created below
    new_todo_id= max(todo['todo_id'] for todo in all_todos)+1 #creating new id by adding 1 to the last id

    new_todo ={
        'todo_id':new_todo_id,
        'todo_name': todo['todo_name'],
        'todo_description': todo['todo_description']
    }
    all_todos.append(new_todo)
    return new_todo

@api.put('/todos/{todo_id}')
def update_todo(todo_id: int, updated_todo: dict):
    for todo in all_todos:
        if todo['todo_id']==todo_id:
            todo['todo_name']= updated_todo['todo_name']
            todo['todo_description']=updated_todo['todo_description']
            return todo
    return "Error ! Not Found"

@api.delete('/todos/{todo_id}')
def delete_todo(todo_id:int):
    for index,todo in enumerate(all_todos):
        if todo['todo_id']==todo_id:
            deleted_todo=all_todos.pop(index)
            return deleted_todo
    return "Error! Not Found" 