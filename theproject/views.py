#superuser = user: rafid    pass: 123456
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import auth,messages
import pyrebase
from .models import client
import datetime

#pyrebase sdk
config = {
    'apiKey': "AIzaSyDr4jO2Gp7j0hsx5VLHDtdObBZp7XemTOs",
    'authDomain': "project-d4bf4.firebaseapp.com",
    'databaseURL': "https://project-d4bf4-default-rtdb.firebaseio.com",
    'projectId': "project-d4bf4",
    'storageBucket': "project-d4bf4.appspot.com",
    'messagingSenderId': "145308609557",
    'appId': "1:145308609557:web:f01d105775ec058187721c",
    'measurementId': "G-7BENWP5SS7" }

firebase = pyrebase.initialize_app(config)

db = firebase.database()
pyreauth = firebase.auth()
pyrestorage = firebase.storage()

#Returns loginpage
def loginpage(request):
    return render(request, 'login/index.html')

#Returns homepage
def homepage(request, message):
    userobj = request.session.get('uid')
    name = db.child("user").child(userobj).child("name").child("name").get()
    print(name.val())
    array = arrayfile(userobj)
    request.session['roles'] = array
    rolelist = request.session.get('roles')
    print(rolelist)
    avpath = "avatar/"+ userobj +".jpg" 
    avpath = pyrestorage.child(avpath).get_url(None)
    print(userobj)
    #print(avpath)
    return render(request, 'dashboard/sidebar.html', {"msg": message ,"lid": userobj,"dp": avpath,"nam": name.val(), "roles": rolelist })

#login function
def firebaseLoginAuth(request):
    if request.method =='POST':
        mail = request.POST['email']
        password = request.POST['passw']
        x = db.child("admin").child("password").get()
        if mail == 'admin':
            if x.val() == password:
                print ("succuss")
                return adminhome(request)
            else:
                message="invalid email or password"
                return render(request, 'demo2.html')
                #return render(request, 'login/index.html', {"msg": message}) 
        else:
            try:
                userobject = pyreauth.sign_in_with_email_and_password(mail,password)
                #localID set and print
                sid = userobject['localId']
                request.session['uid'] = sid
                sid = request.session.get('uid')
                print(sid)    
                #roles set and print
                return homepage(request, "successfully logged in")
            except:
                message="invalid email or password"
                return render(request, 'login/index.html', {"msg": message})
    else: 
        return homepage(request, "")

#logout function
def logout(request):
    auth.logout(request)
    return loginpage(request)

#Google Sign in works
def GoogleSignin(request):
    userobj = request.POST['uid']
    print(userobj)
    request.session['uid'] = userobj
    return homepage (request, "Google Sign in success")

#fetch publicfile data list
def publicfiles (request):
    userobj = request.session.get('uid')
    filenamearr = []
    filelinkarr = []
    timearr = []
    uploaderarr = []
    uploadername = [] 
    x = db.child("files").child("public").get()
    print(x.each())
    for user in x.each():
        # dummy data must be skipped that's why if condition
        if (user.val() != 0):
            print (user.key())
            y = db.child("files").child("public").child(user.key()).get()
            userlist = []
            for docs in y.each():
                userlist.append(docs.key())
                userlist.append(docs.val())
            
            filenamearr.append(userlist[0])
            filelinkarr.append(pyrestorage.child(userlist[1]).get_url(None))
            timearr.append(userlist[3])
            uploaderarr.append(userlist[5])
    for user in uploaderarr:
        xyz = db.child("user").child(user).child("name").child("name").get()
        uploadername.append(xyz.val())
    print(uploadername)
    print(userlist)
    print(filenamearr)
    print(filelinkarr)
    print(timearr)
    print(uploaderarr)
    print(type(filenamearr))
    zipped = zip(filenamearr, timearr, uploadername, filelinkarr)
    return render(request, 'dashboard/public/datatabledash.html', 
    {'uploaderid': uploaderarr, 'thiszip': zipped })

#fetch privatefiles in data list
def privatefiles (request):
    userobj = request.session.get('uid')
    filenamearr = []
    filelinkarr = []
    timearr = []
    uploaderarr = []
    uploadername = [] 
    x = db.child("files").child("private").get()
    for user in x.each():
        # dummy data must be skipped that's why if condition
        if (user.val() != 0):
            y = db.child("files").child("private").child(user.key()).get()
            userlist = []
            checker = db.child("files").child("private").child(user.key()).child("uid").get()
            print(checker.val())
            if (checker.val() == userobj):
                for docs in y.each():
                    print(docs.val())
                    userlist.append(docs.key())
                    userlist.append(docs.val())
                
                filenamearr.append(userlist[0])
                filelinkarr.append(pyrestorage.child(userlist[1]).get_url(None))
                timearr.append(userlist[3])
                uploaderarr.append(userlist[5])
    for user in uploaderarr:
        xyz = db.child("user").child(user).child("name").child("name").get()
        uploadername.append(xyz.val())
    #print(uploadername)
    #print(userlist)
    #print(filenamearr)
    #print(filelinkarr)
    #print(timearr)
    #print(uploaderarr)
    #print(type(filenamearr))
    zipped = zip(filenamearr, timearr, uploadername, filelinkarr)
    return render(request, 'dashboard/private/private.html', 
    {'uploaderid': uploaderarr, 'thiszip': zipped })

def uploadfile(request):
    roletype = request.POST['filetype']
    filelink = request.FILES['doc']
    filename = request.POST['filename']
    userobj = request.session.get('uid')
    print(roletype)
    print(filename)
    if (roletype == "public" or roletype == "private"):
        try:
            x = roletype + '/' + userobj + '/' + filename 
            y = pyrestorage.child(x).put(filelink)
            c = str(datetime.datetime.now())
            # file directory in storage for z
            z = {filename : y['name'],
                "timestamp" : c,
                "uid" : userobj
                }
            db.child("files").child(roletype).push(z)
            print(y)
            #url to view file online
            #y = (pyrestorage.child(x).get_url(userobj))
            print(y)
            return homepage(request, "File upload success!")
        except:
            return homepage(request, "Error try again") 
    elif (roletype == "none"):
        return homepage(request, "Please select a role")
    else:
        try:
            x = "role" + '/' + roletype + '/' + filename
            y = pyrestorage.child(x).put(filelink)
            print(y)
            c = str(datetime.datetime.now())
            z = {filename : y['name'],
                "timestamp" : c,
                "uid" : userobj
                }
             # file directory in storage for z
            db.child("files").child(roletype).push(z)
            #url to view file online
            #y = (pyrestorage.child(x).get_url(userobj))
            print(y)
            return homepage(request, "File upload success!")
        except:
            return homepage(request, "Error try again") 

#ADMIN SECTION START

def adminhome (request):
    x = db.child("user").get()
    y = db.child("role").get()
    users = 0
    roles = 0
    sidarr = []
    rolearr = []
    for user in x.each():
        print(user.key()) 
        users = users + 1
        sidarr.append(user.key())
    for role in y.each():
        print (role.key())
        roles = roles + 1
        rolearr.append(role.key())
    request.session['sidlist'] = sidarr
    request.session['rolelist'] = rolearr
    message = request.session.get('message')
    return render(request, 'Admin template/admindashboard.html', {'usercount':users , 'rolecount': roles, 'msg': message})

def editrole (request):
    namearr = getalluser()
    request.session['namelist'] = namearr
    sidarr = request.session.get('sidlist')
    rolearr = request.session.get('rolelist')
    try:
        message = request.session.get('message')
    except:
        message = ""
    
    return render (request, 'Admin template/editUserRoles.html', {'namelist': namearr, 'rolelist': rolearr, 'msg': message })

def postedit (request):
    try:
        if request.method == "POST":
            name = request.POST['username']
            role = request.POST['role']
            print(name)
            print(role)
            namearr = getalluser()
            sidarr = request.session.get('sidlist')
            index = 0
            flag = False
            for x in namearr:
                if name == x:
                    flag = True
                    break
                else:
                    index += 1
            print(flag)
            if flag == True:
                sid = sidarr[index]
                rolelist = db.child("user").child(sid).child("role").get() 
                print("Here 3")
                flag1 = False
                for y in rolelist.each():
                    if y.val() == True:
                        if y.key() == role:
                            flag1 = True
                            break
                        else:
                            flag1 = False
                            continue
                    else: 
                        if y.key() == role:
                            flag1 = False
                            break
                        else:
                            flag1 = True
                            continue
                if flag1 == True:
                    request.session['message'] = "User already has this role, Try again!"
                    return editrole(request)
                else:
                    print("Here 2")
                    db.child("user").child(sid).child("role").update({role:True})
                    db.child("role").child(role).update({sid:True})
                    request.session['message'] = "SUCCESS!"
                    return editrole(request)
            else:
                request.session['message'] = "Error updating, Try again!"
                return editrole(request)
    except:
        request.session['message'] = "JHAMELA!"
        return editrole(request)


def deleteacc (request):
    namearr = getalluser()
    request.session['namelist'] = namearr
    try:
        message = request.session.get('message')
    except:
        message = ""
    return render (request, 'Admin template/deleteExistingAcc.html', {'namelist': namearr, 'msg': message })

def postdelete (request):
    accname = request.POST['username']
    passw = request.POST['password']
    x = db.child("admin").child("password").get()
    if x.val() != passw:
        request.session['message'] = "Incorrect admin password! Try again"
        return deleteacc(request)
    else:
        namearr = getalluser()
        sidarr = request.session.get('sidlist')
        index = 0
        flag = False
        for x in namearr:
            if accname == x:
                flag = True
                break
            else:
                index += 1
        print(flag)
        if flag == True:
            sid = sidarr[index]
            db.child("user").child(sid).remove()
            delete1 = db.child("role").get()
            for z in delete1.each():
                delete2 = db.child("role").child(z.key()).get()
                for zx in delete2.each():
                    if zx.key() == sid:
                        db.child("role").child(z.key()).child(zx.key()).remove()
                
            request.session['message'] = "ACCOUNT DELETION SUCCESS!"
            return deleteacc(request)    
        else:
            request.session['message'] = "Error Deleting Account! Try again"
            return deleteacc(request)

def newacc(request):
    rolearr = request.session.get('rolelist')
    try:
        message = request.session.get('message')
    except:
        message = ""
    return render(request, 'Admin template/createNewAcc.html', {'rolelist': rolearr, 'msg': message})

def postnewacc(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        filelink = request.FILES['doc']
        passw = request.POST['password1']
        passw2 = request.POST['password2']
        role = request.POST['role']

        if passw != passw2:
           request.session['message'] = "Passwords didn't Match! Try again"
           return newacc(request)
        else:
            try:
                userobj = pyreauth.create_user_with_email_and_password(email, passw)
                sid = userobj['localId']
                print(sid)
                x = "avatar/"+sid+".jpg"
                y = pyrestorage.child(x).put(filelink)
                print(y)
                db.child("role").child(role).update({sid:True})
                db.child("user").child(sid).child("name").update({"name":name})
                db.child("user").child(sid).child("role").update({role:True})

                request.session['message'] = "Account Creation Success!"
                return newacc(request)
            except:
                request.session['message'] = "Account Creation Failure. TRY AGAIN!"
                return newacc(request)

    else:
        request.session['message'] = "ERROR!" 
        return newacc (request)

def newrole(request):
    namearr = getalluser()
    try:
        message = request.session.get('message')
    except:
        message = ""
    return render(request, 'Admin template/createNewRole.html', {'namelist': namearr, 'msg':message })

def newrolepost(request):
    if request.method == "POST":    
        username = request.POST['name12']
        role = request.POST['role']
        print(username)
        print(role)
        namearr = getalluser()
        sidarr = request.session.get('sidlist')
        index = 0
        flag = False
        for x in namearr:
            if username == x:
                flag = True
                break
            else:
                index += 1
        print(flag)
        if flag == True:
            sid = sidarr[index]
        print(sid)
        db.child("role").child(role).update({sid: True})
        db.child("user").child(sid).child("role").update({role:True})
        request.session['message'] = "Successfully created role"
        return newrole(request)
    else:
        request.session['message'] = "ERROR!"
        return newrole(request)

def adminpass(request):
    if request.method == "POST":
        oldpass = request.POST['oldpass']
        newpass = request.POST['newpass']
        x = db.child("admin").child("password").get()
        if x.val() == oldpass:
            db.child("admin").update({"password": newpass})
            request.session['message'] = "Successfully changed!"
            return adminhome(request)
        else:
            request.session['message'] = "Incorrect Old Password! Try again"
            return adminhome(request)
    else:
        request.session['message'] = "ERROR!"
        return adminhome(request)

#ADMIN SECTION END

#fetch all user list
def getalluser():
    namearray = []
    x = db.child("user").get()
    for users in x.each():
        print (users.key())
        y = db.child("user").child(users.key()).child("name").get()
        for nam in y.each():
            if nam.key() == "name":
                namearray.append(nam.val())
    print(namearray)
    return namearray

#fetching array file for roles
def arrayfile(lid):
    role = db.child('user').child(lid).child('role').get()
    rolearr = []
    for role in role.each():
        if role.val() == True:
            rolearr.append(role.key())
    return rolearr
