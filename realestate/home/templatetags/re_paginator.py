from django.template import Library

register = Library()


@register.inclusion_tag('includes/pagination.html', takes_context=True)
def pagination_url(context, paginator):
    pages = []
    if paginator.has_next():
        qdict = context['request'].GET.copy()
        qdict['page'] = paginator.next_page_number()
        next = '?' + qdict.urlencode()
    else:
        next = None
    if paginator.has_previous():
        qdict = context['request'].GET.copy()
        qdict['page'] = paginator.previous_page_number()
        previous = '?' + qdict.urlencode()
    else:
        previous = None
    current = paginator.number
    if paginator.paginator.num_pages > 10:
        if current > 5 and (paginator.paginator.num_pages - current ) < 6:
            pagination_range = range(paginator.paginator.num_pages - 9, paginator.paginator.num_pages + 1)
        elif current > 5:

            pagination_range = range(current - 4, current + 6)
        else:
            pagination_range = range(1, 11)
    else:
        pagination_range = paginator.paginator.page_range
    for page in pagination_range:
        qdict = context['request'].GET.copy()
        qdict['page'] = page
        pages.append({'href': context['request'].path + '?' + qdict.urlencode(), 'page': page})

    return {
        'current': current,
        'next': next,
        'previous': previous,
        'links': pages,
    }

  