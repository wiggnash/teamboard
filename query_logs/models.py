from django.db import models

class QueryLog(models.Model):
    company       = models.ForeignKey(
                        'companies.Company',
                        on_delete=models.CASCADE,
                        related_name='query_logs'
                    )
    search_term   = models.CharField(max_length=255)
    results_count = models.IntegerField()  # how many KB entries matched
    queried_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-queried_at']

    def __str__(self):
        return f'{self.company_id}: "{self.search_term}" ({self.results_count})'
