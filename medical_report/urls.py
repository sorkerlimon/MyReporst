from django.urls import path
from .views import *


urlpatterns = [
    path('dashboard/',dashboard,name='dashboard'),
    path('developer/',developer,name='developer'),
    path('analysis/',analysis,name='analysis'),
    path('addImage/',addImage,name='addImage'),
    
    path('faq/',faq,name='faq'),
    path('contact/',contact,name='contact'),

    path('bloodAnalysis/',bloodAnalysis,name='bloodAnalysis'),
    path('cbc_/',cbc_,name='cbc_'),
    path('esr_/',esr_,name='esr_'),
    path('hba1c_/',hba1c_,name='hba1c_'),
    
    path('urinAnalysis/',urinAnalysis,name='urinAnalysis'),
    path('bloodImage/',bloodImage,name='bloodImage'),
    path('urinImage/',urinImage,name='urinImage'),
    path('allimage/',allimage,name='gallery'),
    path('paitent/',paitent,name='paitent'),
    
    # Analysis Url 
    path('cbc_analysis/<pk>/',cbc_analysis,name='cbc_analysis'),
    path('esr_analysis/<pk>/',esr_analysis,name='esr_analysis'),
    path('hba1c_analysis/<pk>/',hba1c_analysis,name='hba1c_analysis'),


    # Image addd Path
    path('cbcimage/',cbcimage,name='cbcimage'),
    path('esrimage/',esrimage,name='esrimage'),
    path('hba1c/',hba1c,name='hba1c'),

]