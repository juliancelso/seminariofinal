from django.urls import path
from ..views.dashboard.general import DashboardView
from ..views.dashboard.agent import AgentDashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("agent/", AgentDashboardView.as_view(), name="dashboard-agent"),
]