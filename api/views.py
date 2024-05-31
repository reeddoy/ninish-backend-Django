from rest_framework.decorators import api_view
from rest_framework.response import Response
from quizzes.models import Quiz, ConductingTime, Category
from account.models import Student
from .serializers import QuizSerializer, ConductingTimeSerializer
from rest_framework import status
from django.http import HttpResponse
from django.utils.timezone import now
import random

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
image_path = BASE_DIR / "api/input.png"
download_path = BASE_DIR / "api/output.png"
font_path = BASE_DIR / "api/great_vibes.ttf"

# Create your views here.


@api_view(['GET'])
def index(request):
    return HttpResponse("Ninish API", status=status.HTTP_200_OK)


@api_view(['GET'])
def getQuizzes(request,pk):
    try:
        conductingTime = ConductingTime.objects.last();
        conductingTimeStart = int(conductingTime.start.strftime('%Y%m%d%H%M'))
        conductingTimeEnd= int(conductingTime.end.strftime('%Y%m%d%H%M'))
        current_time =  now()
        current_time = int(current_time.strftime('%Y%m%d%H%M'))

        if current_time < conductingTimeStart:
            return Response(412,status=status.HTTP_412_PRECONDITION_FAILED)
       
        if current_time > conductingTimeEnd:
            return Response(412,status=status.HTTP_412_PRECONDITION_FAILED)

        quizzes = Quiz.objects.filter(category=pk)
        serialize = QuizSerializer(quizzes, many=True)
        
        if pk == 1:
            randomQuizzes = random.sample(serialize.data,30)
        elif pk == 2:
            randomQuizzes = random.sample(serialize.data,40)
        elif pk == 3:
            randomQuizzes = random.sample(serialize.data,50)
        elif pk == 4:
            randomQuizzes = random.sample(serialize.data,60)
        elif pk == 5:
            randomQuizzes = random.sample(serialize.data,60)

        return Response(randomQuizzes, status=status.HTTP_200_OK)
    except:
        return Response("Not Found", status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def getQuizzesMaster(request,pk):
    try:
        quizzes = Quiz.objects.filter(category=pk)
        serialize = QuizSerializer(quizzes, many=True)
        return Response(serialize.data, status=status.HTTP_200_OK)
    except:
        return Response("Not Found", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getConductingTime(request):
    try:
        conductingTime = ConductingTime.objects.first()
        serialize = ConductingTimeSerializer(conductingTime)
        return Response(serialize.data, status=status.HTTP_200_OK)
    except:
        return Response("Not Found", status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def submitForm(request):
    if request.method == "POST":
        user = request.data['user']
        quizzes = request.data['quizzes']
        quizTime = request.data['totalTime']
        minutes = request.data['minutes']
        seconds = request.data['seconds']

        minutes = (quizTime - int(minutes))

        if int(seconds) > 0:
            seconds = (60 - int(seconds))
        else:
            seconds = 0

        # Check if deadline is finished or not
        conductingTime = ConductingTime.objects.last();
        conductingTimeEnd = int(conductingTime.end.strftime('%Y%m%d%H%M'))
        submission_time =  now()
        submission_time = int(submission_time.strftime('%Y%m%d%H%M'))

        if submission_time > conductingTimeEnd:
            return Response(412,status=status.HTTP_412_PRECONDITION_FAILED)
        

        # Get the correct order of quiz
        quizIds = []
        # Sort the response in ascending order to match server data order 
        res = sorted(quizzes, key = lambda item: item['id'])
        count = 0
        clientQuizAns = []
        '''
         Loop through response and response.options to generate a list of dictionaries 
         containing quizId, selected quiz and option id to match server and client response
        '''

        totalQuestions = 0
        correctAnswers = 0
        wrongAnswers = 0
        attempted = 0

        for quiz in res:
            clientQuizCheck = []
            totalQuestions += 1
            # If user attempted the quiz
            if quiz['attempted'] == True:
                quizIds.append(quiz["id"])      
                attempted += 1;
                for option in quiz['options']:
                    obj = {}
                    obj["quizId"] = quiz["id"]
                    obj["flag"] = option["isSelected"]
                    obj["optionId"] = option["id"]
                    clientQuizCheck.append(obj)
                clientQuizAns.append({})
                clientQuizAns[count] = clientQuizCheck
                count += 1

        try:
            serverQuizzes = Quiz.objects.filter(id__in=quizIds)
        except:
            return Response("Not Found",status=status.HTTP_404_NOT_FOUND)
        
        serverQuizAns = []
        count = 0
        '''
         Loop through serverData and serverData.options to generate a list of dictionaries 
         containing quizId, selected quiz and option id to match server and client response
        '''
        for quiz in serverQuizzes:
            serverQuizCheck = []
            for option in quiz.options.all():
                obj = {}
                obj["quizId"] = quiz.id
                obj["flag"] = option.isCorrect
                obj["optionId"] = option.id
                serverQuizCheck.append(obj)
            serverQuizAns.append({})
            serverQuizAns[count] = serverQuizCheck
            count += 1
       
        # Count the number of dictionaries matching both client and server quiz
        for i in range(0,len(serverQuizAns)):
            if(serverQuizAns[i] == clientQuizAns[i]):
                correctAnswers += 1
            else:
                wrongAnswers += 1

        student = Student.objects.get(registrationId=user['regNumber'])

        if student.marks != 0:
            return Response({"status":409},status=status.HTTP_409_CONFLICT)
        
        student.submission_date = now()
        student.quizCompleted = True
        marks = correctAnswers - (wrongAnswers * 0.3)

        # print(totalQuestions)
        # print(attempted)
        # print(correctAnswers)
        # print(wrongAnswers)
        # print(marks)

        student.totalQuiz = totalQuestions
        student.rightAns = correctAnswers
        student.marks = marks
        student.quizTimeTaken = f'{minutes}:{seconds}'

        student.save()

    return Response({"status":200},status=status.HTTP_200_OK)

@api_view(['POST'])
def modifyUser(request):
    if request.method == "POST":
        name = request.data['name']
        regNumber = request.data['regNumber']
        stu_class = request.data['cls']
        institute = request.data['institute']
        district = request.data['district']
        quizCategoryId = request.data['quizCategory']

        categoryName = "বিশ্ববিদ্যালয়"

        # If the quiz category is correct
        try:
            quizCategory = Category.objects.get(id = quizCategoryId)
            categoryName = quizCategory.name
        except:
            quizCategoryId = 5

        student = Student.objects.get(registrationId = regNumber)
        
        student.name = name
        student.stu_class = stu_class
        student.institution = institute
        student.area = district
        student.quizCategory = categoryName
        student.quizId = quizCategoryId
        student.isDhaka = False
        student.profileCompleted = True

        student.save()

        return Response({"status":200},status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    if request.method == "POST":
        regNumber = request.data['regNumber']
        phone = request.data['phone']      
        name = request.data['name']

        try:
            student = Student.objects.get(registrationId=regNumber)

            # Check if the student has registered for Dhaka Round
            if student.isDhaka is True:
                return Response({"status":401},status=status.HTTP_401_UNAUTHORIZED)
                
            # Check if the student phone is correct
            if student.phone != phone:
                return Response({"status":401},status=status.HTTP_401_UNAUTHORIZED)
                
            # Check if the student has filled profile
            if student.profileCompleted != True:
                response = {
                    "status":201,
                    "regNumber":regNumber
                }
                return Response(response,status=status.HTTP_201_CREATED)
            
            # Check if the student has completed payment
            if student.paymentCompleted is not True:
                return Response({"status":402},status=status.HTTP_402_PAYMENT_REQUIRED)

            quizCompleted = False
            if student.quizCompleted:
                quizCompleted = True
                
            student.name = name
            student.save()

            response = {
                "status":200,
                "quizCompleted":quizCompleted,
                "quizId":student.quizId,
                "name":student.name
            }
            return Response(response,status=status.HTTP_200_OK)
        except:
            try:
                Student.objects.create(registrationId = regNumber, phone = phone,paymentCompleted = True)
                response = {
                    "status":201,
                    "regNumber":regNumber
                }
                return Response(response,status=status.HTTP_201_CREATED)
            except:
                return Response({"status":406},status=status.HTTP_406_NOT_ACCEPTABLE)
        

@api_view(['GET'])
def downloadCertificate(request,regNum):
    student = Student.objects.get(registrationId = regNum)

    name = student.name

    # Open the image
    i = Image.open(image_path)
    # add 2D graphics in an image call draw Method
    Im = ImageDraw.Draw(i)

    # Font select
    mf = ImageFont.truetype(str(font_path), 300)

    # Add Text to an image
    Im.text((1300,1600), name, (0,0,0), font=mf)

    # Save the image
    i.save(download_path)

   # Open the image file
    with open(download_path, 'rb') as file:
        # Create the HttpResponse object with file content type
        response = HttpResponse(file.read(), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="certificate.png"'
    return response
    

@api_view(['GET'])
def downloadCertificateV2(request):
    regNum = request.GET.get('regNumber')
    name = request.GET.get('name')

    try:
        student = Student.objects.get(registrationId = regNum)
    except:
        return Response({"status":404},status=status.HTTP_404_NOT_FOUND)
    
    if student.quizCompleted != True:
        return Response({"status":401},status=status.HTTP_401_UNAUTHORIZED)

    # Open the image
    i = Image.open(image_path)
    # add 2D graphics in an image call draw Method
    Im = ImageDraw.Draw(i)

    # Font select
    mf = ImageFont.truetype(str(font_path), 300)

    # Add Text to an image
    Im.text((1900,1600), name, (0,0,0), font=mf)

    # Save the image
    i.save(download_path)

    # Open the image file
    with open(download_path, 'rb') as file:
        # Create the HttpResponse object with file content type
        response = HttpResponse(file.read(), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="certificate.png"'
    return response

