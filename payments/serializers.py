from rest_framework import serializers

from .models import Gateway, Payment


class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = ['id', 'gw_type', 'title']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id']

    def to_representation(self, instance):
        data = super(PaymentSerializer, self).to_representation(instance)

        gateway_excluses = {'gw_code': Gateway.FUNCTION_VAS}

        if 'vas_gateway' in self.context and self.context['vas_gateway']:
            gateway_excluses = {}
        data["active_gateways"] = GatewaySerializer(
            instance=Gateway.objects.filter(is_enable=True).exclude(**gateway_excluses), many=True,
            read_only=True).data
        data["pay_url"] = instance.get_url()
        return data
