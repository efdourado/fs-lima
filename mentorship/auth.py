from .models import Mentee

def validate_token(token):
    return Mentee.objects.filter(token=token).first()