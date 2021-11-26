from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from timekeeping.models import Project, Task, TaskAssignment

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
		"owner",
		"title",
		"slug",
		"id",
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

class TaskAssignmentInline(admin.TabularInline):
	model = TaskAssignment
	fk_name = "task"
	show_change_link = True
	autocomplete_fields = ["user",]
	extra = 1
	fields = ("user", "allowed", "max_workload", "current_workload",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	""" Admin for Tasks
	"""
	save_on_top = True
	list_display = (
		"project",
		"title",
		"status",
		"id",
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
		TaskAssignmentInline,
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


@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
	""" Admin for Task Assignments
	"""
	save_on_top = True
	list_display = (
		"task",
		"user",
		"current_workload",
		"max_workload",
		"allowed",
		"id",
	)
	list_display_links = ("task", "user",)
	readonly_fields = [
		"id",
		"current_workload",
		"archived_log",
		"created_at",
		"updated_at",
	]
	search_fields = ["task", "user"]
	autocomplete_fields = ["task", "user"]
	list_filter = ("allowed", "max_workload",)
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
					("max_workload", "current_workload", "allowed"),
					("current_log", "archived_log"),
				)
			},
		),
		(
			_("System Information"),
			{
				"classes": ("collapse",),
				"fields": (
					("id",),
					("created_at", "updated_at"),
				),
			},
		)
	)
	formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }