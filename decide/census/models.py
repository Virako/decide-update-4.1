from django.db import models


class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['voting_id', 'voter_id'], name='unique_voting_voter'),
        ]
