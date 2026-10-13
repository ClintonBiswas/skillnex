from django.shortcuts import render, get_object_or_404, redirect
from skillnex import models
from django.contrib import messages
from .services.enrollment_sms import (
    send_admin_enrollment_sms,
    send_student_enrollment_sms,
)
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from .services.contact_email import send_contact_inquiry_email
# Create your views here.
def Home(request):

    service_list = models.Service.objects.filter(
        is_active=True
    )[:2]

    training_categories = models.TrainingCategory.objects.filter(
        is_active=True
    )[:2]

    featured_courses = models.TrainingCourse.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related(
        "category"
    )[:3]
    featured_projects = models.Project.objects.filter( is_active=True, is_featured=True ).order_by("-created_at")[:3]
    featured_reviews = models.Review.objects.filter( is_active=True, is_featured=True, ).select_related( "course", "service", )
    company_history = models.CompanyHistory.objects.first()

    context = {
        "service_list": service_list,
        "training_categories": training_categories,
        "featured_courses": featured_courses,
        "featured_projects": featured_projects,
        "featured_reviews": featured_reviews,
        "company_history": company_history,
        "show_all_services_link": True,
        "show_all_training_link": True,
    }

    return render(
        request,
        "skillnex/home.html",
        context
    )

def Training(request):
    training_categories = models.TrainingCategory.objects.filter(
    is_active=True
    ).prefetch_related("courses")
    instructors = models.TrainingInstructor.objects.filter( is_active=True )

    return render(
        request,
        "skillnex/training.html",
        {
            "training_categories": training_categories,
            "show_all_training_link": False,
            "instructors": instructors,
        }
    )


def TrainingCategoryDetails(request, slug):
    category = get_object_or_404(
    models.TrainingCategory.objects.prefetch_related("courses"),
    slug=slug,
    is_active=True
    )
    courses = category.courses.filter(
        is_active=True
    )

    context = {
        "category": category,
        "courses": courses,
    }

    return render(
        request,
        "skillnex/training_category_details.html",
        context
    )

def TrainingCourseDetails(request, slug):

    course = get_object_or_404(
        models.TrainingCourse.objects
        .select_related("category")
        .prefetch_related(
            "modules__lessons",
            "batches",
        ),
        slug=slug,
        is_active=True
    )

    context = {
        "course": course,
    }

    return render(
        request,
        "skillnex/training_course_details.html",
        context
    )

def Services(request):

    service_list = models.Service.objects.filter(
        is_active=True
    )

    context = {
        "service_list": service_list,
    }

    return render(
        request,
        "skillnex/services.html",
        context
    )
def ServiceDetails(request, slug):
    service_details = get_object_or_404(models.Service, slug=slug, is_active=True)
    context = {'service_details': service_details}
    return render(request, 'skillnex/service_details.html', context)


def AboutUs(request):

    about_page = models.AboutPage.objects.filter(
        is_active=True
    ).prefetch_related(
        "values",
        "achievements"
    ).first()

    context = {
        "about_page": about_page,
    }

    return render(
        request,
        "skillnex/about.html",
        context
    )

def Projects(request):
    projects = models.Project.objects.filter(
    is_active=True
    ).order_by("-created_at")

    return render(
        request,
        "skillnex/projects.html",
        {
            "projects": projects,
        }
    )

def ProjectDetails(request, slug):
    project = get_object_or_404(
    models.Project,
    slug=slug,
    is_active=True,
    )

    return render(
        request,
        "skillnex/project_details.html",
        {
            "project": project,
        },
    )

def Contact(request):

    services = models.Service.objects.filter(
        is_active=True
    ).order_by(
        "order",
        "name"
    )

    training_categories = models.TrainingCategory.objects.filter(
        is_active=True
    ).prefetch_related("courses")

    courses = models.TrainingCourse.objects.filter(
        is_active=True
    ).select_related("category")


    if request.method == "POST":

        errors = {}


        # -----------------------------------------
        # Get submitted data
        # -----------------------------------------

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        inquiry_type = request.POST.get(
            "inquiry_type",
            ""
        ).strip()

        service_id = request.POST.get(
            "service",
            ""
        ).strip()

        course_id = request.POST.get(
            "course",
            ""
        ).strip()

        training_purpose = request.POST.get(
            "training_purpose",
            ""
        ).strip()

        preferred_contact_method = request.POST.get(
            "preferred_contact_method",
            ""
        ).strip()

        message = request.POST.get(
            "message",
            ""
        ).strip()


        # -----------------------------------------
        # Name validation
        # -----------------------------------------

        if not name:

            errors["name"] = (
                "Please enter your full name."
            )

        elif len(name) < 2:

            errors["name"] = (
                "Your name must contain at least 2 characters."
            )

        elif len(name) > 150:

            errors["name"] = (
                "Your name is too long."
            )


        # -----------------------------------------
        # Email validation
        # -----------------------------------------

        if not email:

            errors["email"] = (
                "Email address is required."
            )

        else:

            try:

                validate_email(email)

            except ValidationError:

                errors["email"] = (
                    "Please enter a valid email address."
                )


        # -----------------------------------------
        # Phone validation
        # -----------------------------------------

        if not phone:

            errors["phone"] = (
                "Please enter your phone or WhatsApp number."
            )

        elif len(phone) < 7:

            errors["phone"] = (
                "Please enter a valid phone number."
            )

        elif len(phone) > 30:

            errors["phone"] = (
                "Phone number is too long."
            )


        # -----------------------------------------
        # Inquiry type validation
        # -----------------------------------------

        valid_inquiry_types = {
            choice[0]
            for choice in models.ContactInquiry.INQUIRY_TYPES
        }

        if inquiry_type not in valid_inquiry_types:

            errors["inquiry_type"] = (
                "Please select what you are looking for."
            )


        # -----------------------------------------
        # Message validation
        # -----------------------------------------

        if not message:

            errors["message"] = (
                "Please tell us a little about your requirement."
            )

        elif len(message) < 10:

            errors["message"] = (
                "Please provide a little more detail "
                "so we can understand your requirement."
            )

        elif len(message) > 5000:

            errors["message"] = (
                "Your message is too long. "
                "Please keep it under 5000 characters."
            )


        # -----------------------------------------
        # Training purpose validation
        # -----------------------------------------

        valid_training_purposes = {
            choice[0]
            for choice in models.ContactInquiry.TRAINING_PURPOSES
        }

        if (
            inquiry_type == "training"
            and training_purpose
            and training_purpose not in valid_training_purposes
        ):

            errors["training_purpose"] = (
                "Please select a valid training purpose."
            )


        # -----------------------------------------
        # Contact method validation
        # -----------------------------------------

        valid_contact_methods = {
            choice[0]
            for choice in models.ContactInquiry.CONTACT_METHODS
        }

        if (
            preferred_contact_method
            and preferred_contact_method not in valid_contact_methods
        ):

            errors["preferred_contact_method"] = (
                "Please select a valid contact method."
            )


        # -----------------------------------------
        # Return validation errors
        # -----------------------------------------

        if errors:

            return JsonResponse(
                {
                    "success": False,
                    "errors": errors,
                },
                status=400
            )


        # -----------------------------------------
        # Get selected service
        # -----------------------------------------

        service = None

        if (
            inquiry_type == "service"
            and service_id
            and service_id != "consultation"
        ):

            service = get_object_or_404(
                models.Service,
                id=service_id,
                is_active=True
            )


        # -----------------------------------------
        # Get selected course
        # -----------------------------------------

        course = None

        if inquiry_type == "training" and course_id:

            course = get_object_or_404(
                models.TrainingCourse,
                id=course_id,
                is_active=True
            )


        # -----------------------------------------
        # Save inquiry
        # -----------------------------------------

        inquiry = models.ContactInquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            inquiry_type=inquiry_type,
            service=service,
            course=course,
            training_purpose=(
                training_purpose
                if inquiry_type == "training"
                else ""
            ),
            preferred_contact_method=preferred_contact_method,
            message=message,
        )
        print("CONTACT INQUIRY CREATED:")
        print("ID:", inquiry.id)
        print("NAME:", inquiry.name)
        print("EMAIL:", inquiry.email)


        # -----------------------------------------
        # Send notification email
        # -----------------------------------------

        try:

            send_contact_inquiry_email(
                inquiry
            )

        except Exception as exc:

            print(
                "CONTACT EMAIL ERROR:",
                repr(exc)
            )


        # -----------------------------------------
        # AJAX success response
        # -----------------------------------------

        return JsonResponse(
            {
                "success": True,
                "message": (
                    "Thank you! Your inquiry has been "
                    "submitted successfully. "
                    "Our team will contact you soon."
                ),
            }
        )


    context = {
        "services": services,
        "training_categories": training_categories,
        "courses": courses,
    }

    return render(
        request,
        "skillnex/contact.html",
        context
    )
def TrainingEnrollmentCreate(request, slug):

    course = get_object_or_404(
        models.TrainingCourse.objects
        .select_related("category")
        .prefetch_related("batches"),
        slug=slug,
        is_active=True
    )

    batches = course.batches.filter(
        is_active=True
    ).order_by("start_date")

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        batch_id = request.POST.get("batch", "").strip()
        message = request.POST.get("message", "").strip()

        if not name:

            messages.error(
                request,
                "Please enter your name."
            )

        elif not phone:

            messages.error(
                request,
                "Please enter your phone or WhatsApp number."
            )

        else:

            batch = None

            if batch_id:

                batch = get_object_or_404(
                    models.TrainingBatch,
                    id=batch_id,
                    course=course,
                    is_active=True
                )

            enrollment = models.TrainingEnrollment.objects.create(
                name=name,
                email=email,
                phone=phone,
                course=course,
                batch=batch,
                payment_method="offline",
                status="pending",
                message=message,
            )

            print("\n")
            print("======================================")
            print("NEW ENROLLMENT CREATED")
            print("ID:", enrollment.id)
            print("Student:", enrollment.name)
            print("Phone:", enrollment.phone)
            print("Course:", enrollment.course.name)
            print("======================================")

            try:

                from .services.enrollment_sms import (
                    send_student_enrollment_sms,
                    send_admin_enrollment_sms,
                )

                # Student SMS
                student_result = send_student_enrollment_sms(
                    enrollment
                )

                print(
                    "STUDENT SMS RESULT:",
                    student_result
                )

                # Admin SMS
                admin_result = send_admin_enrollment_sms(
                    enrollment
                )

                print(
                    "ADMIN SMS RESULT:",
                    admin_result
                )

            except Exception as exc:

                print(
                    "SMS SYSTEM ERROR:",
                    repr(exc)
                )

            return redirect(
                "skillnex:training_enrollment_success",
                pk=enrollment.pk
            )

    return render(
        request,
        "skillnex/training_enrollment.html",
        {
            "course": course,
            "batches": batches,
        }
    )


def TrainingEnrollmentSuccess(request, pk):

    enrollment = get_object_or_404(
        models.TrainingEnrollment.objects
        .select_related("course", "batch"),
        pk=pk
    )

    return render(
        request,
        "skillnex/training_enrollment_success.html",
        {
            "enrollment": enrollment,
        }
    )

### Blog Views Here

def Blog(request):
    featured_post = (
        models.BlogPost.objects
        .filter(
            is_published=True,
            is_featured=True,
        )
        .select_related("category")
        .prefetch_related("tags")
        .first()
    )

    posts = (
        models.BlogPost.objects
        .filter(
            is_published=True,
        )
        .select_related("category")
        .prefetch_related("tags")
    )

    if featured_post:
        posts = posts.exclude(pk=featured_post.pk)

    categories = models.BlogCategory.objects.filter(
        is_active=True
    )

    tags = models.BlogTag.objects.all()

    context = {
        "featured_post": featured_post,
        "posts": posts,
        "categories": categories,
        "tags": tags,
    }

    return render(
        request,
        "skillnex/blog.html",
        context
    )


def BlogCategory(request, slug):
    category = get_object_or_404(
        models.BlogCategory,
        slug=slug,
        is_active=True,
    )

    posts = (
        models.BlogPost.objects
        .filter(
            category=category,
            is_published=True,
        )
        .select_related("category")
        .prefetch_related("tags")
    )

    categories = models.BlogCategory.objects.filter(
        is_active=True
    )

    return render(
        request,
        "skillnex/blog.html",
        {
            "category": category,
            "posts": posts,
            "categories": categories,
        }
    )

def BlogTag(request, slug):
    tag = get_object_or_404(
        models.BlogTag,
        slug=slug,
    )

    posts = (
        models.BlogPost.objects
        .filter(
            tags=tag,
            is_published=True,
        )
        .select_related("category")
        .prefetch_related("tags")
    )

    categories = models.BlogCategory.objects.filter(
        is_active=True
    )

    return render(
        request,
        "skillnex/blog.html",
        {
            "tag": tag,
            "posts": posts,
            "categories": categories,
        }
    )

def BlogDetails(request, slug):
    post = get_object_or_404(
        models.BlogPost.objects
        .select_related("category")
        .prefetch_related("tags"),
        slug=slug,
        is_published=True,
    )

    related_posts = (
        models.BlogPost.objects
        .filter(
            category=post.category,
            is_published=True,
        )
        .exclude(pk=post.pk)
        .select_related("category")
        .prefetch_related("tags")[:3]
    )

    return render(
        request,
        "skillnex/blog_details.html",
        {
            "post": post,
            "related_posts": related_posts,
        }
    )