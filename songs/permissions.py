# songs/permissions.py
def user_can_upload(user):
    if not user.is_authenticated:
        return False
    if user.is_staff:
        return True
    # profile exists via signal
    try:
        return user.profile.can_upload
    except Exception:
        return False
