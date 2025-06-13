from django.db import models

class Scheme(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    # Geographic methods without database fields
    def get_coordinates(self):
        """Returns (longitude, latitude) for Leaflet maps"""
        state_coords = {
            'AP': (83.2185, 17.6868), 'AR': (93.6167, 27.1004), 'AS': (92.9376, 26.2006),
            'BR': (85.3131, 25.0961), 'CT': (81.8661, 21.2787), 'GA': (74.1240, 15.2993),
            'GJ': (71.1924, 22.2587), 'HR': (76.0856, 29.0588), 'HP': (77.1734, 31.1048),
            'JH': (85.2799, 23.6102), 'KA': (75.7139, 15.3173), 'KL': (76.2711, 10.8505),
            'MP': (78.6569, 22.9734), 'MH': (75.7139, 19.7515), 'MN': (93.9063, 24.6637),
            'ML': (91.3662, 25.4670), 'MZ': (92.9376, 23.1645), 'NL': (93.9511, 25.7999),
            'OR': (85.0985, 20.9517), 'PB': (75.3412, 31.1471), 'RJ': (74.2179, 27.0238),
            'SK': (88.6167, 27.3333), 'TN': (78.6569, 11.1271), 'TG': (79.0193, 18.1124),
            'TR': (91.9882, 23.9408), 'UP': (80.9462, 26.8467), 'UT': (79.0193, 30.0668),
            'WB': (87.8550, 22.9868)
        }
        return state_coords.get(self.code, (78.9629, 20.5937))  # Default: India center
    
    def total_beneficiaries(self):
        """Calculates total beneficiaries without DB field"""
        from django.db.models import Sum
        return self.schemadata_set.aggregate(
            total=Sum('beneficiaries')
        )['total'] or 0
    
    def active_schemes_count(self):
        """Counts schemes without DB field"""
        return self.schemadata_set.count()

class SchemeData(models.Model):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE, related_name='scheme_data')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='scheme_data')  
    beneficiaries = models.IntegerField()
    year = models.IntegerField()
    
    class Meta:
        unique_together = ('scheme', 'state', 'year')
    
    def __str__(self):
        return f"{self.scheme} in {self.state} ({self.year})"