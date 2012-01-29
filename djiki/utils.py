import re
from django.conf import settings
from django.db.models import Q

def spaces_as_underscores():
        return getattr(settings, 'DJIKI_SPACES_AS_UNDERSCORES', True)

def urlize_title(title):
    if spaces_as_underscores():
        return re.sub(r'\s+', '_', title)
    return title

def deurlize_title(title):
    if spaces_as_underscores():
        return re.sub(r'[_\s]+', ' ', title)
    return title

def anchorize(txt):
    return re.compile(r'[^\w_,\.-]+', re.UNICODE).sub('_', txt).strip('_')


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
