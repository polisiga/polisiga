from django.contrib.auth.decorators import (
    login_required,
    permission_required)
from django.shortcuts import (
    get_object_or_404,
    render)


@login_required
def index(request):
    return render(request, 'academico/index.html')

@login_required
@permission_required('view_alumno')
def alumno_list(request):
    return render(request, 'academico/alumno_list.html')

def alumno_detail(request):
    pass



