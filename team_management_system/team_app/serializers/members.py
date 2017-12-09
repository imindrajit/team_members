import json
from django.core.serializers import serialize

from team_app.models import Member


class MemberSerializer:
    @staticmethod
    def serialize(obj):
        if isinstance(obj, Member):
            obj = [obj]

        serialized_result = serialize("json", obj)
        json_serialized_results = json.loads(serialized_result)
        json_data = list()
        for each_result in json_serialized_results:
            data = each_result.get('fields')
            data['unique_id'] = each_result.get("pk")
            data.pop('is_active', None)
            json_data.append(data)
        return json_data