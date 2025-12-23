from django.shortcuts import render
from django.contrib import messages
from Users.models import UserRegisterModel

#============================================================================================
def AdminLogin(request):
    if request.method == 'POST':
        username =    request.POST.get('username')
        password =    request.POST.get('password')
        print(username , password)
        try:
            if username=='admin' and password=='admin':
                return render(request, 'admins/AdminHome.html')
            else:
                messages.warning(request  , 'Invalid credentials')
                return render(request, 'Adminlgoin.html')
        except Exception as e:
            messages.warning(request  , f'{e} ')
    return render(request, 'Adminlgoin.html')
#============================================================================================

def AdminHome(request):
    return render(request, 'admins/AdminHome.html')

#============================================================================================
def viewusers(request):
    data= UserRegisterModel.objects.all()
    return render(request, 'admins/Viewregisterusers.html', {'data':data})

#============================================================================================
def Activateusers(request):
    if request.method == 'GET':
        uid = request.GET.get('id')
        status ='Activate'
        UserRegisterModel.objects.filter(id=uid).update(status=status)
        data= UserRegisterModel.objects.all()
    return render(request, 'admins/Viewregisterusers.html' , {'data':data})

#============================================================================================
def Deactivateusers(request):
    if request.method == 'GET':
        uid = request.GET.get('id')
        status ='waiting'
        UserRegisterModel.objects.filter(id=uid).update(status=status)
        data= UserRegisterModel.objects.all()
    return render(request, 'admins/Viewregisterusers.html' , {'data':data})


#============================================================================================

def Deleteusers(request):
    if request.method == 'GET':
        uid = request.GET.get('id')
        UserRegisterModel.objects.get(id=uid).delete()
        data= UserRegisterModel.objects.all()
    return render(request, 'admins/Viewregisterusers.html' , {'data':data})