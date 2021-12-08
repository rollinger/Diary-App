from datetime import date
from django import forms
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



class EntryAdminForm(forms.ModelForm):
	class Meta:
		model = Entry
		exclude = [
			"created_at",
        	"updated_at",
		]

	def __init__(self, *args, **kwargs):
		super(EntryAdminForm, self).__init__(*args, **kwargs)
		self.initial['occasion'] = date.today()


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
		"user",
        "created_at",
        "updated_at",
    ]
	search_fields = ["user", "text"]
	autocomplete_fields = ["user", "emotions"]
	form = EntryAdminForm
	fieldsets = (
        (
            None,
            {
                "fields": (
                    ("occasion"),
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
                    ("id","user",),
                    ("created_at", "updated_at"),
                ),
            },
        )
	)

	def save_model(self, request, obj, form, change):
		""" Adds the request user as the user, always."""
		obj.user = request.user
		obj.save()

	def get_queryset(self, request):
		""" Shows all objects to superuser. To all others only
		their own entries
		"""
		if request.user.is_superuser:
			queryset = super(EntryAdmin, self).get_queryset(request)
		else:
			queryset = Entry.objects.my_entries(user=request.user)
		return queryset

	def _get_emotion_list(self, obj):
		"""Aggregate emotions for listing in display"""
		return ", ".join([e.name for e in obj.emotions.all()])
	_get_emotion_list.allow_tags = True
	_get_emotion_list.short_description = _('List of Emotions')
