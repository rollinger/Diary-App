from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from timekeeping.models import Project, Task

class TaskInline(admin.TabularInline):
    model = Task
    fk_name = "project"
    show_change_link = True
    #autocomplete_fields = ["target"]
    #ordering = ("-updated_at",)
    extra = 1
    fields = ("title", "description", "status",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	""" Admin for Projects
	"""
	list_display = (
		"id",
		"owner",
		"title",
		"slug"
	)
	list_display_links = ("title",)
	readonly_fields = [
        "id",
        "created_at",
        "updated_at",
    ]
	search_fields = ["title", "description"]
	autocomplete_fields = ["owner",]
	prepopulated_fields = {"slug": ("title",)}
	inlines = [
		TaskInline,
	]	
	fieldsets = (
        (
            None,
            {
                "fields": (
                    ("title", "owner"),
                    "description",
                )
            },
        ),
		(
            _("System Information"),
            {
                "classes": ("collapse",),
                "fields": (
                    ("id", "slug"),
                    ("created_at", "updated_at"),
                ),
            },
        )
	)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	""" Admin for Tasks
	"""
	list_display = (
		"id",
		"project",
		"title",
		"status",
		"slug"
	)
	list_display_links = ("title",)
	readonly_fields = [
        "id",
        "created_at",
        "updated_at",
    ]
	search_fields = ["title", "description"]
	autocomplete_fields = ["project",]
	list_filter = ("status",)
	prepopulated_fields = {"slug": ("title",)}
	fieldsets = (
        (
            None,
            {
                "fields": (
                    ("project", "title", "status"),
                    "description",
                )
            },
        ),
		(
            _("System Information"),
            {
                "classes": ("collapse",),
                "fields": (
                    ("id", "slug"),
                    ("created_at", "updated_at"),
                ),
            },
        )
	)