import django

django.setup()

from apps.terminal import models
from apps.first import models as first_models

result = first_models.Result.objects.last()
order = result.order

a: models.Deal = models.Deal.open_first(result=result)
a.close_first()
