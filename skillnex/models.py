from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

class CompanyHistory(models.Model):
    project_complete = models.IntegerField()
    happy_clients = models.IntegerField()
    years_of_experience = models.IntegerField()
    client_satisfication = models.IntegerField()

    def __str__(self):
        return f"Skillnex - {self.project_complete}"
    
class Service(models.Model):
    name = models.CharField(max_length=150)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    short_description = models.TextField()

    description = models.TextField(
        blank=True,
        help_text="Main description shown on the service detail page."
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Font Awesome class, e.g. fa-solid fa-code"
    )

    image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "skillnex:service-details",
            kwargs={"slug": self.slug}
        )


class ServiceFeature(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="features"
    )

    title = models.CharField(max_length=150)

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Font Awesome class"
    )

    description = models.CharField(
        max_length=255,
        blank=True
    )

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

class ServiceHighlight(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="highlights"
    )

    title = models.CharField(max_length=100)

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Font Awesome class"
    )

    short_text = models.CharField(
        max_length=200,
        blank=True
    )

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class AboutPage(models.Model):
    # Hero / Introduction
    eyebrow = models.CharField(
        max_length=100,
        default="About Skillnex"
    )

    title = models.CharField(
        max_length=200,
        default="Empowering Businesses Through Digital Solutions"
    )

    short_description = models.TextField(
        help_text="Short introduction shown in the About page hero section."
    )

    description = models.TextField(
        help_text="Main company description shown in the About page."
    )

    image = models.ImageField(
        upload_to="about/",
        blank=True,
        null=True
    )

    # Mission & Vision
    mission_title = models.CharField(
        max_length=150,
        default="Our Mission"
    )

    mission = models.TextField(
        blank=True
    )

    vision_title = models.CharField(
        max_length=150,
        default="Our Vision"
    )

    vision = models.TextField(
        blank=True
    )

    # Why choose us
    why_title = models.CharField(
        max_length=200,
        default="Why Choose Skillnex?"
    )

    why_description = models.TextField(
        blank=True
    )

    # Status
    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

    def __str__(self):
        return self.title


class AboutValue(models.Model):
    about_page = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name="values"
    )

    title = models.CharField(
        max_length=150
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Font Awesome class, e.g. fa-solid fa-bullseye"
    )

    description = models.CharField(
        max_length=255
    )

    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class AboutAchievement(models.Model):
    about_page = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name="achievements"
    )

    number = models.CharField(
        max_length=50,
        help_text="Example: 100+ or 5+"
    )

    label = models.CharField(
        max_length=100
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Font Awesome class"
    )

    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.number} {self.label}"

#### Training sections
class TrainingCategory(models.Model):

    name = models.CharField(
        max_length=150
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    short_description = models.CharField(
        max_length=255,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Font Awesome class"
    )

    image = models.ImageField(
        upload_to="training/categories/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse(
            "skillnex:training_category_details",
            kwargs={"slug": self.slug}
        )

class TrainingCourse(models.Model):

    category = models.ForeignKey(
        TrainingCategory,
        on_delete=models.PROTECT,
        related_name="courses"
    )

    name = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    short_description = models.CharField(
        max_length=300
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="training/courses/",
        blank=True,
        null=True
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Font Awesome class"
    )

    duration = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: 3 Months"
    )

    total_classes = models.PositiveIntegerField(
        default=0
    )

    level = models.CharField(
        max_length=50,
        choices=[
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
            ("advanced", "Advanced"),
        ],
        default="beginner"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "skillnex:training_course_detail",
            kwargs={"slug": self.slug}
        )

class CourseModule(models.Model):

    course = models.ForeignKey(
        TrainingCourse,
        on_delete=models.CASCADE,
        related_name="modules"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.name} - {self.title}"

class CourseLesson(models.Model):

    module = models.ForeignKey(
        CourseModule,
        on_delete=models.CASCADE,
        related_name="lessons"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    duration = models.PositiveIntegerField(
        default=0,
        help_text="Duration in minutes"
    )

    order = models.PositiveIntegerField(
        default=0
    )

    is_preview = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class TrainingInstructor(models.Model):

    name = models.CharField(
        max_length=150
    )

    designation = models.CharField(
        max_length=150,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="training/instructors/",
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

class TrainingBatch(models.Model):

    course = models.ForeignKey(
        TrainingCourse,
        on_delete=models.PROTECT,
        related_name="batches"
    )
    instructor = models.ForeignKey(
        TrainingInstructor,
        on_delete=models.PROTECT,
        related_name="batches",
        blank=True,
        null=True
    )

    name = models.CharField(
        max_length=100,
        help_text="Example: Web Design Batch 01"
    )

    start_date = models.DateField()

    end_date = models.DateField(
        blank=True,
        null=True
    )

    class_schedule = models.CharField(
        max_length=200,
        blank=True,
        help_text="Example: Sat, Mon & Wed — 7:00 PM"
    )

    max_students = models.PositiveIntegerField(
        default=20
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.course.name} - {self.name}"

class Project(models.Model):

    CATEGORY_CHOICES = [
        ("website", "Website"),
        ("ecommerce", "E-Commerce"),
        ("web_app", "Web Application"),
        ("branding", "Branding"),
        ("digital_marketing", "Digital Marketing"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=200)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    short_description = models.CharField(
        max_length=300
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="projects/"
    )

    client_name = models.CharField(
        max_length=150,
        blank=True
    )

    project_url = models.URLField(
        blank=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def get_absolute_url(self): 
        return reverse( "skillnex:project_details", kwargs={"slug": self.slug} )


class ContactInquiry(models.Model):

    INQUIRY_TYPES = [
        ("training", "Training"),
        ("service", "Service"),
        ("general", "General"),
    ]

    CONTACT_METHODS = [
        ("whatsapp", "WhatsApp"),
        ("phone", "Phone Call"),
        ("email", "Email"),
    ]

    TRAINING_PURPOSES = [
        ("course_details", "Course Details"),
        ("fee", "Course Fee"),
        ("next_batch", "Next Batch"),
        ("schedule", "Class Schedule"),
        ("career", "Career Guidance"),
        ("help_choose", "Help Me Choose a Course"),
    ]

    name = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30
    )

    inquiry_type = models.CharField(
        max_length=20,
        choices=INQUIRY_TYPES
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inquiries"
    )

    course = models.ForeignKey(
        TrainingCourse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inquiries"
    )

    training_purpose = models.CharField(
        max_length=30,
        choices=TRAINING_PURPOSES,
        blank=True
    )

    preferred_contact_method = models.CharField(
        max_length=20,
        choices=CONTACT_METHODS,
        blank=True
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.name} - {self.phone}"

class TrainingEnrollment(models.Model):

    PAYMENT_METHODS = [
        ("offline", "Offline Payment"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("contacted", "Contacted"),
        ("payment_pending", "Payment Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    name = models.CharField(max_length=150)

    email = models.EmailField(blank=True)

    phone = models.CharField(max_length=30)

    course = models.ForeignKey(
        TrainingCourse,
        on_delete=models.PROTECT,
        related_name="enrollments"
    )

    batch = models.ForeignKey(
        TrainingBatch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="enrollments"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default="offline",
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="pending"
    )

    message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.course.name}"


class SMSSettings(models.Model):

    admin_phone = models.CharField(
        max_length=30,
        default="01628768066",
        help_text="Phone number that receives Skillnex admin SMS notifications."
    )

    is_active = models.BooleanField(
        default=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "SMS Settings"
        verbose_name_plural = "SMS Settings"

    def __str__(self):
        return "SMS Settings"

class Review(models.Model):

    REVIEW_TYPE_CHOICES = [
        ("student", "Student Review"),
        ("service", "Service Review"),
    ]

    name = models.CharField(max_length=150)

    review_type = models.CharField(
        max_length=20,
        choices=REVIEW_TYPE_CHOICES,
    )

    designation = models.CharField(
        max_length=150,
        blank=True,
        help_text="Example: Student, Business Owner, CEO, etc."
    )

    course = models.ForeignKey(
        "TrainingCourse",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )

    service = models.ForeignKey(
        "Service",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )

    photo = models.ImageField(
        upload_to="reviews/",
        blank=True,
        null=True,
    )

    rating = models.PositiveSmallIntegerField(
        default=5,
    )

    review = models.TextField()

    is_featured = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.name} - {self.get_review_type_display()}"


class SiteSettings(models.Model):
    company_name = models.CharField(
        max_length=150,
        default="Skillnex IT Academy"
    )
    logo = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True
    )
    favicon = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True
    )
    short_description = models.TextField(
        blank=True
    )

    email = models.EmailField(
        blank=True
    )
    phone = models.CharField(
        max_length=30,
        blank=True
    )
    whatsapp = models.CharField(
        max_length=30,
        blank=True
    )
    address = models.TextField(
        blank=True
    )
    facebook_url = models.URLField(
        blank=True
    )
    instagram_url = models.URLField(
        blank=True
    )
    linkedin_url = models.URLField(
        blank=True
    )
    youtube_url = models.URLField(
        blank=True
    )
    is_active = models.BooleanField(
        default=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
        
    def __str__(self):
        return self.company_name

#### Blog Models Here
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "skillnex:blog_category",
            kwargs={"slug": self.slug}
        )

class BlogTag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "skillnex:blog_tag",
            kwargs={"slug": self.slug}
        )

class BlogPost(models.Model):

    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.PROTECT,
        related_name="posts"
    )

    tags = models.ManyToManyField(
        BlogTag,
        blank=True,
        related_name="posts"
    )

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        unique=True,
        blank=True,
        max_length=200
    )

    excerpt = models.CharField(
        max_length=300
    )

    content = models.TextField()

    featured_image = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True
    )

    author = models.CharField(
        max_length=100,
        blank=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_published = models.BooleanField(
        default=True
    )

    published_at = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "skillnex:blog_details",
            kwargs={"slug": self.slug}
        )