from django import forms
from .models import Candidate, JobTitle, Location, Interviewer, Stage, SubStage, CandidateSubmission, JobOpening

# Define choices for the dropdown fields
NOTICE_PERIOD_CHOICES = [
    ('Immediate', 'Immediate'),
    ('Serving', 'Serving'),
    ('15 days', '15 days'),
    ('30 Days', '30 Days'),
    ('45 Days', '45 Days'),
    ('60 Days', '60 Days'),
    ('90 Days', '90 Days'),
]

SOURCE_CHOICES = [
    ('Linkedin', 'Linkedin'),
    ('Shine', 'Shine'),
    ('Naukri', 'Naukri'),
    ('Referals', 'Referals'),
    ('Vendors / Consultancy', 'Vendors / Consultancy'),
    ('Walk-in', 'Walk-in'),
    ('Internal Reference', 'Internal Reference'),
    ('Indeed', 'Indeed'),
]

SOURCER_CHOICES = [
    ('Telephonic', 'Telephonic'),
    ('MS Teams', 'MS Teams'),
    ('Zoom', 'Zoom'),
    ('WebEx', 'WebEx'),
    ('G Meet', 'G Meet'),
    ('Monjin', 'Monjin'),
    ('FIPO', 'FIPO'),
]

EXPERIENCE_YEARS_MONTHS_CHOICES = [
    ('Fresher', 'Fresher'),
    ('0-1', '0-1'),
    ('1-2', '1-2'),
    ('2-3', '2-3'),
    ('3-4', '3-4'),
    ('4-5', '4-5'),
    ('5-6', '5-6'),
    ('6-7', '6-7'),
    ('7-8', '7-8'),
    ('8-9', '8-9'),
    ('9-10', '9-10'),
    ('10-11', '10-11'),
    ('11-12', '11-12'),
    ('12-13', '12-13'),
    ('13-14', '13-14'),
    ('14-15', '14-15'),
    ('15-16', '15-16'),
    ('16-17', '16-17'),
    ('17-18', '17-18'),
    ('18-19', '18-19'),
    ('19-20', '19-20'),
]

RELEVANT_EXPERIENCE_CHOICES = [
    ('Fresher', 'Fresher'),
    ('0-1 years', '0-1 years'),
    ('1-2 years', '1-2 years'),
    ('2-3 years', '2-3 years'),
    ('3-5 years', '3-5 years'),
    ('5-10 years', '5-10 years'),
    ('10-15 years', '10-15 years'),
    ('15-20 years', '15-20 years'),
]

class CandidateForm(forms.ModelForm):
    notice_period = forms.ChoiceField(choices=NOTICE_PERIOD_CHOICES, label='Notice Period')
    source = forms.ChoiceField(choices=SOURCE_CHOICES, label='Source')
    sourcer = forms.ChoiceField(choices=SOURCER_CHOICES, label='Sourcer')
    experience_years_months = forms.ChoiceField(choices=EXPERIENCE_YEARS_MONTHS_CHOICES, label='Experience (Years-Months)')
    relevant_experience = forms.ChoiceField(choices=RELEVANT_EXPERIENCE_CHOICES, label='Relevant Experience')
    
    stage = forms.ChoiceField(choices=[
        ('1-Screening', '1-Screening'),
        ('2-Interview', '2-Interview'),
        ('3-Selection', '3-Selection'),
        ('4-Offer', '4-Offer'),
        ('5-Joined', '5-Joined'),
        ('6-Reject', '6-Reject'),
        ('7-Hold', '7-Hold'),
    ], label='Stage')
    
    sub_stage = forms.ChoiceField(choices=[
        ('1 - Internal Screening', '1 - Internal Screening'),
        ('11 - Internal Screening Cleared', '11 - Internal Screening Cleared'),
        ('100 - CV Pending to be shared', '100 - CV Pending to be shared'),
        ('101 - CV Feedback Pending', '101 - CV Feedback Pending'),
        ('102 - CV sent for Screening', '102 - CV sent for Screening'),
        ('103 - Test Link to be shared', '103 - Test Link to be shared'),
        ('104 - Test Completion Pending', '104 - Test Completion Pending'),
        ('201 - L1 Pending', '201 - L1 Pending'),
        ('202 - L1 Scheduled', '202 - L1 Scheduled'),
        ('203 - L1 Reschedule-Panel No Show', '203 - L1 Reschedule-Panel No Show'),
        ('204 - L1 Reschedule-Candidate No Show', '204 - L1 Reschedule-Candidate No Show'),
        ('205 - L1 FB Pending', '205 - L1 FB Pending'),
        ('206 - L2 Pending', '206 - L2 Pending'),
        ('207 - L2 Scheduled', '207 - L2 Scheduled'),
        ('208 - L2 Reschedule-Panel No Show', '208 - L2 Reschedule-Panel No Show'),
        ('209 - L2 Reschedule-Candidate No Show', '209 - L2 Reschedule-Candidate No Show'),
        ('210 - L2 FB Pending', '210 - L2 FB Pending'),
        ('300 - Final Select', '300 - Final Select'),
        ('401 - Documents Pending', '401 - Documents Pending'),
        ('402 - HR Pending', '402 - HR Pending'),
        ('403 - Offer WIP', '403 - Offer WIP'),
        ('404 - Offer Acceptance Pending', '404 - Offer Acceptance Pending'),
        ('405 - Offer Accepted', '405 - Offer Accepted'),
        ('500 - Joined', '500 - Joined'),
        ('601 - Reject - Screen Reject', '601 - Reject - Screen Reject'),
        ('603 - Reject - CV Duplicate', '603 - Reject - CV Duplicate'),
        ('604 - Reject - Test', '604 - Reject - Test'),
        ('605 - Reject - Not Attended Interview', '605 - Reject - Not Attended Interview'),
        ('606 - Reject - Higher NP', '606 - Reject - Higher NP'),
        ('607 - Reject - Time delay', '607 - Reject - Time delay'),
        ('608 - Reject - L1 Interview', '608 - Reject - L1 Interview'),
        ('609 - Reject - L2 Interview', '609 - Reject - L2 Interview'),
        ('610 - Reject - Not ready to relocate', '610 - Not ready to relocate'),
        ('611 - Reject - Shift timing issue', '611 - Shift timing issue'),
        ('612 - Reject - Expecting higher CTC', '612 - Expecting higher CTC'),
        ('613 - Reject - Found other opportunity', '613 - Found other opportunity'),
        ('614 - Reject - Test link not shared', '614 - Test link not shared'),
        ('615 - Reject -Test not completed', '615 - Test not completed'),
        ('616 - Reject - Interview scheduled after due date', '616 - Interview scheduled after due date'),
        ('617 - Reject - Offer Declined', '617 - Offer Declined'),
        ('618 - Reject - Offer Declined Counter Offer', '618 - Offer Declined Counter Offer'),
        ('700 - On Hold', '700 - On Hold'),
    ], label='Sub Stage')
    
    position_status = forms.ChoiceField(choices=[
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Closed', 'Closed'),
    ], label='Position Status')

    class Meta:
        model = Candidate
        fields = [
            'name', 'contact_number', 'email_id', 'job_title', 'location', 'notice_period', 'stage', 
            'sub_stage', 'source', 'position_status', 'interview_date', 'interviewer', 'sourcer', 
            'current_company', 'current_position', 'experience_years_months', 'relevant_experience', 
            'current_salary_lpa', 'expected_salary_lpa', 'other_offers_lpa', 'last_working_day', 
            'internal_screening', 'date_of_interview_2', 'date_of_interview_3', 'joined_date', 
            'evaluation_link', 'remark', 'resume'
        ]

        widgets = {
            'interview_date': forms.DateInput(attrs={'type': 'date'}),
            'last_working_day': forms.DateInput(attrs={'type': 'date'}),
            'internal_screening': forms.DateInput(attrs={'type': 'date'}),
            'date_of_interview_2': forms.DateInput(attrs={'type': 'date'}),
            'date_of_interview_3': forms.DateInput(attrs={'type': 'date'}),
            'joined_date': forms.DateInput(attrs={'type': 'date'}),
        }

# Form for Candidate Submission
class CandidateSubmissionForm(forms.ModelForm):
    position = forms.ModelChoiceField(
        queryset=JobTitle.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="All Positions"
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="All Branches"
    )

    class Meta:
        model = CandidateSubmission
        fields = ['name', 'email', 'phone', 'position', 'location', 'resume']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# Form for Job Opening
class JobOpeningForm(forms.ModelForm):
    class Meta:
        model = JobOpening
        fields = ['job_title', 'branch_location', 'number_of_openings', 'status', 'priority', 'recruiter', 'job_description']
        widgets = {
            'number_of_openings': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'job_description': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['job_title'] = forms.ModelChoiceField(queryset=JobTitle.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['branch_location'] = forms.ModelChoiceField(queryset=Location.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['recruiter'] = forms.ModelChoiceField(queryset=Interviewer.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))

# Administrative forms
class JobTitleForm(forms.ModelForm):
    class Meta:
        model = JobTitle
        fields = ['name']

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']

class InterviewerForm(forms.ModelForm):
    class Meta:
        model = Interviewer
        fields = ['name']

class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['name']

class SubStageForm(forms.ModelForm):
    class Meta:
        model = SubStage
        fields = ['name']
