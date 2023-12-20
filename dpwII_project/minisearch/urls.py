from django.urls import path 
from minisearch.views import views
from minisearch.views import result

app_name = 'minisearch'

urlpatterns = [
    # add urls of main page.
    #path('', views.index, name='header_view'),  
    path('', views.index, name = 'header_view'),
    #path('search/', views.search_index, name='search_view'), 
    # path means all type of data is allowed.
    # str allows all data except '/'.
    path('result', result.sql_result, name='result_view'),
    
]
