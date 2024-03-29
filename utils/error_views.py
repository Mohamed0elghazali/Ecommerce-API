from django.http import JsonResponse

# don`t forget to make DEBUG = False and add localhost in ALLOWED_HOSTS
# DEBUG = False
# ALLOWED_HOSTS = ['localhost']

def handler404(request, exception):
    message = ("Path not found")
    response = JsonResponse(data={"error": message})
    response.status_code = 404
    return response

def handler500(request):
    message = ("Internal Server Error")
    response = JsonResponse(data={"error": message})
    response.status_code = 500
    return response