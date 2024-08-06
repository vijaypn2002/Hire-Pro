from django.contrib.auth.decorators import login_required
from django.urls import path
from django.urls import include
from django.urls import path
from .views import login  # Make sure to import the login view
from .views import (
    login, home, add_candidate, candidate_detail, candidate_edit, candidate_delete, 
    interviewers_list, interviewer_candidates, download_candidates_excel, view_360, 
    search_candidate, candidate_submission, view_submissions, job_dashboard, 
    add_job_opening, edit_job_opening, delete_job_opening, reports_home, 
    generate_report, download_report, download_selected, export_submissions,
    delete_submissions, administrator, job_position_update, job_position_delete, 
    location_update, location_delete, interview_stage_update, interview_stage_delete,
    sub_stage_update, sub_stage_delete, interviewer_update, interviewer_delete,delete_selected,custom_login
)


urlpatterns = [
       path('', custom_login, name='login_redirect'),
    path('login/', custom_login, name='login'),

    # Apply login_required to all views in these URL patterns
    path('home/', login_required(home), name='home'),
    path('add/', login_required(add_candidate), name='add_candidate'),
    path('<int:candidate_id>/', login_required(candidate_detail), name='candidate_detail'),
    path('<int:candidate_id>/edit/', login_required(candidate_edit), name='candidate_edit'),
    path('<int:candidate_id>/delete/', login_required(candidate_delete), name='candidate_delete'),
    
    path('interviewers/', login_required(interviewers_list), name='interviewers_list'),
    path('interviewers/<str:interviewer>/', login_required(interviewer_candidates), name='interviewer_candidates'),
    path('download_candidates_excel/', login_required(download_candidates_excel), name='download_candidates_excel'),

    path('view-360/', login_required(view_360), name='view_360'),
    path('search_candidate/', login_required(search_candidate), name='search_candidate'),
    path('submit/', (candidate_submission), name='candidate_submission'),

    path('view_submissions/', login_required(view_submissions), name='view_submissions'),
    path('export_submissions/', login_required(export_submissions), name='export_submissions'),
    path('delete_submissions/', login_required(delete_submissions), name='delete_submissions'),

    path('job-dashboard/', login_required(job_dashboard), name='job_dashboard'),
    path('add-job-opening/', login_required(add_job_opening), name='add_job_opening'),
    path('edit-job-opening/<int:pk>/', login_required(edit_job_opening), name='edit_job_opening'),
    path('delete-job-opening/<int:pk>/', login_required(delete_job_opening), name='delete_job_opening'),

    path('reports/', login_required(reports_home), name='reports_home'),
    path('generate_report/', login_required(generate_report), name='generate_report'),
    path('download_report/', login_required(download_report), name='download_report'),
    path('download_selected/', login_required(download_selected), name='download_selected'),

    path('administrator/', login_required(administrator), name='administrator'),
    path('job_position/update/<int:pk>/', login_required(job_position_update), name='job_position_update'),
    path('job_position/delete/<int:pk>/', login_required(job_position_delete), name='job_position_delete'),
    path('location/update/<int:pk>/', login_required(location_update), name='location_update'),
    path('location/delete/<int:pk>/', login_required(location_delete), name='location_delete'),
    path('interview_stage/update/<int:pk>/', login_required(interview_stage_update), name='interview_stage_update'),
    path('interview_stage/delete/<int:pk>/', login_required(interview_stage_delete), name='interview_stage_delete'),
    path('sub_stage/update/<int:pk>/', login_required(sub_stage_update), name='sub_stage_update'),
    path('sub_stage/delete/<int:pk>/', login_required(sub_stage_delete), name='sub_stage_delete'),
    path('interviewer/update/<int:pk>/', login_required(interviewer_update), name='interviewer_update'),
    path('interviewer/delete/<int:pk>/', login_required(interviewer_delete), name='interviewer_delete'),

    path('delete-selected/', login_required(delete_selected), name='delete_selected'),
]
