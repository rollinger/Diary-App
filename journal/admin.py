from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from journal.models import Emotion, Entry


@admin.register(Emotion)
class EmotionAdmin(admin.ModelAdmin):
	""" Admin for Emotion
	"""
	save_on_top = True
	list_display = (
		"id",
		"name",
	)
	list_display_links = ("name",)
	readonly_fields = [
        "id",
        "created_at",
        "updated_at",
    ]
	search_fields = ["name"]
	fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                )
            },
        ),
		(
            _("System Information"),
            {
                "classes": ("collapse",),
                "fields": (
                    ("id"),
                    ("created_at", "updated_at"),
                ),
            },
        )
	)



@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
	""" Admin for Diary Journal Entry
	"""
	save_on_top = True
	list_display = (
		"id",
		"user",
		"date",
	)
	list_display_links = ("date",)
	readonly_fields = [
        "id",
		"emotions",
        "created_at",
        "updated_at",
    ]
	search_fields = ["user", "text"]
	fieldsets = (
        (
            None,
            {
                "fields": (
                    ("user", "date"),
					"text",
					"emotions"
                )
            },
        ),
		(
            _("System Information"),
            {
                "classes": ("collapse",),
                "fields": (
                    ("id"),
                    ("created_at", "updated_at"),
                ),
            },
        )
	)