# Using sessions in Flask

Login and logout routes have been added to the app in the auth module.

These do not currently manage login and lgout, all they do is set and delete the session cookie so that you can see how sessions work.

1. Start the Flask app

2. Open Chrome 
    - Open the developer tools
    - Select the Application tab along the top of the toolbar
    - Select Cookies from the sidebar on the left

3. Login
    - Go to http://localhost:5000/login/ in Chrome.
    - Enter any email address and password and submit the form. 
    - The index page should show the email address you just entered on the login form.
    - You should see the session in the Cookies section of the Developer Tools pane in Chrome.

4. Logout
    - enter http://localhost:5000/logout/
    

**Note**: You are unlikely to need to create sessions explicitly in the coursework. 

The code that you just used will be replaced in the next activity when we use Flask-Login. 

Flask-Login uses sessions however it creates and manages these for you.
