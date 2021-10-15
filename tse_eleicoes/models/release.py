import uuid
from django.db import models
from psqlextra.models import PostgresModel


class Release(PostgresModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    year = models.IntegerField(unique=True)
    finished = models.BooleanField(default=False)
    folder = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['finished']),
        ]


class Type(models.IntegerChoices):
    PARTY_MEMBER = 0
    DELEGATE = 1
    CANDIDATE = 2
    REMOVAL = 3


class Download(PostgresModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    type = models.IntegerField(choices=Type.choices)
    uri = models.URLField()

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['finished']),
            models.Index(fields=['type']),
        ]
        constraints = [
            models.UniqueConstraint(
                name='unique_tse_eleicoes_download',
                fields=['release', 'type', 'uri'],
            ),
        ]


class Insert(PostgresModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    type = models.IntegerField(choices=Type.choices)
    finished = models.BooleanField(default=False)
    file = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['finished']),
            models.Index(fields=['type']),
        ]
