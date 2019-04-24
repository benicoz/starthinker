###########################################################################
# 
#  Copyright 2019 Google Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################


from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from starthinker_ui.account.decorators import permission_admin
from starthinker_ui.storage.models import storage_create, storage_list, storage_run, storage_run_all


@permission_admin()
def view_storage_link(request):
  storage_create(request.user)
  return HttpResponseRedirect(request.user.get_bucket())


@permission_admin()
def view_storage_list(request):
  recipes = list(storage_list(request.user))
  return render(request, "storage/storage_list.html", { 'recipes':recipes })


@permission_admin()
def view_storage_run(request, recipe=None):
  try:
    if recipe:
      storage_run(request.user, recipe)
    else:
      storage_run_all(request.user)
    messages.success(request, 'Storage recipe deployed.')
  except Exception, e:
    messages.error(request, 'Error: %s' % str(e))
  return HttpResponseRedirect('/storage/')
