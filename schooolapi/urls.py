from rest_framework.routers import DefaultRouter

from .views import ProgramaView

router = DefaultRouter()

router.register('programa', ProgramaView)

urlpatterns = router.urls