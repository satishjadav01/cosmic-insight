class UserRepository:
    """Repository for user-related database operations"""

    def get_user(self, mobile):
        """
        Get user by mobile number from login table
        Returns user dict if found, None otherwise
        """
        try:
            from .models import login

            print(f"[UserRepo] Looking up user: {mobile}")

            # Check if this mobile has logged in before
            user_login = login.objects.filter(mobile=mobile).first()

            if user_login:
                print(f"[UserRepo] User found - ID: {user_login.id}")
                return {
                    'mobile': mobile,
                    'id': user_login.id,
                    'created_at': user_login.datetime
                }

            print(f"[UserRepo] No user found for: {mobile}")
            return None

        except Exception as e:
            print(f"[UserRepo] ERROR: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_user_by_mobile(self, mobile):
        """
        Alias for get_user - for consistency
        """
        return self.get_user(mobile)

    def create_user(self, mobile):
        """
        Create placeholder for new user
        Actual creation happens in LoginRepository.create_login()
        """
        print(f"[UserRepo] Placeholder for new user: {mobile}")
        return {'mobile': mobile, 'id': None}

    def get_all_users(self):
        """
        Get all users
        """
        try:
            from .models import login
            users = login.objects.all()
            return [
                {
                    'mobile': user.mobile,
                    'id': user.id,
                    'created_at': user.datetime
                }
                for user in users
            ]
        except Exception as e:
            print(f"[UserRepo] ERROR getting all users: {e}")
            return []


class LoginRepository:
    """Repository for login-related database operations"""

    def create_login(self, mobile, login_time=None):
        """
        Create a new login record
        This creates the user on first login
        """
        try:
            from .models import login
            from django.utils import timezone

            print(f"[LoginRepo] Creating login record for: {mobile}")

            # Check if user already exists
            existing_user = login.objects.filter(mobile=mobile).first()

            if existing_user:
                print(f"[LoginRepo] User already exists - ID: {existing_user.id}")
                # User exists, just return the existing record
                return existing_user

            # Create new login record (first time user)
            login_record = login.objects.create(
                mobile=mobile
            )

            print(f"✓ [LoginRepo] Login record created successfully!")
            print(f"  - ID: {login_record.id}")
            print(f"  - Mobile: {login_record.mobile}")
            print(f"  - DateTime: {login_record.datetime}")

            return login_record

        except Exception as e:
            print(f"✗ [LoginRepo] ERROR: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_login_history(self, mobile, limit=10):
        """
        Get login history for a user
        """
        try:
            from .models import login

            # Since we're storing only one record per user,
            # return the single login record
            user_login = login.objects.filter(mobile=mobile).first()

            if user_login:
                return [{
                    'id': user_login.id,
                    'mobile': user_login.mobile,
                    'datetime': user_login.datetime
                }]

            return []

        except Exception as e:
            print(f"[LoginRepo] ERROR getting login history: {e}")
            return []

    def get_total_logins(self, mobile):
        """
        Get total number of logins for a user
        In this system, it's just 1 record per user
        """
        try:
            from .models import login
            count = login.objects.filter(mobile=mobile).count()
            return count
        except Exception as e:
            print(f"[LoginRepo] ERROR: {e}")
            return 0