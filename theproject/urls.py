from django.urls import path
from . import views

urlpatterns = [
    path ('', views.loginpage),
    path ('home', views.firebaseLoginAuth, name = "Dashboard"),
    path ('public', views.publicfiles, name = "public"),
    path ('private', views.privatefiles, name = "private"),
    path ('uploadfile/', views.uploadfile, name = "upload"),
    path ('logout/', views.logout, name = "logout"),
    path ('gsignin/', views.GoogleSignin, name = "Gsign"),
    path ('adminhome/', views.adminhome, name = "adminhome"),
    path ('adminpass/', views.adminpass, name = "adminpass"),
    path ('adminnewacc/', views.newacc, name = "newacc"),
    path ('adminnewaccpost/', views.postnewacc, name = "newaccpost"),
    path ('adminrole/', views.newrole, name = "newrole"),
    path ('adminrolepost/', views.newrolepost, name = "newrolepost"),
    path ('adminroleedit/', views.editrole, name = "editrole"),
    path ('adminroleeditpost/', views.postedit, name = "postedit"),
    path ('admindelete/', views.deleteacc, name = "deleteacc"),
    path ('admindeletepost/', views.postdelete, name = "postdelete"),
    
    #path ('home/', views.hompage),
]
