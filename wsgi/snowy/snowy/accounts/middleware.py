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

from django.middleware.common import CommonMiddleware
from django.utils import translation
from django.http import HttpResponseRedirect

from django.conf import settings

class LocaleMiddleware:
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated():
            profile = request.user.get_profile()
            if profile.language:
                translation.activate(profile.language)
        return None

class LoginRedirectMiddleware:
    def process_request(self, request):
        if request.path == settings.LOGIN_REDIRECT_URL and \
        request.session.get('login_complete_redirect', None) and \
        request.user.is_authenticated():
            redirect_to = request.session['login_complete_redirect']
            # do not redirect the next time the user visits LOGIN_REDIRECT_URL
            request.session['login_complete_redirect'] = None
            return HttpResponseRedirect(redirect_to)
