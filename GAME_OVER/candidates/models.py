from django.db import models
from django.utils import timezone

class JobTitle(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Interviewer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Stage(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SubStage(models.Model):
    name = models.CharField(max_length=255)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='sub_stages')

    def __str__(self):
        return self.name

#------------------------------- Administrator -------------------------------------------------------------- 

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    job_title = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
    notice_period = models.CharField(max_length=100, null=True, blank=True)
    stage = models.CharField(max_length=100, null=True, blank=True)
    sub_stage = models.CharField(max_length=100, null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    position_status = models.CharField(max_length=100, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    interview_status = models.CharField(max_length=100, null=True, blank=True)
    interview_date = models.DateField(null=True, blank=True)
    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    sourcer = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=100)
    email_id = models.CharField(max_length=100)
    current_company = models.CharField(max_length=100, null=True, blank=True)
    current_position = models.CharField(max_length=100, null=True, blank=True)
    experience_years_months = models.CharField(max_length=100, null=True, blank=True)
    relevant_experience = models.CharField(max_length=100, null=True, blank=True)
    current_salary_lpa = models.CharField(max_length=100, null=True, blank=True)
    expected_salary_lpa = models.CharField(max_length=100, null=True, blank=True)
    other_offers_lpa = models.CharField(max_length=100, null=True, blank=True)
    last_working_day = models.CharField(max_length=100, null=True, blank=True)
    internal_screening = models.DateField(null=True, blank=True)
    date_of_interview_2 = models.DateField(null=True, blank=True)
    date_of_interview_3 = models.DateField(null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    evaluation_link = models.URLField(max_length=200, null=True, blank=True)
    joined_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.name

    
class CandidateSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='candidate_submissions/')
    location = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    submission_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    

    
class JobOpening(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low')
    ]

    job_title = models.ForeignKey(JobTitle, on_delete=models.CASCADE, null=True, blank=True)
    branch_location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    number_of_openings = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='Medium')
    recruiter = models.ForeignKey(Interviewer, on_delete=models.CASCADE, null=True, blank=True)
    job_description = models.FileField(upload_to='job_descriptions/', null=True, blank=True)

    def __str__(self):
        return self.job_title