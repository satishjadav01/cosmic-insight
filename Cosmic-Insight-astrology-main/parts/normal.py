from .order import genrate_otp,send_sms
from django.contrib.auth.hashers import check_password

class SignupNormal:

    def __init__(self,user_repo):
        self.user_repo = user_repo

    def register(self,name,mobile,password,confirmPassword):
        if self.user_repo.user_exists(mobile):
            return {"error":"Mobile already exists"}

        if password != confirmPassword:
            return {"error":"Password not match"}

        otp = genrate_otp()
        send_sms(mobile,otp)

        self.user_repo.create_user({
            "name":name,
            "mobile":mobile,
            "password":password,
            "confirmPassword":confirmPassword,
            "is_admine":False
        })

        return {"otp":otp,
                "mobile":mobile}


class LoginNormal:
    def __init__(self, user_repo, login_repo):
        self.user_repo = user_repo
        self.login_repo = login_repo

    def login(self, mobile):
        print("LOGIN METHOD CALLED")

        user = self.user_repo.get_user(mobile)
        print(f"USER FROM REPO: {user}")

        if user is None:
            print("USER NOT FOUND - Will create on first login")
            return {'mobile': mobile, 'id': None, 'new_user': True}

        print("LOGIN SUCCESS - Existing user")
        return user

    def save_login(self, mobile, login_time):
        print(f"SAVING LOGIN: {mobile} at {login_time}")
        return self.login_repo.create_login(mobile, login_time)