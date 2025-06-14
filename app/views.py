from django.shortcuts import render, redirect

# Create your views here.
def home(req):
    return render(req, 'index.html')

from .models import Faculty, Student
def faculty(req):
    if req.session.get('unm'):
        return redirect('fac_dashboard')
    fac = None
    if req.method=='POST':
        unm = req.POST.get('unm')
        pwd = req.POST.get('pwd')
        fac = Faculty.objects.filter(unm=unm, pwd=pwd)
        if fac:
            req.session['fid'] = fac.first().id
            req.session['name'] = fac.first().name 
            req.session['unm'] = unm
            req.session['type'] = 'faculty'
            return redirect('fac_dashboard')
        else:
            print('Wrong user name')
    return render(req, 'login.html', {'login_type':'Faculty'})

def fac_dashboard(req):
    if not req.session.get('unm'):
        return redirect('faculty')    
    return render(req, 'faculty_dashboard.html')

def logout(req):
    if req.session.get('unm'):
        req.session.clear()
        return redirect('/')

def student(req):
    return render(req, 'login.html', {'login_type':'Student'})

from .models import Exam
from .serializers import ExamSerializer
from rest_framework import viewsets

from django.http import HttpResponse

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

def fac_exam(req):
    fac_dict = {'id':req.session.get('fid'), 'name':req.session.get('name')}
    return render(req, 'fac_exam.html', {'fac':fac_dict})

from .models import *
def student_dashboard(req):
    context = {'msg':'', 'exams':[], 'results':[]}
    if req.method=='POST':
        unm = req.POST.get('unm')
        pwd = req.POST.get('pwd')
        sid = req.POST.get('sid')
        req.session['sid'] = sid
        stud = Student.objects.filter(unm=unm, pwd=pwd)        
        if stud:
            assements = Assement.objects.filter(student_id=sid, is_attemp=False)
            for assement in assements:
                exams = Exam.objects.filter(id=assement.exam_id)
                if exams:
                    context['exams'].extend(exams)

            assements = Assement.objects.filter(student_id=sid, is_attemp=True)
            for assement in assements:
                exams = Exam.objects.filter(id=assement.exam_id)
                if exams:
                    context['results'].extend(exams)

        else:
            context['msg'] = 'Please check all values'
    return render(req, 'student_dashboard.html', context)


def stud_exam(req, eid=1):
    context = {'eid':eid}
    if req.method=='POST':
        qans = req.POST.copy()
        qans.pop('csrfmiddlewaretoken')
        exam = Exam.objects.filter(id=eid).first()
        print(qans)
        for _, ans in qans.items():
            aa = AssementAnswer()
            aa.answer = ans
            aa.exam = exam
            aa.scored = 0
            aa.save()
        assmet = Assement.objects.filter(exam_id=eid, student_id=req.session.get('sid')).first()
        assmet.is_attemp = True
        assmet.save()
        return redirect('sd')
    ques = Question.objects.filter(exam_id=eid)
    context['ques'] = ques
    return render(req, 'stud_exam.html', context)

def stud_res(req, eid=1):
    context = {'eid':eid, 'answerd':[]}
    assmet = Assement.objects.filter(is_attemp=True, 
                                     student_id=req.session.get('sid')).first()
    assmetans = AssementAnswer.objects.filter(exam_id=assmet.exam_id)
    ques = Question.objects.filter(exam_id=eid)
    answered = []
    total = 0
    for a, q in zip(assmetans, ques):
        total += a.scored
        answered.append({'que':q.que, 'ans':a.answer, 'score':a.scored})
    context['answerd'] = answered
    context['total'] = total
    return render(req, 'stud_res.html', context)
