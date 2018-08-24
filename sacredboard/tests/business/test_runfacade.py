# coding=utf-8
"""
Run Facade feature tests.

This sample uses the pytest-bdd extension for behavioral tests.
For educational purposes...
"""
import pytest
from flexmock import flexmock
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
    parsers)

from sacredboard.app.business import RunFacade
from sacredboard.app.data import DataStorage, MetricsDAO, NotFoundError
from sacredboard.app.data.rundao import RunDAO


@pytest.mark.skip(reason="Bug in pytest-bdd https://github.com/pytest-dev/pytest-bdd/issues/250")
@scenario('runfacade.feature', 'Removing a run')
def test_removing_a_run1():
    """Removing a run."""
    pass


@pytest.mark.skip(reason="Bug in pytest-bdd https://github.com/pytest-dev/pytest-bdd/issues/250")
@scenario('runfacade.feature', 'Removing a run when two runs exist')
def test_abcremoving_a_run2():
    """Removing a run when two runs exist"""
    pass

@pytest.mark.skip(reason="Bug in pytest-bdd https://github.com/pytest-dev/pytest-bdd/issues/250")
@scenario('runfacade.feature', 'Removing a run with two metrics')
def test_removing_a_run_with_two_metrics():
    """Removing a run with two metrics"""
    pass

@when(parsers.parse('Run {run_id:d} exists'))
def a_run_exists(run_id, data_access):
    """A run exists."""
    data_access.get_run_dao().should_receive("get").with_args(run_id) \
        .and_return({"_id": run_id})
    assert data_access.get_run_dao().get(run_id) is not None


@when(parsers.parse('Metric {metric_id} of run {run_id:d} exists'))
def a_metric_of_that_run_exists(data_access, metric_id, run_id):
    """A metric of that run exists."""
    data_access.get_run_dao().get(run_id)["info"] = {
        "metrics": [metric_id]}
    data_access.get_metrics_dao().should_receive("get") \
        .with_args(run_id, metric_id) \
        .and_return({"metric_id": str(metric_id), "run_id": str(run_id)})
    assert data_access.get_metrics_dao().get(run_id,
                                             metric_id) is not None

@when(parsers.parse('I delete run {run_id:d}'))
def i_delete_the_run(run_facade, run_id):
    run_facade.delete_run(run_id)


@then(parsers.parse('Metric {metric_id} of run {run_id:d} should not exist'))
def the_metric_of_that_run_should_not_exist(data_access, metric_id, run_id):
    """The metric of that run should not exist."""
    with pytest.raises(NotFoundError):
        data_access.get_metrics_dao().get(run_id, metric_id)


@then(parsers.parse('Run {run_id:d} should not exist'))
def the_run_should_not_exist(data_access, run_id):
    """The run should not exist."""
    with pytest.raises(NotFoundError):
        data_access.get_run_dao().get(run_id)


@then(parsers.parse('Run {run_id:d} should exist'))
def the_run_should_exist(data_access, run_id):
    """The run should exist."""
    assert data_access.get_run_dao().get(run_id)["_id"] == run_id


@then(parsers.parse('Metric {metric_id} of run {run_id:d} should exist'))
def the_metric_of_that_run_should_exist(data_access, metric_id, run_id):
    """The metric of that run should exist."""
    assert data_access.get_metrics_dao().get(run_id,
                                             metric_id)[
               "metric_id"] == metric_id


@given("Data gateway")
def data_access():
    data_access = flexmock(DataStorage())
    run_dao = flexmock(RunDAO())
    metric_dao = flexmock(MetricsDAO())
    data_access.should_receive("get_run_dao").and_return(run_dao)
    data_access.should_receive("get_metrics_dao").and_return(metric_dao)

    # once deleted, it should raise an error
    metric_dao.delete = lambda run_id: metric_dao.should_receive(
        "get").with_args(run_id, object).and_raise(NotFoundError)
    run_dao.delete = lambda run_id: run_dao.should_receive(
        "get").with_args(run_id).and_raise(NotFoundError)

    # default behaviour:
    run_dao.should_receive("get").with_args(object).and_raise(
        NotFoundError)
    metric_dao.should_receive("get").with_args(object,
                                                      object).and_raise(
        NotFoundError)
    return data_access


@pytest.fixture()
def run_facade(data_access):
    return RunFacade(data_access)