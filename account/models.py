from django.db import models
from django.utils.translation import gettext_lazy as _
# from django.utils.timezone import now

# Create your models here.

class Student(models.Model):
    name = models.CharField(_("Name"), max_length=50,null=True,blank=True)
    stu_class = models.CharField(_("Class"), max_length=50,null=True,blank=True)
    institution = models.TextField(_("Institution"), null=True,blank=True)
    phone = models.CharField(_("Phone"),max_length=15,null=True,blank=True)
    registrationId = models.CharField(_("Registration Id"),max_length=255,null=True,blank=True)
    rightAns = models.IntegerField(_("Right quiz ans"),null=True,blank=True)
    totalQuiz = models.IntegerField(_("Total quizzes"),null=True,blank=True)
    marks = models.FloatField(_("Marks"),default=0)
    submission_date = models.DateTimeField(_("Submission Date"),null=True,blank=True)
    quizId = models.IntegerField(_("Quiz Id"),null=True,blank=True)
    quizCategory = models.CharField(_("Quiz Category"), max_length=50,null=True,blank=True)
    quizCompleted = models.BooleanField(_("Quiz Finished"),default=False)

    # New
    paymentCompleted = models.BooleanField(_("Payment Completed"),default=False)
    paymentRequest = models.BooleanField(_("Payment Request"),default=False)
    trxId = models.CharField(_("Trx Id"), max_length=255,null=True,blank=True)
    senderPhone = models.CharField(_("Sender Phone"),max_length=15,null=True,blank=True)
    receiverPhone = models.CharField(_("Receiver Phone"),max_length=50,null=True,blank=True)

    area = models.CharField(_("Area"), max_length=255,null=True,blank=True)
    isDhaka = models.BooleanField(_("Is Dhaka"),default=True)
    
    profileCompleted = models.BooleanField(_("Profile Completed"),default=False)

    otp = models.CharField(_("OTP"),max_length=4,null=True,blank=True)
    otpVerified = models.BooleanField(_("Verified"),default=False)
    otpTime = models.DateTimeField(_("Otp deadline"),null=True,blank=True)

    quizTimeTaken = models.CharField(_("Quiz Time Taken"),max_length=5,null=True,blank=True)

    def __str__(self):
        return f'{self.name} - {self.registrationId}'
    