# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Sum
from datetime import datetime, timedelta
from openpyxl import Workbook
import pandas as pd

from .forms import CandidateForm, CandidateSubmissionForm, JobOpeningForm
from .models import Candidate, CandidateSubmission, JobOpening

# Function views using the imports above
############################################################################################################################
                                            #   LOGIN
##########################################################################################################################
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.models import User

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check hardcoded credentials
        if username == 'it@lakshyaca.com' and password == 'it@lakshyaca.com':
            # Check if the user exists in the database
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)  # Set the user's password
                user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'login.html')



# candidates/middleware.py

from django.shortcuts import redirect





    ############################################################################################################################
                                            #   HOME
##########################################################################################################################
@login_required
def home(request):
    return render(request, 'home.html')
############################################################################################################################
                                            #   ADD CANDIDATW
##########################################################################################################################
@login_required
def add_candidate(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('reports_home')
    else:
        form = CandidateForm()
    return render(request, 'add_candidate.html', {'form': form})
############################################################################################################################
                                            # OLD MANAGE CANDIDATE PAGE-  NOT USING
##########################################################################################################################



# def manage_candidates(request):
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#     candidates_list = Candidate.objects.all()
    
#     if start_date and end_date:
#         candidates_list = candidates_list.filter(interview_date__range=[start_date, end_date])

#     paginator = Paginator(candidates_list, 10)  # Show 10 candidates per page.
#     page_number = request.GET.get('page')
#     try:
#         candidates = paginator.page(page_number)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver first page.
#         candidates = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range, deliver last page of results.
#         candidates = paginator.page(paginator.num_pages)
    
#     return render(request, 'manage_candidates.html', {'candidates': candidates})
############################################################################################################################
                                            #   CANDIDATE DETAIL
##########################################################################################################################
@login_required
def candidate_detail(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    return render(request, 'candidate_detail.html', {'candidate': candidate})




############################################################################################################################
                                            #   CANDIDATE EDIT
##########################################################################################################################



@login_required
def candidate_edit(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Candidate details updated successfully.')
            return redirect('reports_home')
        else:
            messages.error(request, 'There was an error saving the form. Please check the fields and try again.')
    else:
        form = CandidateForm(instance=candidate)
    return render(request, 'candidate_edit.html', {'form': form, 'candidate': candidate})

@login_required
def candidate_delete(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    if request.method == 'POST':
        candidate.delete()
        return redirect('reports_home')
    # return render(request, 'candidate_delete.html', {'candidate': candidate})
@login_required
def download_candidates_excel(request):
    interviewer = request.GET.get('interviewer')
    candidates = Candidate.objects.filter(interviewer=interviewer)

    wb = Workbook()
    ws = wb.active
    ws.append(['Name', 'Job Title', 'Notice Period', 'Stage', 'Sub Stage', 'Source', 'Position Status', 'Location', 'Interview Status', 'Interview Date', 'Interviewer', 'Resume'])
    for candidate in candidates:
        ws.append([candidate.name, candidate.job_title, candidate.notice_period, candidate.stage, candidate.sub_stage, candidate.source, candidate.position_status, candidate.location, candidate.interview_status, candidate.interview_date, candidate.interviewer, candidate.resume.url])

    from io import BytesIO
    buffer = BytesIO()
    wb.save(buffer)

    response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=candidates.xlsx'
    return response

############################################################################################################################
                                            #   RECRUITEMNT OVERVIEW
##########################################################################################################################


from django.db.models import Count
@login_required
def interviewers_list(request):
    interviewers = Candidate.objects.values('interviewer__name').annotate(count=Count('interviewer')).distinct()
    interviewers_list = [interviewer['interviewer__name'] for interviewer in interviewers]
    interviewers_data = {interviewer['interviewer__name']: interviewer['count'] for interviewer in interviewers}
    
    return render(request, 'interviewers_list.html', {
        'interviewers': interviewers_list,
        'interviewers_data': interviewers_data
    })


############################################################################################################################
                                            #   INTERVIEWR CANDIDATES
##########################################################################################################################
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render
from .models import Candidate, Interviewer  # Assuming Interviewer is the related model

import json

LOCATION_CHOICES = [
    ('Kochi', 'Kochi'),
    ('Calicut', 'Calicut'),
    ('Kannur', 'Kannur'),
    ('Kottayam', 'Kottayam'),
    ('Trivandrum', 'Trivandrum'),
    ('Thrissur', 'Thrissur'),
    ('Bangalore', 'Bangalore'),
    ('Dubai', 'Dubai'),
    ('Kolkata', 'Kolkata'),
    ('Delhi', 'Delhi'),
]

from django.shortcuts import get_object_or_404, render
from .models import Candidate, Interviewer
@login_required
def interviewer_candidates(request, interviewer):
    interviewer_obj = get_object_or_404(Interviewer, name=interviewer)
    candidates = Candidate.objects.filter(interviewer=interviewer_obj)
    
    # Optional: Filtering by location
    location = request.GET.get('location')
    if location:
        candidates = candidates.filter(location=location)
    
    # Pagination
    paginator = Paginator(candidates, 100)  # Show 100 candidates per page
    page_number = request.GET.get('page')
    try:
        candidates = paginator.page(page_number)
    except PageNotAnInteger:
        candidates = paginator.page(1)
    except EmptyPage:
        candidates = paginator.page(paginator.num_pages)
    
    return render(request, 'interviewer_candidates.html', {
        'candidates': candidates,
        'interviewer': interviewer_obj,
        'location_choices': LOCATION_CHOICES,
    })


############################################################################################################################
                                            #   360 VIEW
##########################################################################################################################

from django.shortcuts import render
from django.db.models import Count
from datetime import datetime
import json
from .models import Candidate, JobOpening, CandidateSubmission
from django.db.models.functions import ExtractMonth, ExtractYear

from django.shortcuts import render
from django.db.models import Count, Sum
from datetime import datetime, timedelta
import json
from .models import Candidate, JobOpening, CandidateSubmission
from django.db.models.functions import ExtractMonth
@login_required
def view_360(request):
    # Current date
    today = datetime.today()

    # Start of the current week and month
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    # Calculating weekly and monthly interviews
    weekly_interviews = Candidate.objects.filter(interview_date__gte=start_of_week).count()
    monthly_interviews = Candidate.objects.filter(interview_date__gte=start_of_month).count()

    # Total number of interviews
    total_interviews = Candidate.objects.filter(interview_date__isnull=False).count()

    # Branch-wise data for candidates
    candidate_branch_data = Candidate.objects.values('location__name').annotate(total=Count('id')).order_by('-total')
    candidate_branch_labels = [location['location__name'] for location in candidate_branch_data]
    candidate_branch_values = [location['total'] for location in candidate_branch_data]

    # Branch-wise data for job openings
    job_openings_data = JobOpening.objects.filter(status='open').values('branch_location__name').annotate(total_openings=Sum('number_of_openings')).order_by('-total_openings')
    job_openings_labels = [opening['branch_location__name'] for opening in job_openings_data]
    job_openings_values = [opening['total_openings'] for opening in job_openings_data]

    # Source of candidates
    candidate_sources = Candidate.objects.values('source').annotate(total=Count('source')).order_by('-total')
    source_labels = [source['source'] for source in candidate_sources]
    source_values = [source['total'] for source in candidate_sources]

    # Interviewer data
    interviewer_data = Candidate.objects.values('interviewer__name').annotate(total=Count('interviewer')).order_by('-total')
    interviewer_labels = [interviewer['interviewer__name'] for interviewer in interviewer_data]
    interviewer_values = [interviewer['total'] for interviewer in interviewer_data]

    # Count rejected and offered candidates
    rejected_candidates = Candidate.objects.filter(stage="6-Reject").count()
    offered_candidates = Candidate.objects.filter(stage="4-Offer").count()

    # Hiring Trends: Get the selected year from the request (default to the current year)
    selected_year = request.GET.get('year', today.year)
    selected_year = int(selected_year)

    # Create a list of years to be used in the dropdown
    years = list(range(2024, 2031))

    # Filter candidates based on the selected year and stage '5-Joined'
    candidates = Candidate.objects.filter(stage='5-Joined', interview_date__year=selected_year)

    # Annotate the count of candidates grouped by month
    monthly_data = candidates.annotate(month=ExtractMonth('interview_date')).values('month').annotate(count=Count('id')).order_by('month')

    # Prepare data for the chart
    chart_data = [0] * 12  # Initialize list with 12 zeros (for 12 months)
    for data in monthly_data:
        chart_data[data['month'] - 1] = data['count']  # Fill the count for the corresponding month

    # Context to pass to the template
    context = {
        'total_candidates': Candidate.objects.count(),
        'current_job_openings': JobOpening.objects.filter(status='open').count(),
        'total_candidate_submissions': CandidateSubmission.objects.count(),
        'total_interviews': total_interviews,
        'weekly_interviews': weekly_interviews,
        'monthly_interviews': monthly_interviews,
        'candidate_branch_labels': json.dumps(candidate_branch_labels),
        'candidate_branch_values': json.dumps(candidate_branch_values),
        'job_openings_labels': json.dumps(job_openings_labels),
        'job_openings_values': json.dumps(job_openings_values),
        'source_labels': json.dumps(source_labels),
        'source_values': json.dumps(source_values),
        'interviewer_labels': json.dumps(interviewer_labels),
        'interviewer_values': json.dumps(interviewer_values),
        'rejected_candidates': rejected_candidates,
        'offered_candidates': offered_candidates,
        'selected_year': selected_year,
        'years': years,
        'chart_data': json.dumps(chart_data),  # Data for the Hiring Trends chart
    }

    return render(request, '360_view.html', context)



############################################################################################################################
                                            #   SEARCH CANDIDATE
##########################################################################################################################
@login_required
def search_candidate(request):
    if 'mobile_number' in request.GET:
        mobile_number = request.GET['mobile_number']
        try:
            candidate = Candidate.objects.get(contact_number=mobile_number)
        except Candidate.DoesNotExist:
            candidate = None
        return render(request, 'search_candidate.html', {'candidate': candidate})
    else:
        return render(request, 'search_candidate.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import JobOpening, CandidateSubmission
from .forms import CandidateSubmissionForm

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import JobOpening, CandidateSubmission, JobTitle, Location
from .forms import CandidateSubmissionForm


############################################################################################################################
                                            #   CANDIDATE FORM
##########################################################################################################################

def candidate_submission(request):
    if request.method == 'POST':
        form = CandidateSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your resume has been submitted successfully.')
            return redirect('candidate_submission')
        else:
            messages.error(request, 'There was an error with your submission. Please try again.')
    else:
        form = CandidateSubmissionForm()
    
    job_titles = JobTitle.objects.all()  # Query the JobTitle model
    branch_locations = Location.objects.all()  # Query the Location model
    
    context = {
        'form': form,
        'job_titles': job_titles,
        'branch_locations': branch_locations,
    }
    
    return render(request, 'candidate_submission.html', context)






from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.utils.dateparse import parse_date
from datetime import datetime
import pandas as pd
from .forms import CandidateSubmissionForm
from .models import CandidateSubmission, JobTitle, Location
############################################################################################################################
                                            #   CANDIDATE DRIVE
##########################################################################################################################

# Your view functions can go here
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from datetime import datetime
import pandas as pd
from .models import CandidateSubmission, JobTitle, Location
@login_required
def view_submissions(request):
    selected_position = request.GET.get('position')
    selected_branch = request.GET.get('branch')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    positions = JobTitle.objects.all()
    branches = Location.objects.all()
    selected_position_name = None

    candidates = CandidateSubmission.objects.all()

    # Apply filters if provided
    if selected_position and selected_position != 'None':
        try:
            position_obj = JobTitle.objects.get(id=selected_position)
            candidates = candidates.filter(position=position_obj.name)
            selected_position_name = position_obj.name
        except JobTitle.DoesNotExist:
            candidates = candidates.none()

    if selected_branch and selected_branch != 'None':
        try:
            branch_obj = Location.objects.get(id=selected_branch)
            candidates = candidates.filter(location=branch_obj.name)
        except Location.DoesNotExist:
            candidates = candidates.none()

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            candidates = candidates.filter(submission_date__range=[start_date, end_date])
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")

    # Pagination count (items per page)
    pagination_count = int(request.GET.get('pagination_count', 10))  # Default to 10 items per page
    paginator = Paginator(candidates.order_by('id'), pagination_count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'view_submissions.html', {
        'page_obj': page_obj,
        'positions': positions,
        'branches': branches,
        'selected_position': selected_position,
        'selected_position_name': selected_position_name,
        'selected_branch': selected_branch,
        'start_date': start_date,
        'end_date': end_date,
        'pagination_count': pagination_count,
        'export_url': build_export_url(request),
    })
@login_required
def build_export_url(request):
    base_url = request.path.replace('view_submissions', 'export_submissions')
    params = request.GET.copy()
    return f"{base_url}?{params.urlencode()}"
@login_required
def export_submissions(request):
    select_all = request.POST.get('select_all') == 'true'
    selected_candidates = request.POST.getlist('selected_candidates')

    if select_all:
        candidates = CandidateSubmission.objects.all()
    else:
        candidates = CandidateSubmission.objects.filter(id__in=selected_candidates)

    if not candidates.exists():
        response = HttpResponse("No data available to export.", content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=candidates.txt'
        return response

    data = [
        {
            'Name': candidate.name,
            'Email': candidate.email,
            'Phone': candidate.phone,
            'Position': candidate.position,
            'Location': candidate.location,
            'Resume': candidate.resume.url if candidate.resume else 'No Resume',
            'Submission Date': candidate.submission_date.strftime('%Y-%m-%d') if candidate.submission_date else 'No Date',
        }
        for candidate in candidates
    ]

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=candidates.xlsx'
    df.to_excel(response, index=False)
    return response
@login_required
def delete_submissions(request):
    select_all = request.POST.get('select_all') == 'true'
    selected_candidates = request.POST.getlist('selected_candidates')

    if select_all:
        candidates = CandidateSubmission.objects.all()
    else:
        candidates = CandidateSubmission.objects.filter(id__in=selected_candidates)

    if candidates.exists():
        candidates.delete()
        messages.success(request, "Selected candidates have been deleted.")
    else:
        messages.error(request, "No candidates selected for deletion.")

    return redirect('view_submissions')







############################################################################################################################
                                            #   JOB OPENING/CLOSED
##########################################################################################################################


from django.shortcuts import render
from .models import JobOpening

from django.shortcuts import render
from .models import JobOpening

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import JobOpening
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CandidateSubmissionForm
from .models import CandidateSubmission
from django.http import HttpResponse
import pandas as pd
from django.utils.dateparse import parse_date
@login_required
def job_dashboard(request):
    jobs = JobOpening.objects.all()

    # Get filter values from request
    branch_location_id = request.GET.get('branch_location')
    status = request.GET.get('status')
    priority = request.GET.get('priority')
    recruiter_id = request.GET.get('recruiter')

    # Apply filters if provided
    if branch_location_id and branch_location_id != 'None':
        if branch_location_id.isdigit():
            jobs = jobs.filter(branch_location_id=branch_location_id)
        else:
            jobs = jobs.none()  # or handle this case appropriately

    if status and status != 'None':
        if status in dict(JobOpening.STATUS_CHOICES):
            jobs = jobs.filter(status=status)
        else:
            jobs = jobs.none()  # or handle this case appropriately

    if priority and priority != 'None':
        if priority in dict(JobOpening.PRIORITY_CHOICES):
            jobs = jobs.filter(priority=priority)
        else:
            jobs = jobs.none()  # or handle this case appropriately
            
    if recruiter_id and recruiter_id != 'None':
        if recruiter_id.isdigit():
            jobs = jobs.filter(recruiter_id=recruiter_id)
        else:
            jobs = jobs.none()  # or handle this case appropriately

    # Get choices
    branch_location_choices = Location.objects.all()
    status_choices = JobOpening._meta.get_field('status').choices
    priority_choices = JobOpening._meta.get_field('priority').choices
    recruiter_choices = Interviewer.objects.all()

    # Count open and closed jobs
    open_jobs_count = jobs.filter(status='open').count()
    closed_jobs_count = jobs.filter(status='closed').count()

    # Paginate jobs
    paginator = Paginator(jobs, 7)  # Show 7 jobs per page
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    return render(request, 'job_dashboard.html', {
        'jobs': jobs,
        'branch_location': branch_location_id,
        'status': status,
        'priority': priority,
        'recruiter': recruiter_id,
        'branch_location_choices': branch_location_choices,
        'status_choices': status_choices,
        'priority_choices': priority_choices,
        'recruiter_choices': recruiter_choices,
        'open_jobs_count': open_jobs_count,
        'closed_jobs_count': closed_jobs_count,
    })

from django.shortcuts import render, redirect, get_object_or_404
from .forms import JobOpeningForm
from .models import JobOpening
@login_required
def add_job_opening(request):
    if request.method == 'POST':
        form = JobOpeningForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('job_dashboard')
    else:
        form = JobOpeningForm()
    return render(request, 'add_job_opening.html', {'form': form})
@login_required
def edit_job_opening(request, pk):
    job = get_object_or_404(JobOpening, pk=pk)
    if request.method == 'POST':
        form = JobOpeningForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_dashboard')
    else:
        form = JobOpeningForm(instance=job)
    return render(request, 'edit_job_opening.html', {'form': form, 'job': job})
@login_required
def delete_job_opening(request, pk):
    job = get_object_or_404(JobOpening, pk=pk)
    if request.method == 'POST':
        job.delete()
        return redirect('job_dashboard')
    return redirect('job_dashboard')



# candidate_management/views.py


############################################################################################################################
                                            #   CONFIGURE
##########################################################################################################################

from django.http import HttpResponse
import pandas as pd
from .models import Candidate, JobTitle, Location, Interviewer
from datetime import datetime

from django.http import HttpResponse
import pandas as pd
from .models import Candidate, JobTitle, Location
from datetime import datetime

from django.http import HttpResponse
import pandas as pd
from .models import Candidate, JobTitle, Location
from datetime import datetime

from django.http import HttpResponse
import pandas as pd
from .models import Candidate, JobTitle, Location
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from .models import Candidate, JobTitle, Location, Interviewer
from datetime import datetime

from django.http import HttpResponse
import pandas as pd
from .models import Candidate, JobTitle, Location, Interviewer
from datetime import datetime
from docx import Document
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas




from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import JobTitle, Location, Interviewer, Stage, SubStage
from .forms import JobTitleForm, LocationForm, InterviewerForm, StageForm, SubStageForm
@login_required
def administrator(request):
    job_positions = JobTitle.objects.all()
    locations = Location.objects.all()
    interview_stages = Stage.objects.all()
    sub_stages = SubStage.objects.all()
    interviewers = Interviewer.objects.all()

    job_position_form = JobTitleForm()
    location_form = LocationForm()
    interview_stage_form = StageForm()
    sub_stage_form = SubStageForm()
    interviewers_form = InterviewerForm()
    
    if request.method == 'POST':
        if 'job_position_submit' in request.POST:
            job_position_form = JobTitleForm(request.POST)
            if job_position_form.is_valid():
                job_position_form.save()
                return redirect(f"{reverse('administrator')}?section=job-position-section")
        elif 'location_submit' in request.POST:
            location_form = LocationForm(request.POST)
            if location_form.is_valid():
                location_form.save()
                return redirect(f"{reverse('administrator')}?section=location-section")
        elif 'interview_stage_submit' in request.POST:
            interview_stage_form = StageForm(request.POST)
            if interview_stage_form.is_valid():
                interview_stage_form.save()
                return redirect(f"{reverse('administrator')}?section=interview-stage-section")
        elif 'sub_stage_submit' in request.POST:
            sub_stage_form = SubStageForm(request.POST)
            if sub_stage_form.is_valid():
                sub_stage_form.save()
                return redirect(f"{reverse('administrator')}?section=sub-stage-section")
        elif 'interviewer_submit' in request.POST:
            interviewers_form = InterviewerForm(request.POST)
            if interviewers_form.is_valid():
                interviewers_form.save()
                return redirect(f"{reverse('administrator')}?section=interviewers-section")

    return render(request, 'administrator.html', {
        'job_positions': job_positions,
        'locations': locations,
        'interview_stages': interview_stages,
        'sub_stages': sub_stages,
        'interviewers': interviewers,
        'job_position_form': job_position_form,
        'location_form': location_form,
        'interview_stage_form': interview_stage_form,
        'sub_stage_form': sub_stage_form,
        'interviewers_form': interviewers_form,
    })
@login_required
def job_position_update(request, pk):
    job_position = get_object_or_404(JobTitle, pk=pk)
    if request.method == 'POST':
        form = JobTitleForm(request.POST, instance=job_position)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('administrator')}?section=job-position-section")
    else:
        form = JobTitleForm(instance=job_position)
    
    return render(request, 'administrator.html', {
        'job_position_form': form,
        'job_positions': JobTitle.objects.all(),  # Ensure the list of job positions is passed
    })

@login_required
def job_position_delete(request, pk):
    job_position = get_object_or_404(JobTitle, pk=pk)
    if request.method == 'POST':
        job_position.delete()
        return redirect(f"{reverse('administrator')}?section=job-position-section")
    return redirect(f"{reverse('administrator')}?section=job-position-section")
@login_required
def location_update(request, pk):
    location = get_object_or_404(Location, pk=pk)
    form = LocationForm(request.POST or None, instance=location)
    if form.is_valid():
        form.save()
        return redirect(f"{reverse('administrator')}?section=location-section")
    return redirect(f"{reverse('administrator')}?section=location-section")
@login_required
def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        location.delete()
        return redirect(f"{reverse('administrator')}?section=location-section")
    return redirect(f"{reverse('administrator')}?section=location-section")
@login_required
def interview_stage_update(request, pk):
    interview_stage = get_object_or_404(Stage, pk=pk)
    form = StageForm(request.POST or None, instance=interview_stage)
    if form.is_valid():
        form.save()
        return redirect(f"{reverse('administrator')}?section=interview-stage-section")
    return redirect(f"{reverse('administrator')}?section=interview-stage-section")
@login_required
def interview_stage_delete(request, pk):
    interview_stage = get_object_or_404(Stage, pk=pk)
    if request.method == 'POST':
        interview_stage.delete()
        return redirect(f"{reverse('administrator')}?section=interview-stage-section")
    return redirect(f"{reverse('administrator')}?section=interview-stage-section")
@login_required
def sub_stage_update(request, pk):
    sub_stage = get_object_or_404(SubStage, pk=pk)
    form = SubStageForm(request.POST or None, instance=sub_stage)
    if form.is_valid():
        form.save()
        return redirect(f"{reverse('administrator')}?section=sub-stage-section")
    return redirect(f"{reverse('administrator')}?section=sub-stage-section")
@login_required
def sub_stage_delete(request, pk):
    sub_stage = get_object_or_404(SubStage, pk=pk)
    if request.method == 'POST':
        sub_stage.delete()
        return redirect(f"{reverse('administrator')}?section=sub-stage-section")
    return redirect(f"{reverse('administrator')}?section=sub-stage-section")
@login_required
def interviewer_update(request, pk):
    interviewers = get_object_or_404(Interviewer, pk=pk)
    form = InterviewerForm(request.POST or None, instance=interviewers)
    if form.is_valid():
        form.save()
        return redirect(f"{reverse('administrator')}?section=interviewers-section")
    return redirect(f"{reverse('administrator')}?section=interviewers-section")
@login_required
def interviewer_delete(request, pk):
    interviewers = get_object_or_404(Interviewer, pk=pk)
    if request.method == 'POST':
        interviewers.delete()
        return redirect(f"{reverse('administrator')}?section=interviewers-section")
    return redirect(f"{reverse('administrator')}?section=interviewers-section")

#------------------------------- Administrator -------------------------------------------------------------- 
############################################################################################################################
                                            #   REPORTS
##########################################################################################################################


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Candidate, JobTitle, Location, Interviewer
from datetime import datetime
import pandas as pd
from django.core.paginator import Paginator
@login_required
def reports_home(request):
    candidates = Candidate.objects.all()

    # Filtering parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    interviewer = request.GET.get('interviewer')
    job_title_id = request.GET.get('job_title')
    location_id = request.GET.get('location')
    stage = request.GET.get('stage')

    # Filter by job title
    if job_title_id and job_title_id != 'None':
        try:
            job_title_obj = JobTitle.objects.get(id=job_title_id)
            candidates = candidates.filter(job_title=job_title_obj.id)
        except JobTitle.DoesNotExist:
            candidates = candidates.none()

    # Filter by location
    if location_id and location_id != 'None':
        try:
            location_obj = Location.objects.get(id=location_id)
            candidates = candidates.filter(location=location_obj.id)
        except Location.DoesNotExist:
            candidates = candidates.none()

    # Filter by interviewer
    if interviewer:
        candidates = candidates.filter(interviewer__name__icontains=interviewer)

    # Filter by date range
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            candidates = candidates.filter(interview_date__range=[start_date, end_date])
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")

    # Filter by stage
    if stage:
        candidates = candidates.filter(stage=stage)

    stages = [
        '1-Screening', '2-Interview', '3-Selection', '4-Offer', '5-Joined', '6-Reject', '7-Hold'
    ]

    # Pagination logic
    pagination_count = int(request.GET.get('pagination_count', 10))
    paginator = Paginator(candidates, pagination_count)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Context data for rendering the template
    context = {
        'page_obj': page_obj,
        'pagination_count': pagination_count,
        'job_titles': JobTitle.objects.all(),
        'locations': Location.objects.all(),
        'interviewers': Interviewer.objects.all(),
        'stages': stages,
    }

    return render(request, 'reports_home.html', context)
@login_required
def generate_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    interviewer_id = request.GET.get('interviewer')
    job_title_id = request.GET.get('job_title')
    location_id = request.GET.get('location')
    stage = request.GET.get('stage')

    # Fetch all candidates with related JobTitle, Location, and Interviewer
    candidates = Candidate.objects.select_related('job_title', 'location', 'interviewer').all()

    # Apply filters
    if job_title_id and job_title_id != 'None':
        candidates = candidates.filter(job_title_id=job_title_id)
    if location_id and location_id != 'None':
        candidates = candidates.filter(location_id=location_id)
    if interviewer_id and interviewer_id != 'None':
        candidates = candidates.filter(interviewer_id=interviewer_id)
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            candidates = candidates.filter(interview_date__range=[start_date, end_date])
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
    if stage:
        candidates = candidates.filter(stage=stage)

    # Prepare data for CSV export
    data = {
        'Name': [candidate.name for candidate in candidates],
        'Job Title': [candidate.job_title.name if candidate.job_title else '' for candidate in candidates],
        'Interviewer': [candidate.interviewer.name if candidate.interviewer else '' for candidate in candidates],
        'Location': [candidate.location.name if candidate.location else '' for candidate in candidates],
        'Stage': [candidate.stage for candidate in candidates],
        'Interview Date': [candidate.interview_date.strftime('%Y-%m-%d') if candidate.interview_date else '' for candidate in candidates]
    }

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'
    df.to_csv(path_or_buf=response, index=False)
    return response
@login_required
def download_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    interviewer_id = request.GET.get('interviewer')
    job_title_id = request.GET.get('job_title')
    location_id = request.GET.get('location')
    stage = request.GET.get('stage')

    # Fetch all candidates and include related field names
    candidates_list = Candidate.objects.select_related('job_title', 'location', 'interviewer')

    # Apply filters
    if start_date and end_date:
        candidates_list = candidates_list.filter(interview_date__range=[start_date, end_date])
    if interviewer_id and interviewer_id != 'None':
        candidates_list = candidates_list.filter(interviewer_id=interviewer_id)
    if job_title_id and job_title_id != 'None':
        candidates_list = candidates_list.filter(job_title_id=job_title_id)
    if location_id and location_id != 'None':
        candidates_list = candidates_list.filter(location_id=location_id)
    if stage:
        candidates_list = candidates_list.filter(stage=stage)

    # Prepare data for export with resolved names
    data = [
        {
            'Name': candidate.name,
            'Job Title': candidate.job_title.name if candidate.job_title else 'N/A',
            'Location': candidate.location.name if candidate.location else 'N/A',
            'Interviewer': candidate.interviewer.name if candidate.interviewer else 'N/A',
            'Notice Period': candidate.notice_period,
            'Stage': candidate.stage,
            'Sub Stage': candidate.sub_stage,
            'Source': candidate.source,
            'Position Status': candidate.position_status,
            'Interview Status': candidate.interview_status,
            'Interview Date': candidate.interview_date.strftime('%Y-%m-%d') if candidate.interview_date else '',
        }
        for candidate in candidates_list
    ]

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=filtered_candidates_report.xlsx'
    df.to_excel(response, index=False)
    return response
@login_required
def download_selected(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_candidates')
        stage = request.POST.get('stage')

        # Fetch candidates with related fields included
        candidates_list = Candidate.objects.filter(id__in=selected_ids).select_related('job_title', 'location', 'interviewer')

        if stage:
            candidates_list = candidates_list.filter(stage=stage)

        # Prepare data for export with resolved names
        data = []
        for candidate in candidates_list:
            data.append({
                'Name': candidate.name,
                'Job Title': candidate.job_title.name if candidate.job_title else 'N/A',
                'Location': candidate.location.name if candidate.location else 'N/A',
                'Interviewer': candidate.interviewer.name if candidate.interviewer else 'N/A',
                'Notice Period': candidate.notice_period,
                'Stage': candidate.stage,
                'Sub Stage': candidate.sub_stage,
                'Source': candidate.source,
                'Position Status': candidate.position_status,
                'Interview Status': candidate.interview_status,
                'Interview Date': candidate.interview_date.strftime('%Y-%m-%d') if candidate.interview_date else '',
                'Resume': candidate.resume.url if candidate.resume else 'No Resume',
                'Sourcer': candidate.sourcer,
                'Contact Number': candidate.contact_number,
                'Email ID': candidate.email_id,
                'Current Company': candidate.current_company,
                'Current Position': candidate.current_position,
                'Experience (Years-Months)': candidate.experience_years_months,
                'Relevant Experience': candidate.relevant_experience,
                'Current Salary (LPA)': candidate.current_salary_lpa,
                'Expected Salary (LPA)': candidate.expected_salary_lpa,
                'Other Offers (LPA)': candidate.other_offers_lpa,
                'Last Working Day': candidate.last_working_day,
                'Internal Screening Date': candidate.internal_screening.strftime('%Y-%m-%d') if candidate.internal_screening else '',
                'Interview Date 2': candidate.date_of_interview_2.strftime('%Y-%m-%d') if candidate.date_of_interview_2 else '',
                'Interview Date 3': candidate.date_of_interview_3.strftime('%Y-%m-%d') if candidate.date_of_interview_3 else '',
                'Joined Date': candidate.joined_date.strftime('%Y-%m-%d') if candidate.joined_date else '',
                'Evaluation Link': candidate.evaluation_link,
                'Remarks': candidate.remark,
            })

        # Convert the data into a DataFrame
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=selected_candidates_report.xlsx'
        df.to_excel(response, index=False)
        return response
@login_required
def delete_selected(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_candidates')
        if selected_ids:
            Candidate.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f"Successfully deleted {len(selected_ids)} candidates.")
        else:
            messages.error(request, "No candidates selected for deletion.")
    return redirect('reports_home')
