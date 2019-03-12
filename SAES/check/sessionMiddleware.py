from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, render, redirect


class M1(MiddlewareMixin):
    def process_request(self, request):
        if request.path in ['/login/', '/register/']:
            return None

        static = request.session.get("static")
        if not static:
            return redirect('/login/')
