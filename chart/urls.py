from django.urls import path
from . import views

urlpatterns = [
   path("", views.home_view, name="home"),
   path("bc_cases_by_age_group/", views.bc_cases_by_age_group_view, name="bc_cases_by_age_group"),
   path("bc_cases_by_age_group/<str:end_date>/", views.bc_cases_by_age_group_view, name="bc_cases_by_age_group"),
   path("bc_cases_by_sex/", views.bc_cases_by_sex_view, name="bc_cases_by_sex"),
   path("bc_cases_by_ha/", views.bc_cases_by_ha_view, name="bc_cases_by_ha"),
   path("bc_cases_and_mortality/", views.bc_cases_and_mortality_view, name="bc_cases_and_mortality"),
   path("bc_cases_and_mortality/<str:start_date>/", views.bc_cases_and_mortality_view, name="bc_cases_and_mortality"),
   path("bc_cases_and_mortality/<str:start_date>/<str:end_date>/", views.bc_cases_and_mortality_view, name="bc_cases_and_mortality"),
   path("bc_ha_cases_and_mortality/<str:ha>/", views.bc_ha_cases_and_mortality_view, name="bc_ha_cases_and_mortality"),
   path("bc_ha_cases_and_mortality/<str:ha>/<str:end_date>/", views.bc_ha_cases_and_mortality_view, name="bc_ha_cases_and_mortality"),
   path("bc_cases_and_testing_by_ha/", views.bc_cases_and_testing_by_ha_view, name="bc_cases_and_testing_by_ha"),
   path("bc_cases_and_testing_by_ha/<str:ha>/", views.bc_cases_and_testing_by_ha_view, name="bc_cases_and_testing_by_ha"),
   path("bc_cases_and_testing_by_ha/<str:ha>/<str:start_date>/", views.bc_cases_and_testing_by_ha_view, name="bc_cases_and_testing_by_ha"),
   path("bc_cases_and_testing_by_ha/<str:ha>/<str:start_date>/<str:end_date>/", views.bc_cases_and_testing_by_ha_view, name="bc_cases_and_testing_by_ha"),
   path("bc_lab_tests/<str:region>/", views.bc_lab_tests_view, name="bc_lab_tests"),
   path("bc_lab_tests/<str:region>/<str:start_date>/<str:end_date>/", views.bc_lab_tests_view, name="bc_lab_tests"),
   path("bc_lab_tests/<str:region>/<str:start_date>/", views.bc_lab_tests_view, name="bc_lab_tests"),
   path("bc_lab_tests_before/<str:region>/<str:end_date>/", views.bc_lab_tests_before_view, name="bc_lab_tests_before"),
]
