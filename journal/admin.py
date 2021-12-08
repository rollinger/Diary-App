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
		"occasion",
		"_get_emotion_list",
	)
	list_display_links = ("occasion",)
	list_filter = ("emotions",)
	readonly_fields = [
        "id",
		#"emotions",
        "created_at",
        "updated_at",
    ]
	search_fields = ["user", "text"]
	autocomplete_fields = ["user", "emotions"]
	fieldsets = (
        (
            None,
            {
                "fields": (
                    ("user", "occasion"),
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

	def _get_emotion_list(self, obj):
		return ", ".join([e.name for e in obj.emotions.all()])
	_get_emotion_list.allow_tags = True
	_get_emotion_list.short_description = _('List of Emotions')
