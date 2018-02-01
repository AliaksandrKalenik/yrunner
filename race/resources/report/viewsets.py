import datetime as dt

from django.db.models import Sum, Avg
from django.http.response import HttpResponseBadRequest
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from race.models import Race
from race.resources.report.serializer import RaceReportSerializer, WeekReport


class RaceReportViewSet(ListAPIView):
    queryset = Race.objects.order_by("date")
    serializer_class = RaceReportSerializer

    def list(self, request, *args, **kwargs):
        week_items = self.get_report(request.query_params['start_date'], request.query_params['end_date'])
        # serializer = RaceReportSerializer(
        #     instance=week_items, many=True
        # )
        return Response(week_items)

    def get_report(self, start_date, end_date):
        if not isinstance(start_date, dt.date):
            start_date = dt.datetime.strptime(start_date, '%Y-%m-%d').date()
        if not isinstance(end_date, dt.date):
            end_date = dt.datetime.strptime(end_date, '%Y-%m-%d').date()
        while start_date.weekday() != 0:
            start_date = start_date + dt.timedelta(days=1)
        while end_date.weekday() != 6:
            end_date = end_date - dt.timedelta(days=1)
        if end_date < start_date:
            return HttpResponseBadRequest("End date less than start date")

        qs = self.get_queryset()
        delta_start_date = start_date
        delta_end_date = start_date + dt.timedelta(days=6)
        week_items = []
        while delta_end_date != end_date:
            total_result = qs.filter(
                date__gte=delta_start_date,
                date__lte=delta_end_date
            ).annotate(
                total_distance=Sum('distance'),
                total_time=Sum('time'),
            ).values_list("total_distance", "total_time").first()
            average_time = qs.filter(
                date__gte=delta_start_date,
                date__lte=delta_end_date
            ).all().aggregate(
                average_time=Avg('time'),
            ).get("average_time")
            if total_result:
                total_distance = total_result[0]
            else:
                total_distance = None
            if total_result:
                total_time = total_result[1]
            else:
                total_time = None
            if total_distance and total_time:
                average_speed = total_distance/total_time.seconds
            else:
                average_speed = None
            week_report = dict(
                week_start_date=delta_start_date,
                week_end_date=delta_end_date,
                total_distance=total_distance,
                average_speed=average_speed,
                average_time=average_time,
            )
            week_items.append(week_report)
            delta_start_date += dt.timedelta(days=7)
            delta_end_date += dt.timedelta(days=7)
        return week_items

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        if not user.is_superuser:
            queryset = queryset.filter(user=user)
        return queryset
