

def login_required(func, request):
    if request.user != None:
        return func