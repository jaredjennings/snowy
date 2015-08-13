#
# Copyright (c) 2009 Brad Taylor <brad@getcoded.net>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django import template

from snowy import settings
from snowy.notes.models import Note, NoteTag

from django.db.models import Q

register = template.Library()

@register.tag
def user_notes_list(parser, tokens):
    """ Usage:
        {% user_notes_list request author as list_notes %}
    """
    try:
        tag_name, request, author, _as, dest = tokens.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
            "%r tag requires exactly four arguments" % tag_name
    if _as != "as":
        raise template.TemplateSyntaxError, \
            "%r tag's third argument should be 'as'" % tag_name
    return UserNotesListNode(request, author, dest)

class UserNotesListNode(template.Node):
    def __init__(self, request, author, dest):
        self.request = template.Variable(request)
        self.author = template.Variable(author)
        self.dest = dest

    def render(self, context):
        request = self.request.resolve(context)
        author = self.author.resolve(context)
        search_query = request.GET.get('query', None)

        list_notes = Note.objects.user_viewable(request.user, author) \
                                .order_by('-pinned', '-user_modified')
        
        if search_query:
            list_notes = list_notes.filter(Q(title__icontains=search_query) |
                                           Q(content__icontains=search_query))

        if not search_query:
            # do not limit the amount of search results returned
            list_notes = list_notes[:settings.SNOWY_LIST_MAX_NOTES]

        context[self.dest] = list_notes
        return ''

@register.tag
def user_notebook_list(parser, tokens):
    """ Usage:
        {% user_notebook_list request author as all_notebooks %}
    """
    try:
        tag_name, request, author, _as, dest = tokens.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
            "%r tag requires exactly four arguments" % tag_name
    if _as != "as":
        raise template.TemplateSyntaxError, \
            "%r tag's third argument should be 'as'" % tag_name
    return UserNotebookListNode(request, author, dest)

class UserNotebookListNode(template.Node):
    def __init__(self, request, author, dest):
        self.request = template.Variable(request)
        self.author = template.Variable(author)
        self.dest = dest

    def render(self, context):
        request = self.request.resolve(context)
        author = self.author.resolve(context)

        context[self.dest] = NoteTag.objects.filter(author=author,
	                                            is_notebook=True)[:5]
        return ''
