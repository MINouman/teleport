import uuid
from django.db import models
from users.models import User

# Create your models here.
class CareerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='career_profiles'
    )
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} — {self.title}"
    
class ResumeFormat(models.TextChoices):
    STANDARD = 'standard', 'Standard Template'
    LATEX    = 'latex',    'LaTeX Custom'
    UPLOAD   = 'upload',   'Uploaded File'


class Resume(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    profile = models.ForeignKey(
        CareerProfile,
        on_delete=models.CASCADE,
        related_name='resumes'
    )

    version_label = models.CharField(max_length=100, blank=True)

    format_type = models.CharField(
        max_length=20,
        choices=ResumeFormat.choices,
        default=ResumeFormat.STANDARD
    )

    content = models.JSONField(default=dict, blank=True)
    latex_source = models.TextField(blank=True)
    uploaded_file = models.FileField(upload_to='resumes/uploads/', blank=True, null=True)
    generated_pdf = models.FileField(upload_to='resumes/generated/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    file = models.FileField(upload_to='resumes/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Resume v({self.version_label}) — {self.profile.title}"

class SectionType(models.TextChoices):
    EXPERIENCE     = 'experience',     'Work Experience'
    EDUCATION      = 'education',      'Education'
    SKILLS         = 'skills',         'Skills'
    CERTIFICATIONS = 'certifications', 'Certifications'
    PROJECTS       = 'projects',       'Projects'


class ResumeSection(models.Model):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='sections'
    )
    section_type = models.CharField(
        max_length=30,
        choices=SectionType.choices
    )
    content = models.JSONField(default=dict)

    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.section_type} in {self.resume}"