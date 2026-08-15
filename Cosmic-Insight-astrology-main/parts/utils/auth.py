import random
from django.shortcuts import render
def Signup(request):
    if request.method == "POST":
        print("In POST Method")
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        if signup.objects.filter(mobile=mobile):
            return render(request,'Signup.html',context={"error":"Mobile number registered already"})

        if password!=confirmPassword:
            return render(request,'Signup.html',context={"error":"Password Miss Match !"})

        otp = random.randint(100000,999999)
        request.session['otp'] = otp
        request.session['mobile'] = mobile
        request.session['name'] = name
        request.session['password'] = password

        print(f"Genrated otp for {mobile}:{otp}")
        return redirect('otp')
    print("Getting GET Method")
    return render(request,'Signup.html')
def otp(request):
    sessionOTP = request.session.get('otp')
    if request.method == 'POST':
        otp1 = request.POST.get('otp1')
        otp2 = request.POST.get('otp2')
        otp3= request.POST.get('otp3')
        otp4 = request.POST.get('otp4')
        otp5 = request.POST.get('otp5')
        otp6 = request.POST.get('otp6')
        final = otp1 + otp2 + otp3 + otp4 + otp5 + otp6
        if sessionOTP == int(final):
            return redirect('login')
        else:
            return HttpResponse("<h1> Unsuccessful otp Verify")
    return render(request,'otp.html')

#
def Login(request):
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        print(mobile, password)

        try:
            user = signup.objects.get(mobile=mobile)
            print(user)

            if user.password == password:
                # Set session for authentication
                request.session['user_mobile'] = mobile
                request.session['is_authenticated'] = True
                request.session['is_admin'] = user.is_admine

                # Save login record
                DateTime = datetime.datetime.now()
                login_record = login(mobile=mobile, datetime=DateTime)
                login_record.save()

                print("Login successful")

                if user.is_admine:
                    print("Admin")
                    return redirect('showdata')
                else:
                    print("Home")
                    return redirect('home')
            else:
                print("Invalid password")
                return render(request, 'login.html', {'error': 'Invalid password'})

        except signup.DoesNotExist:
            print("User not found")
            return render(request, 'login.html', {'error': 'User not found'})

    return render(request, 'login.html')
def showdata(request):
    obj = login.objects.all()
    return render(request,'tables.html',context={'data':obj})

def edit(request,id):
    obj = login.objects.get(id=id)
    if request.method == 'POST':
        obj.id = request.POST.get('id')
        obj.mobile = request.POST.get('mobile')
        obj.DateTime = datetime.datetime.now()
        obj.save()
        return redirect('viewdata')
    return render(request,'edit.html',context={'data':obj})

def delete(request,id):
    if request.method == 'POST':
        id = request.POST.get('id')
        mobile = request.POST.get('mobile')
        DateTime = request.POST.get('DateTime')
        obj = login(id=id,mobile=mobile,DateTime=DateTime)
        obj.save()
        return render(request,'delete.html')
