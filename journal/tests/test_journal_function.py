import pytest
from datetime import timedelta
from time import sleep
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from users.tests.factories import UserFactory
from factory import Faker
from journal.diary.models import Entry, Emotion

User = get_user_model()

@pytest.mark.django_db
def test_create_journal_entry():
    """ Make sure the entry get only saved if user and text is present.
    Test that the date is added if left blank and is equal to today
    """
    pass

@pytest.mark.django_db
def test_my_entries_method():
    """ Make sure the Entry.objects.my_entries() method returns only
    the user entries and is sorted descendingly
    """
    pass




def make_standard_task_entries():
    manager = UserFactory(username="manager")
    worker = UserFactory(username="worker")
    project = Project.objects.create(
        owner = manager,
        title = Faker("title"),
        description = Faker("description"))
    tasks = [
        Task.objects.create(
            project=project, title="Test Task 01", description=Faker("description"), 
            status="started"
        ),
        Task.objects.create(
            project=project, title="Test Task 02", description=Faker("description"), 
            status="planned"
        )
    ]
    assignments = [
        TaskAssignment.objects.create(
            task=tasks[0], user=worker, allowed=True, max_workload=timedelta(hours=2)
        ),
        TaskAssignment.objects.create(
            task=tasks[1], user=manager, allowed=True, max_workload=timedelta(hours=2)
        ),
    ]
    return manager, worker, project, tasks, assignments

@pytest.mark.django_db
def test_standard_task_entries():
    manager, worker, project, tasks, assignments = make_standard_task_entries()
    assert(type(manager) == User)
    assert(type(worker) == User)
    assert(type(project) == Project)
    assert(project.owner == manager)
    for task in tasks:
        assert(type(task) == Task)
        assert(task.project == project)
    for assignment in assignments:
        assert(type(assignment) == TaskAssignment)
    

@pytest.mark.django_db
def test_diary_assigned(user: User):
    # User is assigned to task (True)
    wait_period = 0.05
    manager, worker, project, tasks, assignments = make_standard_task_entries()
    assert(assignments[0].can_log_time(worker) == True)
    assert(assignments[0].start_log_time(worker) == True)
    sleep(wait_period)
    assert(assignments[0].stop_log_time(worker) == True)
    assert(assignments[0].current_log["start"] != None)
    assert(assignments[0].current_log["stop"] != None)
    assert(assignments[0].current_log["time"] >= wait_period)
    assert(assignments[0].current_log["completed"] == True)
    assert(assignments[0].current_workload >= timedelta(seconds=wait_period))


@pytest.mark.django_db
def test_diary_not_assigned(user: User):
    # User is not assigned to task (False)
    manager, worker, project, tasks, assignments = make_standard_task_entries()
    assert(assignments[1].can_log_time(worker) == False)
    assert(assignments[1].can_log_time(manager) == True)

@pytest.mark.django_db
def test_diary_not_assigned(user: User):
    # Assignment is disallowed temporarily (False)
    manager, worker, project, tasks, assignments = make_standard_task_entries()
    assert(assignments[0].can_log_time(worker) == True)
    assignments[0].allowed = False
    assert(assignments[0].can_log_time(worker) == False)

@pytest.mark.django_db
def test_current_diary_workload_exceeded(user: User):
    # Workload is exceeded (False)
    manager, worker, project, tasks, assignments = make_standard_task_entries()
    assert(assignments[0].can_log_time(worker) == True)
    assignments[0].current_workload = assignments[0].max_workload + timedelta(seconds=1)
    assert(assignments[0].can_log_time(worker) == False)

@pytest.mark.django_db
def test_current_diary_workload_exceeded(user: User):
    # Task is not started (False)
    blocking_states = ["planned","hold","finished"]
    manager, worker, project, tasks, assignments = make_standard_task_entries()
    assert(assignments[0].can_log_time(worker) == True)
    for state in blocking_states:
        assignments[0].task.status = state
        assert(assignments[0].can_log_time(worker) == False)
