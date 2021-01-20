from rest_framework import viewsets, mixins, generics, status
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
import csv


from oreo.serializers import MessageSerializer

from .models import Message
from .tasks import update_send_flag


class MessageViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     mixins.ListModelMixin, ):
    """
    A viewset that provides read, create, delete actions
    API: GET:message/   retrieve a list of all messages
         POST:message/  with data format {"title": "123", "body": "123"} to create new message
         GET:message/{id}/ retrieve message by id
         DELETE:message/{id}/ delete message by id
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    throttle_scope = 'create'

    def create(self, request, *args, **kwargs):
        """
        create message method
        """

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            message = Message.objects.create(
                title=serializer.data['title'],
                body=serializer.data['body'],
            )
            update_send_flag.delay(serializer.data, message.pk)
        return Response(
            {'data': serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, *args, **kwargs):
        """
        read message method
        """

        message = self.get_object()
        message.read_flag = True
        message.save()
        serializer = self.get_serializer(message)
        return Response(serializer.data)


class GeneratorCSV(generics.ListAPIView):
    """
    A view that provides API method to generate csv file named "messages.csv" in root
    of project.
    API: GET:generate_csv/
    Also supports filtering by all fields. For example GET:generate_csv/?title=123
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def get(self, request):
        """
        generate csv file method
        """

        messages = self.filter_queryset(self.get_queryset()).order_by('created')
        serializer = self.get_serializer(messages, many=True)
        if serializer.is_valid:
            with open('messages.csv', 'w', newline='') as csvfile:
                message_writer = csv.writer(csvfile, delimiter=',',
                                            quoting=csv.QUOTE_MINIMAL)
                for item in serializer.data:
                    message_writer.writerow(item.values())

        return Response(
            {'data': serializer.data}
        )
