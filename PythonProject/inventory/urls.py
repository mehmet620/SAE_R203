from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.home, name='home'),

    path('server-types/',                views.servertype_list,   name='servertype-list'),
    path('server-types/create/',         views.servertype_create, name='servertype-create'),
    path('server-types/<int:pk>/edit/',  views.servertype_update, name='servertype-update'),
    path('server-types/<int:pk>/delete/',views.servertype_delete, name='servertype-delete'),

    path('servers/',                     views.server_list,   name='server-list'),
    path('servers/create/',              views.server_create, name='server-create'),
    path('servers/<int:pk>/',            views.server_detail, name='server-detail'),
    path('servers/<int:pk>/edit/',       views.server_update, name='server-update'),
    path('servers/<int:pk>/delete/',     views.server_delete, name='server-delete'),

    path('users/',                       views.user_list,   name='user-list'),
    path('users/create/',                views.user_create, name='user-create'),
    path('users/<int:pk>/edit/',         views.user_update, name='user-update'),
    path('users/<int:pk>/delete/',       views.user_delete, name='user-delete'),

    path('services/',                    views.service_list,   name='service-list'),
    path('services/create/',             views.service_create, name='service-create'),
    path('services/<int:pk>/edit/',      views.service_update, name='service-update'),
    path('services/<int:pk>/delete/',    views.service_delete, name='service-delete'),

    path('applications/',                views.application_list,   name='application-list'),
    path('applications/create/',         views.application_create, name='application-create'),
    path('applications/<int:pk>/',       views.application_detail, name='application-detail'),
    path('applications/<int:pk>/edit/',  views.application_update, name='application-update'),
    path('applications/<int:pk>/delete/',views.application_delete, name='application-delete'),

    path('resource-usages/',                 views.resourceusage_list,   name='resourceusage-list'),
    path('resource-usages/create/',          views.resourceusage_create, name='resourceusage-create'),
    path('resource-usages/<int:pk>/delete/', views.resourceusage_delete, name='resourceusage-delete'),

    path('report/',                 views.report_index,  name='report-index'),
    path('report/server/<int:pk>/', views.server_report, name='server-report'),
    path('import/',                 views.json_import,   name='json-import'),
]
