import uuid
from django.db import models
from users.models import User
from jobs.models import JobPosting
from resumes.models import Resume

class ApplicationStatus(models.TextChoices):
    APPLIED       = 'applied',       'Applied'
    REVIEWED      = 'reviewed',      'Reviewed'
    SHORTLISTED   = 'shortlisted',   'Shortlisted'
    INTERVIEW     = 'interview',     'Interview'
    OFFER         = 'offer',         'Offer Extended'
    REJECTED      = 'rejected',      'Rejected'
    WITHDRAWN     = 'withdrawn',     'Withdrawn'   

class JobApplication(models.Model):
    STATUS_CHOICES = ApplicationStatus.choices
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    job = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    resume_version = models.ForeignKey(
        Resume,
        on_delete=models.SET_NULL,
        null=True,
        related_name='applications'
    )
    resume_snapshot = models.JSONField(default=dict)
    cover_letter = models.TextField(blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=ApplicationStatus.APPLIED
    )

    ats_score = models.FloatField(null=True, blank=True)
    match_score = models.FloatField(null=True, blank=True)
    ai_summary = models.TextField(blank=True)
    recruiter_notes = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    feedback = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('applicant', 'job')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.applicant.email} → {self.job.title}"

class ApplicationStatusHistory(models.Model):
    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name='status_history'
    )
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='status_changes_made'
    )
    changed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['changed_at']

    def __str__(self):
        return f"{self.old_status} → {self.new_status} ({self.changed_at})"