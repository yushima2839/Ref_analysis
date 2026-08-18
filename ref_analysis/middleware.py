from django.shortcuts import render
from ref_analysis.models import Teams, Referees


class ErrorHandlingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):

        if isinstance(exception, ValueError):
            error_message = str(exception)

        elif isinstance(exception, Teams.DoesNotExist):
            error_message = '指定されたチームが存在しません。'

        elif isinstance(exception, Referees.DoesNotExist):
            error_message = '指定された審判が存在しません。'

        else:
            error_message = '予期せぬエラーが発生しました。'

        return render(
            request,
            'ref_analysis/error.html',
            {'error_message': error_message}
        )