from django.urls import path
from . import views

urlpatterns = [
    # URLS from App runway
    # Landing
    path('landing/', views.ProductLandingPageView.as_view(), name='landing-page'),
    # Success
    path('success/', views.SuccessView.as_view(), name='success'),
    # Cancel
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    # Create checkout session
    path('create-checkout-session/<pk>/', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    # Highway View
    path('highway/', views.HighwayView.as_view(), name='highway'),
    # Query contrinution View
    path('query_contribution/', views.QueryContributionView.as_view(), name='query_contribution'),

]
