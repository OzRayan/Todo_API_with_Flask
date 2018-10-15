# Todo_API_with_Flask

# Requirements

This API is versioned, all routes should be prefixed with /api/v1
When the app first starts it will attempt to fetch all Todos in the system. 
Handle the request and return all the Todos.
Look at the browser tool to see what is being requested and how and create the appropriate route

When a Todo is created and the save link is clicked, 
it will make a request to the server. Handle the request by creating a Todo and setting the proper status code.
Look at the browser tool to see what is being requested and how and create the appropriate route

When a previously saved Todo is updated and the save link is clicked, 
it will make a request to the server. Handle the request by updating the existing Todo.
Look at the browser tool to see what is being requested and how and create the appropriate route.

When a previously saved Todo is deleted and the save link is clicked, 
it will make a request to the server. Handle the deletion and return a blank response and the proper status code.
Unit test the app.

## Starting

Create a virtualenv and install the project requirements, which are listed in
`requirements.txt`. The easiest way to do this is with `pip install -r
requirements.txt` while your virtualenv is activated.

## Routes

* /api/v1/user
* /api/v1/todos
* /api/v1/todos/<int:id>

## Notes

If no user exist in data base, in `app.py` the `try` block can be uncommented to create an user

