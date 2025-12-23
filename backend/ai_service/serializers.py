from rest_framework import serializers


class PolishSerializer(serializers.Serializer):
    text = serializers.CharField(required=False, allow_blank=True, help_text="需要润色的原始文本")
    image = serializers.ImageField(required=False, allow_null=True, help_text="图片文件（支持jpg, png等格式）")
    model = serializers.CharField(required=False, help_text="指定使用的模型（推荐：zai-org/GLM-4.6V, Qwen/Qwen3-VL-8B-Instruct）")

    def validate(self, attrs):
        if not attrs.get("text") and not attrs.get("image"):
            raise serializers.ValidationError("text 或 image 至少提供一个")
        return attrs


class TagRecommendSerializer(serializers.Serializer):
    text = serializers.CharField(required=False, allow_blank=True)
    image = serializers.ImageField(required=False, allow_null=True)

    def validate(self, attrs):
        if not attrs.get("text") and not attrs.get("image"):
            raise serializers.ValidationError("text 或 image 至少提供一个")
        return attrs


class AIResultSerializer(serializers.Serializer):
    polished_content = serializers.CharField(help_text="润色后的文本")
    suggested_tags = serializers.ListField(child=serializers.CharField(), help_text="推荐的标签列表")
