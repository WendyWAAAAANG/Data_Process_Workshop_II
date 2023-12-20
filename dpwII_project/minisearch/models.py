from django.db import models

#Create your models here.
class BookTFIDF(models.Model):
    term = models.CharField(max_length = 40)
    fileName = models.CharField(max_length = 10)
    TFIDF = models.FloatField()
    #rowNum = models.IntegerField()
    class Meta:
        #unique_together = ["term", "fileName"]
        managed = True
        db_table = 'booktfidf'
        constraints = [models.UniqueConstraint(fields=["term", "fileName"], name = 'unique_token')]

# class BookTFIDFScore(models.Model):
#     Term = models.TextField(primary_key = True)
#     FileName = models.TextField()
#     TFIDF = models.FloatField()
#     RowNum = models.IntegerField()
#     class Meta:
#         db_table = 'books_tfidf'
#         constraints = [models.UniqueConstraint(fields=["Term", "FileName"], name = 'unique_token')]
#         #unique_together = ["Term", "FileName"]
    

# class BookIndex(models.Model):
#     _1 = models.TextField()
#     _2 = models.TextField()
#     _3 = models.FloatField()