from django.urls import path
from skillnex import views

app_name = 'skillnex'

urlpatterns = [
    path('', views.Home, name='home'),
    path('our-services/', views.Services, name='service'),
    path('service-details/<slug:slug>/', views.ServiceDetails, name='service-details'),
    path('about-us/', views.AboutUs, name='about'),
    path("our-work/", views.Projects, name="projects"),
    path("project-details/<slug:slug>/", views.ProjectDetails, name="project_details"),
    path('contact-form/', views.Contact, name='contact'),
    path("training/", views.Training, name="training"),
    path("training/<slug:slug>/", views.TrainingCategoryDetails, name="training_category_details"),
    path( "training/course/<slug:slug>/", views.TrainingCourseDetails, name="training_course_detail" ),
    path( "training/course/<slug:slug>/enroll/", views.TrainingEnrollmentCreate, name="training_enrollment" ), 
    path( "training/enrollment/success/<int:pk>/", views.TrainingEnrollmentSuccess, name="training_enrollment_success" ),
    path("blog/", views.Blog, name="blog"), 
    path( "blog/category/<slug:slug>/", views.BlogCategory, name="blog_category" ), 
    path( "blog/tag/<slug:slug>/", views.BlogTag, name="blog_tag" ), 
    path( "blog/<slug:slug>/", views.BlogDetails, name="blog_details" ),
]
