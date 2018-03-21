# -*- coding: utf-8 -*-
"""Define external bounty related views.

Copyright (C) 2018 Gitcoin Core

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
from django.http import Http404
from django.template.response import TemplateResponse

from external_bounties.forms import ExternalBountyForm
from external_bounties.models import ExternalBounty
from marketing.mails import new_external_bounty


def external_bounties_index(request):
    """Handle External Bounties index page.

    Returns:
        django.TemplateResponse: The external bounty index view.

    """
    tags = []
    external_bounties_results = []
    bounties = ExternalBounty.objects.filter(active=True)
    for external_bounty_result in bounties:
        external_bounty = {
            "created_on": external_bounty_result.created_on,
            "avatar": external_bounty_result.avatar,
            "title": external_bounty_result.title,
            "source": external_bounty_result.source_project,
            "crypto_price": external_bounty_result.amount,
            "fiat_price": external_bounty_result.fiat_price,
            "crypto_label": external_bounty_result.amount_denomination,
            "tags": external_bounty_result.tags,
            "url": external_bounty_result.url,
        }
        tags = tags + external_bounty_result.tags
        external_bounties_results.append(external_bounty)
    categories = list(set(tags))
    categories.sort()

    params = {
        'active': 'offchain',
        'title': 'Offchain Bounty Explorer',
        'bounties': external_bounties_results,
        'categories': categories,
    }
    return TemplateResponse(request, 'external_bounties.html', params)


def external_bounties_new(request):
    """Create a new external bounty.

    Returns:
        django.TemplateResponse: The new external bounty form or submission status.

    """
    params = {
        'active': 'offchain',
        'title': 'New Offchain Bounty',
        'formset': ExternalBountyForm,
    }

    if request.POST:
        new_eb = ExternalBountyForm(request.POST)
        new_eb.github_handle = request.session.get('handle')
        new_eb.save()
        new_external_bounty()
        params['msg'] = "An email has been sent to an administrator to approve your submission"

    return TemplateResponse(request, 'external_bounties_new.html', params)


def external_bounties_show(request, issuenum, slug):
    """Handle Dummy External Bounties show page.

    Args:
        issuenum (int): The Github issue number.
        slug (str): The external bounty slug represenation.

    Returns:
        django.TemplateResponse: The external bounty details view.

    """
    print('************')
    print(issuenum)
    if issuenum == '':
        return external_bounties_index(request)

    try:
        bounty = ExternalBounty.objects.get(pk=issuenum, active=True)
    except Exception:
        raise Http404

    external_bounty = {}
    external_bounty_result = bounty
    external_bounty['created_on'] = external_bounty_result.created_on
    external_bounty['title'] = external_bounty_result.title
    external_bounty['crypto_price'] = external_bounty_result.amount
    external_bounty['crypto_label'] = external_bounty_result.amount_denomination
    external_bounty['fiat_price'] = external_bounty_result.amount
    external_bounty['source'] = external_bounty_result.source_project
    external_bounty['content'] = external_bounty_result.description
    external_bounty['action_url'] = external_bounty_result.action_url
    external_bounty['avatar'] = external_bounty_result.avatar
    external_bounty['fiat_price'] = external_bounty_result.fiat_price

    params = {
        'active': 'offchain',
        'title': 'Offchain Bounty Explorer',
        "bounty": external_bounty,
    }
    return TemplateResponse(request, 'external_bounties_show.html', params)
