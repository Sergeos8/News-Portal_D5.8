from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter
from django.forms import DateInput, CheckboxSelectMultiple
from .models import Author, Category, Post, Comment


class PostFilter(FilterSet):
    category = ModelMultipleChoiceFilter(
        field_name='postcategory__category_category',
        queryset=Category.objects.all(),
        label='Category',
        widget=CheckboxSelectMultiple()
    )
    date_widget = DateInput()
    date_widget.input_type = 'date'
    date_created = DateFilter(
        field_name='date_created',
        lookup_expr='gte',
        widget=date_widget,
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }
