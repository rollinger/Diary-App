from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from journal.models import Emotion, Entry

User = get_user_model()

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

	def get_queryset(self, request):
		""" Shows all objects to superuser. To all others only
		their own entries
		"""
		if request.user.is_superuser:
			queryset = super(EntryAdmin, self).get_queryset(request)
		else:
			queryset = Entry.objects.my_entries(user=request.user)
		return queryset

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		# TODO/FIX: does not filter yet
		if db_field.name == "user":
			kwargs["queryset"] = User.objects.filter(pk=request.user.pk)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

	def _get_emotion_list(self, obj):
		"""Aggregate emotions for listing in display"""
		return ", ".join([e.name for e in obj.emotions.all()])
	_get_emotion_list.allow_tags = True
	_get_emotion_list.short_description = _('List of Emotions')
