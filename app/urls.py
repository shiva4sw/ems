from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter
from .views import ExamViewSet

router = DefaultRouter()
router.register(r'exams', ExamViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('faculty/', faculty, name='faculty'),
    path('student/', student, name='student'),
    path('fac_dashboard', fac_dashboard, name='fac_dashboard'),
    path('logout/', logout, name='logout'),
    path('api/',include(router.urls)),
    path('fac_exam/', fac_exam, name='fac_exam'),
    path('sd/', student_dashboard, name='sd'),
    path('exam/<int:eid>/', stud_exam, name='stud_exam'),
    path('resu/<int:eid>/', stud_res, name='stud_res'),
]