Add the parameters to login_user() for to enable the remember me feature of the login form
Login again and tick the remember me box. Close and re-open the browser, you should still be logged in.

In our login route try the following so that if the user closes and opens the browser within a minute they should be remembered:
```python
from datetime import timedelta

...

login_user(user, remember=form.remember_me.data, duration=timedelta(minutes=1))

```