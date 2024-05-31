import json
from django.shortcuts import render
from quizzes.models import Quiz, Category, Option
from account.models import Student
from django.http import HttpResponse
from tablib import Dataset

# Create your views here.
def upload(request):
    return render(request,'upload.html')

def uploadStuList(request):
    # Only listen for post request and a specific file
    if request.method == 'POST' and request.FILES.get('student_list'):
        dataset = Dataset()
        student_list = request.FILES.get("student_list")

        # Check if uploaded file any other format than xlsx
        if not student_list.name.endswith('xlsx'):
            return render(request, 'upload.html', {'error': 'Invalid Excel file'})
        
        data = dataset.load(student_list.read(),format="xlsx")
        
        # Bulk create student records filling only the registration id
        bulk_list = list()
        for datum in data:
            bulk_list.append(
                Student(registrationId=datum[0])
            )
        Student.objects.bulk_create(bulk_list)
    
        # Return success message
        return render(request, 'upload.html', {'success': 'Student list uploaded successfully'})
    
    # Default message
    return HttpResponse("Not Found")

def uploadQuiz(request):
    # Listen for only post request and a specific file
    if request.method == 'POST' and request.FILES.get('quiz_file'):
        
        #  Try to load the json file
        try:
            quizzes = request.FILES['quiz_file']
            quizzes = json.load(quizzes)

            # Loop through quizzes 
            for quiz in quizzes:
                bulk_list = list()
                
                # Loop through options of each quizzes
                for option in quiz['options']:  
                    Option.objects.create(title = option['title'],isCorrect = option['isCorrect'])
                    option_id = Option.objects.last()
                    bulk_list.append(option_id.id)
                

                # Create a new quiz with all appropriate data
                quiz = Quiz.objects.create(question = quiz['question'],category_id = 5)
                quiz.options.set(bulk_list)
        
        # Handle json file decode error
        except:
            return render(request, 'upload.html', {'error': 'Invalid JSON file'})
        
        # Return success message
        return render(request, 'upload.html', {'success': 'Quiz uploaded successfully'})
    
    # Default message
    return HttpResponse("Not Found")

def clearAll(request):
    # Delete all previous quizzes
    Quiz.objects.all().delete()
    # Category.objects.all().delete()
    Option.objects.all().delete()
    Student.objects.all().delete()
    return HttpResponse("Deleted")
    



# def uploadQuiz(request):
#     # Listen for only post request and a specific file
#     if request.method == 'POST' and request.FILES.get('quiz_file'):
        
#         #  Try to load the json file
#         try:
#             quizzes = request.FILES['quiz_file']
#             quizzes = json.load(quizzes)

#             # Loop through quizzes 
#             for quiz in quizzes:
#                 bulk_list = list()
                
#                 # Loop through options of each quizzes
#                 for option in quiz['options']:  
#                     bulk_list.append(
#                         Option(title = option['title'],isCorrect = option['isCorrect'])
#                     )
#                 Option.objects.bulk_create(bulk_list)

#                 # option_ids = []
#                 # for op in bulk_list:
#                 #     print(op.isCorrect)

#                 # Create a new quiz with all appropriate data
#                 quiz = Quiz.objects.create(question = quiz['question'],category_id = 1)
#                 quiz.options.set(bulk_list)
        
#         # Handle json file decode error
#         except json.JSONDecodeError:
#             return render(request, 'upload.html', {'error': 'Invalid JSON file'})
        
#         # Return success message
#         return render(request, 'upload.html', {'success': 'Quiz uploaded successfully'})
    
#     # Default message
#     return HttpResponse("Not Found")
