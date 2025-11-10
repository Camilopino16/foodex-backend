from rest_framework import serializers
from .models import Role, User, Receta, PasoProcedimiento, Ingrediente, Canasta

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "nombre_rol"]

class UserSerializer(serializers.ModelSerializer):
    rol = RoleSerializer(read_only=True)
    rol_id = serializers.PrimaryKeyRelatedField(
        source="rol", queryset=Role.objects.all(), write_only=True, allow_null=True
    )
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email",
                  "semestre", "carrera", "rol", "rol_id"]

class PasoProcedimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasoProcedimiento
        fields = ["id", "orden_procedimiento", "descripcion"]

class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = ["id", "nombre_ing", "tipo_ing", "cantidad_base", "unidad"]

class RecetaSerializer(serializers.ModelSerializer):
    autor = UserSerializer(read_only=True)
    autor_id = serializers.PrimaryKeyRelatedField(
        source="autor", queryset=User.objects.all(), write_only=True, allow_null=True
    )
    pasos = PasoProcedimientoSerializer(many=True)
    ingredientes = IngredienteSerializer(many=True)

    class Meta:
        model = Receta
        fields = [
            "id","nombre_receta","tipo","autor","autor_id","porciones_base",
            "tiempo_preparacion_min","detalle_montaje","url_bosquejo_base",
            "pasos","ingredientes","creado_en","actualizado_en"
        ]

    def create(self, validated):
        pasos = validated.pop("pasos", [])
        ings = validated.pop("ingredientes", [])
        receta = Receta.objects.create(**validated)
        for i in ings:
            Ingrediente.objects.create(receta=receta, **i)
        for p in pasos:
            PasoProcedimiento.objects.create(receta=receta, **p)
        return receta

    def update(self, instance, validated):
        pasos = validated.pop("pasos", None)
        ings = validated.pop("ingredientes", None)
        for k, v in validated.items():
            setattr(instance, k, v)
        instance.save()
        if ings is not None:
            instance.ingredientes.all().delete()
            for i in ings:
                Ingrediente.objects.create(receta=instance, **i)
        if pasos is not None:
            instance.pasos.all().delete()
            for p in pasos:
                PasoProcedimiento.objects.create(receta=instance, **p)
        return instance

class CanastaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canasta
        fields = ["id", "ingrediente", "cantidad_disponible", "unidad"]
