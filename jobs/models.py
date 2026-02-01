import uuid
from django.db import models
from users.models import User
# Create your models here.

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null = True)
    description = models.CharField(blank=True)
    industry = models.CharField(max_length=100, blank = True)
    founded_year = models.PositiveSmallIntegerField(null = True, blank=True)
    employee_count = models.PositiveSmallIntegerField(null = True, blank=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='companies_created'
    )

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Companies'
    
    def __str__(self):
        return self.name
    

class JobStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    ACTIVE = 'active', 'Active'
    CLOSED = 'closed', 'Closed'
    FILLED = 'filled', 'Filled'

class ExperienceLevel(models.TextChoices):
    ENTRY = 'entry', 'Entry'
    MID = 'mid', 'Mid'
    SENIOR = 'senior', 'Senior'
    LEAD = 'lead', 'Lead'
    EXECUTIVE = 'executive', 'Executive'

class EmploymentType(models.TextChoices):
    FULL_TIME   = 'full_time',   'Full Time'
    PART_TIME   = 'part_time',   'Part Time'
    CONTRACT    = 'contract',    'Contract'
    INTERNSHIP  = 'internship',  'Internship'
    REMOTE      = 'remote',      'Remote'

class JobPosting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        related_name = 'job_postings'
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=JobStatus.choices,
        default=JobStatus.DRAFT
    )
    experience_level = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.ENTRY
    )
    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices,
        default=EmploymentType.FULL_TIME
    )
    location = models.CharField(max_length=200, blank=True)
    is_remote = models.BooleanField(default=False)
    salary_min = models.PositiveIntegerField(null=True, blank=True)
    salary_max = models.PositiveIntegerField(null=True, blank=True)
    salary_currency = models.CharField(max_length=3, default='USD')
    required_skills = models.JSONField(default=list, blank=True)
    preferred_skills = models.JSONField(default=list, blank=True)
    education_required = models.CharField(max_length=100, blank=True)
    max_applications = models.PositiveIntegerField(null=True, blank=True)
    application_deadline = models.DateTimeField(null=True, blank=True)
    posted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_postings'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    @property
    def is_accepting_applications(self):
        """Check if this job is still open for applications."""
        if self.status != JobStatus.ACTIVE:
            return False
        if self.application_deadline and self.application_deadline < __import__('django.utils.timezone', fromlist=['now']).now():
            return False
        return True