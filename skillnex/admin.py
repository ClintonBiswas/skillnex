from django.contrib import admin

from skillnex.models import (
    Service,
    ServiceFeature,
    ServiceHighlight,
    CompanyHistory,
    AboutPage,
    AboutAchievement,
    AboutValue,
    CourseModule,
    TrainingCategory,
    TrainingInstructor,
    CourseLesson,
    TrainingCourse,
    TrainingBatch,
    Project,
    ContactInquiry,
    TrainingEnrollment,
    SMSSettings,
    Review,
    SiteSettings,
    BlogCategory,
    BlogPost,
    BlogTag,
)

from .services.enrollment_sms import send_enrollment_status_sms


# Register your models here.
admin.site.register(Service)
admin.site.register(ServiceFeature)
admin.site.register(ServiceHighlight)
admin.site.register(CompanyHistory)
admin.site.register(AboutPage)
admin.site.register(AboutAchievement)
admin.site.register(AboutValue)
admin.site.register(TrainingCategory)
admin.site.register(CourseModule)
admin.site.register(TrainingInstructor)
admin.site.register(CourseLesson)
admin.site.register(TrainingCourse)
admin.site.register(TrainingBatch)
admin.site.register(Project)
admin.site.register(BlogTag)
admin.site.register(BlogPost)
admin.site.register(BlogCategory)


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "email",
        "inquiry_type",
        "service",
        "course",
        "created_at",
    )

    list_filter = (
        "inquiry_type",
        "created_at",
        "service",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "message",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )


@admin.register(TrainingEnrollment)
class TrainingEnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "course",
        "batch",
        "payment_method",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
        "course",
        "batch",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
        "course__name",
        "message",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    def save_model(self, request, obj, form, change):

        old_status = None

        # Get the previous status before saving
        if change and obj.pk:
            old_enrollment = TrainingEnrollment.objects.get(
                pk=obj.pk
            )
            old_status = old_enrollment.status

        # Save the enrollment
        super().save_model(
            request,
            obj,
            form,
            change
        )

        # Send SMS only when status has changed
        if change and old_status != obj.status:

            print("\n======================================")
            print("ENROLLMENT STATUS CHANGED")
            print("Enrollment ID:", obj.id)
            print("Student:", obj.name)
            print("Phone:", obj.phone)
            print("Old status:", old_status)
            print("New status:", obj.status)
            print("======================================")

            try:

                result = send_enrollment_status_sms(obj)

                print(
                    "STATUS SMS RESULT:",
                    result
                )

            except Exception as exc:

                print(
                    "STATUS SMS ERROR:",
                    repr(exc)
                )


@admin.register(SMSSettings)
class SMSSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "admin_phone",
        "is_active",
        "updated_at",
    )

    readonly_fields = (
        "updated_at",
    )

    def has_add_permission(self, request):

        if SMSSettings.objects.exists():
            return False

        return super().has_add_permission(request)
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "review_type",
        "rating",
        "course",
        "service",
        "is_featured",
        "is_active",
        "order",
        "created_at",
    )

    list_filter = (
        "review_type",
        "rating",
        "is_featured",
        "is_active",
        "course",
        "service",
    )

    search_fields = (
        "name",
        "designation",
        "review",
        "course__name",
        "service__name",
    )

    list_editable = (
        "is_featured",
        "is_active",
        "order",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "order",
        "-created_at",
    )

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    fieldsets = (
        (
            "Brand",
            {
                "fields": (
                    "company_name",
                    "logo",
                    "favicon",
                    "short_description",
                )
            },
        ),
        (
            "Contact",
            {
                "fields": (
                    "email",
                    "phone",
                    "whatsapp",
                    "address",
                )
            },
        ),
        (
            "Social Media",
            {
                "fields": (
                    "facebook_url",
                    "instagram_url",
                    "linkedin_url",
                    "youtube_url",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "is_active",
                    "updated_at",
                )
            },
        ),
    )

    readonly_fields = (
        "updated_at",
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()