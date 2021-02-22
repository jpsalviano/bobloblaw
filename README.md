# BobLobLaw
### 22/02/2021
#### First: Back-end
- start a Django app
- use Django's user authentication system
- Endpoint: create user/sign up
	- receives a request with user, password and email
	- responds created status
- Endpoint: log user/sign in
	- receives a user and password
	- responds with a token and ok status

#### Front-end
- React setup
- Create new user view
	- password, password and user form
	- send form to endpoint
- Login view
	- user and password form
	- sends form to endpoint
	- redirect to logged in view (if token is valid)
