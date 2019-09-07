from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^signin/$',views.signin,name='signin'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^dashboard/$',views.dashboard,name='dashboard'),
    url(r'^dashboard/income/$',views.income,name='income'),
    url(r'^dashboard/income/edit/(?P<id>[0-9]+)/$',views.income_edit,name='income_edit'),
    url(r'^dashboard/income/delete/(?P<id>[0-9]+)/$',views.income_delete,name='income_delete'),
    url(r'^dashboard/expense/$',views.expense,name='expense'),
    url(r'^dashboard/expense/edit/(?P<id>[0-9]+)/$',views.expenses_edit,name='expenses_edit'),
    url(r'^dashboard/expense/delete/(?P<id>[0-9]+)/$',views.expenses_delete,name='expenses_delete'),
    url(r'^dashboard/category/$',views.category,name='category'),
    url(r'^logout/$',views.my_logout,name='logout')
]