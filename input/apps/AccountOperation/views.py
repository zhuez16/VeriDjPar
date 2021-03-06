from rest_framework import mixins
from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .serializers import UserVoteSerializer, UserFlowQuestionSerializer, UserFavSerializer
from .models import UserVote, UserFlowQuestion, UserFav





class UserFlowQuestionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                              mixins.CreateModelMixin, mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):

    """
    用户关注问题
    """

    serializer_class = UserFlowQuestionSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = "question"

    def get_queryset(self):
        return UserFlowQuestion.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save()
        question = instance.question
        question.flow()

    def perform_destroy(self, instance):
        question = instance.question
        question.cancel_flow()
        question.delete()


class UserFavViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin, mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    """
    用户收藏回答
    """

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = UserFavSerializer
    lookup_field = "answer"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)
