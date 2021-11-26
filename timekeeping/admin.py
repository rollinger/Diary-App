from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from timekeeping.models import Project, Task, Assignment, Worklog

class TaskInline(admin.TabularInline):
    model = Task
    fk_name = "project"
    show_change_link = True
    extra = 1
    fields = ("title", "description", "status",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	""" Admin for Projects
	"""
	save_on_top = True
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

class AssignmentInline(admin.TabularInline):
	model = Assignment
	fk_name = "task"
	show_change_link = True
	autocomplete_fields = ["user",]
	extra = 1
	fields = ("user", "allowed", "max_workload",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	""" Admin for Tasks
	"""
	save_on_top = True
	list_display = (
		"id",
		"project",
		"title",
		"status",
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
	list_editable = (
		"status",
	)
	inlines = [
		AssignmentInline,
	]
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


class WorklogInline(admin.TabularInline):
    model = Worklog
    fk_name = "assignment"
    show_change_link = True
    extra = 1
    fields = ("start", "stop", "time", "notes")


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
	""" Admin for Assignments
	"""
	save_on_top = True
	list_display = (
		"id",
		"__str__",
		"max_workload",
		"allowed"
	)
	list_display_links = ("__str__",)
	readonly_fields = [
		"id",
		"created_at",
		"updated_at",
	]
	inlines = [
		WorklogInline,
	]
	search_fields = ["task", "user"]
	autocomplete_fields = ["task", "user"]
	list_filter = ("allowed","max_workload",)
	list_editable = (
		"allowed",
		"max_workload",
	)
	fieldsets = (
		(
			None,
			{
				"fields": (
					("task", "user"),
					("max_workload", "allowed"),
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

@admin.register(Worklog)
class WorklogAdmin(admin.ModelAdmin):
	""" Admin for Assignments
	"""
	save_on_top = True
	list_display = (
		"id",
		"assignment",
		"start",
		"stop",
		"time"
	)
	list_display_links = ("assignment",)
	readonly_fields = [
		"id",
		"created_at",
		"updated_at",
	]
	search_fields = ["assignment",]
	autocomplete_fields = ["assignment",]
	date_hierarchy = 'start'
	list_editable = (
		"start",
		"stop",
		"time"
	)
	fieldsets = (
		(
			None,
			{
				"fields": (
					"assignment",
					("start", "stop", "time",),
					"notes",
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
	