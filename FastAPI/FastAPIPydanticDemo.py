from fastapi import FastAPI, HTTPException
from enum import IntEnum
from typing import List,Optional
from pydantic import BaseModel, Field

api = FastAPI()

class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class TodoBase(BaseModel): #Fields in this are required fields, This is the Todo Base model without the id.
    todo_name: str = Field(..., min_length=3,max_length=512,description="Name of the Todo")
    todo_description: str = Field(..., description="Description of the Todo" )
    priority: Priority = Field(default=Priority.LOW, description="Priority of the Todo")

class TodoCreate(TodoBase): #Inheriting so that we dont use todobase directly. this is for better debuging and more professional code
    pass

class Todo(TodoBase): #Adds ID along with name,desc, priorty as its inheriting TodoBase
    todo_id: int = Field(...,description="Unique Identifier of the Todo")

class TodoUpdate(BaseModel):#Fields are optional as we dont have to update every field everytime, only update the ones we need.
    todo_name: Optional[str] = Field(None, min_length=3,max_length=512,description="Name of the Todo")
    todo_description: Optional[str] = Field(None, description="Description of the Todo" )
    priority: Optional[Priority] = Field(None, description="Priority of the Todo") 

all_todos: List[Todo] = [
    Todo(todo_id=1, todo_name='Buy groceries', todo_description='Purchase milk, bread, eggs, and vegetables', priority=Priority.MEDIUM),
    Todo(todo_id=2, todo_name='Call dentist', todo_description='Schedule a dental check-up',priority=Priority.LOW),
    Todo(todo_id=3, todo_name='Finish report', todo_description='Complete and submit the monthly progress report',priority=Priority.HIGH),
    Todo(todo_id=4, todo_name='Go for a walk', todo_description='Take a 30-minute walk in the evening',priority=Priority.MEDIUM),
    Todo(todo_id=5, todo_name='Read a book', todo_description='Read at least one chapter before bedtime',priority=Priority.LOW)
] #List of Todo class objects

@api.get('/')
def index():
    return {'message':'Hello World'}

# for example : localhost:9999/todos/2
@api.get('/todos/{todo_id}', response_model=Todo) #This means response will be of type todo class havign id name desc etc as Todo class inherits TodoBase also
def get_todo(todo_id: int): #the function will get this 'todo_id' value from the above {}.
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo Not Found") 

# for example : localhost:9999/todos?first_n=2 This is called a query parameter
@api.get('/todos',response_model=List[Todo]) #This means response will contain a List of todos(objects of class todo)
def get_todo(first_n: int=None): #the function will get this parameter value from filter like in example above
                                #also we have to specify type of 'first_n' as int , otherwise it will be read an a string
    if(first_n):
        return all_todos[:first_n] #Return the first n todos, like first 2 todos in above example.
    else:
        return all_todos

@api.post('/todos',response_model=Todo) #This is to create a new todo item
def create_todo(todo: TodoCreate): #Passing the details of new todo item except the id which is dynamically created below
    new_todo_id= max(todo.todo_id for todo in all_todos)+1 #creating new id by adding 1 to the last id

    new_todo =Todo(
        todo_id= new_todo_id,
        todo_name= todo.todo_name,
        todo_description= todo.todo_description,
        priority=todo.priority
    )
    all_todos.append(new_todo)
    return new_todo

@api.put('/todos/{todo_id}',response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id==todo_id:
            if updated_todo.todo_name is not None:
                todo.todo_name= updated_todo.todo_name
            if updated_todo.todo_description is not None:
                todo.todo_description=updated_todo.todo_description
            if updated_todo.priority is not None:
                todo.priority=updated_todo.priority

            
            return todo
    # return "Error ! Not Found" #Now this is a string so response will not be of type Todo, it will be of type string
    #So to avoid this we use HTTPX Exception

    raise HTTPException(status_code=404, detail="Todo Not Found") #So now this is not a return values , this is an exception
        #So, it need not be of response type todo.

@api.delete('/todos/{todo_id}',response_model=Todo)
def delete_todo(todo_id:int):
    for index,todo in enumerate(all_todos):
        if todo.todo_id==todo_id:
            deleted_todo=all_todos.pop(index)
            return deleted_todo
    # return "Error! Not Found" 
    raise HTTPException(status_code=404, detail="Todo Not Found") 