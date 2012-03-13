# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from openstack.common import exception as openstack_exception


ClientConnectionError = openstack_exception.ClientConnectionError
ProcessExecutionError = openstack_exception.ProcessExecutionError
DatabaseMigrationError = openstack_exception.DatabaseMigrationError


class MelangeError(openstack_exception.OpenstackException):
    """Base exception that all custom melange app exceptions inherit from."""

    def __init__(self, message=None, **kwargs):
        if message is not None:
            self.message = message
        super(MelangeError, self).__init__(**kwargs)


class ParamsMissingError(MelangeError):

    message = _("Data Missing")


class MelangeServiceResponseError(MelangeError):

    message = _("Error while responding to service call")


class DBConstraintError(MelangeError):

    message = _("Failed to save %(model_name)s because: %(error)s")


class NoMoreAddressesError(MelangeError):

    message = _("no more addresses")


class InvalidNotifier(MelangeError):

    message = _("no such notifier %(notifier)s exists")
