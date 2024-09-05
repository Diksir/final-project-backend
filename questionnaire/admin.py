from django.contrib import admin
from .models import Faculty, Department, Course, QuestionPaper

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty')
    search_fields = ('name', 'faculty__name')
    list_filter = ('faculty',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'faculty')
    search_fields = ('name', 'code', 'department__name', 'faculty__name')
    list_filter = ('faculty',)

@admin.register(QuestionPaper)
class QuestionPaperAdmin(admin.ModelAdmin):
    ist_display = ('course', 'document')
    search_fields = ('course__name',)
    list_filter = ('course',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            if request is not None:
                if 'department' in request.GET:
                    department_id = request.GET.get('department')
                    kwargs["queryset"] = Course.objects.filter(department_id=department_id)
                elif request.POST.get('department'):
                    department_id = request.POST.get('department')
                    kwargs["queryset"] = Course.objects.filter(department_id=department_id)
                else:
                    kwargs["queryset"] = Course.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        js = ('admin/js/custom_filter.js',)