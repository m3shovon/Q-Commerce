from import_export import resources
from App_Cloud import models

class FoodItemResource(resources.ModelResource):
    class Meta:
        model = models.FoodItem
        fields = ['restaurant', 'title', 'price']