function init() {
    // alert('all set')
    // getExams()
}



function getExams() {
    const exam_url = 'http://127.0.0.1:8000/api/exams/'
    fetch(exam_url)
    .then(res=>res.json())
    .then(data=>{
        let str_html = ''
        facid = document.getElementById('facid').value
        data.forEach(element => {
            if (facid==element.faculty)
                str_html += element.exam + ' - ' + element.startdate + '<hr/>'
        });
        document.getElementById('idExams').innerHTML = str_html
    })
}

function saveExam(){
    const exam = document.getElementById('exam').value
    const startdate = document.getElementById('startdate').value
    const enddate = document.getElementById('enddate').value
    const facid = document.getElementById('facid').value

    const exam_url = 'http://127.0.0.1:8000/api/exams/'
    fetch(exam_url,{
        'method':'POST',
        'headers':{'Content-Type':'application/json'},
        'body':JSON.stringify({
            exam:exam, 
            startdate:startdate,
            enddate:enddate,
            faculty:facid
        })
    })
    .then(res=>res.json())
    .then(data=>{
        console.log(data)
        getExams()
    })
    .catch(error=>alert(error))
}