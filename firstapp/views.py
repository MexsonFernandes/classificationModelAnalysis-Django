from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile, File
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail
import os
import shutil
from django.http import HttpResponse

dir_name = "sample.csv"

def index(request):
    success = 0
    if request.POST and request.FILES:
        csvfile = request.FILES['csv_file']
        global email_id
        email_id = request.POST['email_id']
        global dir_name
        shutil.copytree('MODELS_DATA/', 'MEDIA/' + str(email_id) + '/raw_data')
        dir_name = str(email_id) + '/raw_data/sample.csv'
        path = default_storage.save(dir_name, ContentFile(csvfile.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        success = 1
        os.chdir('MEDIA/' + str(email_id) + '/raw_data/')
        os.system('python runAllModels.py')
#sending mail without attachment
#         subject = 'Model Analysis of dataset | ' + str(csvfile)
#         message = "Hello Sir/Ma'am\n We have processed your file named as " + str(csvfile) + " and you can check the model analysis done using the same. \n\nTHANK YOU FOR USING OUR SERVICE,\nAlpha Machine" 
#         from_email = settings.EMAIL_HOST_USER
#         to_list = [str(email_id)]
#         send_mail(subject,message, from_email, to_list, fail_silently = False)
        try:
            email = EmailMessage('Model Analysis of dataset | ' + str(csvfile),"body",from_email=['robomex2020@gmail.com'],to=[str(email_id)])
            attach_path = "MEDIA/" + str(email_id) + "/raw_data/finalResult.csv"
            email.attach_file('finalResult.csv')
            email.send(fail_silently = False)
        except:
            return HttpResponse(" Error in sending email. Please check your settings.py file.")
    return render(request, "index.html", locals())

def download(request):
    path = email_id + "/raw_data/finalResult.csv"
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        success = 10
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            render(request,"index.html")
            return response
    return HttpResponse("<br> SOME ERROR OCCURED...WE WILL RECTIFY IT AS SOON AS POSSIBLE. <a href="">CLICK HERE </a>")
    #raise "Http404"
