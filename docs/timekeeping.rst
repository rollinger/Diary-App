 .. _timekeeping:

Timekeeping
======================================================================

The Timekeeping App handles Projects, Tasks, TaskAssignments and Worklogs
for tracking work time on a project's task.

WORKERS: normal authenticated users that can:
- list their TaskAssignments
- start & stop a log on a TaskAssignment

ADMIN: users where is_Staff == True:
Complete CRUD Interface via API Viewsets.

For a list of Endpoints see the Class Autodocs.

.. automodule:: timekeeping.models
   :members:
   :noindex: