Login and logout routes have been added to the app, these simply set and delete the session cookie (i.e. no database interaction)
Start the Flask app
Open Chrome:
Open the developer tools
Select the Application tab along the top of the toolbar
Select Cookies from the sidebar on the left
Go to http://localhost:5000/login/. Enter any email address and password and submit. The index page should show the email address you entered on the login form.
You should see the session 
http://localhost:5000/logout/. The index page should no longer show an email address.
