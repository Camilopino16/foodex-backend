from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, UserViewSet, RecetaViewSet, IngredienteViewSet, PasoViewSet, CanastaViewSet

router = DefaultRouter()
router.register(r"roles", RoleViewSet)
router.register(r"users", UserViewSet, basename="users")
router.register(r"recetas", RecetaViewSet)
router.register(r"ingredientes", IngredienteViewSet)
router.register(r"pasos", PasoViewSet)
router.register(r"canasta", CanastaViewSet)

urlpatterns = router.urls
