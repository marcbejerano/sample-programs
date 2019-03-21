import pytest

from test.fixtures import project_permutations, docker_client
from test.project import ProjectType

invalid_permutations = (
    'description,in_params,expected', [
        (
            'no input',
            None,
            'Usage: please input a non-negative integer'
        ), (
            'empty input',
            '""',
            'Usage: please input a non-negative integer'
        ), (
            'invalid input: not a number',
            '"asdf"',
            'Usage: please input a non-negative integer'
        ), (
            'invalid input: negative',
            '"-1"',
            'Usage: please input a non-negative integer'
        )
    ]
)

valid_permutations = (
    'description,in_params,expected', [
        (
            'sample input: zero',
            '"0"',
            '1'
        ), (
            'sample input: one',
            '1',
            '1'
        ), (
            'sample input: four',
            '4',
            '24'
        ), (
            'sample input: eight',
            '8',
            '40320'
        ), (
            'sample input: ten',
            '10',
            '3628800'
        )
    ]
)


@pytest.fixture(params=project_permutations[ProjectType.Factorial].params,
                ids=project_permutations[ProjectType.Factorial].ids)
def factorial(request):
    return request.param


@pytest.mark.parametrize(valid_permutations[0], valid_permutations[1],
                         ids=[p[0] for p in valid_permutations[1]])
def test_factorial_valid(description, in_params, expected, docker_client, factorial):
    actual = factorial.run(docker_client, params=in_params)
    assert actual.strip() == expected


@pytest.mark.parametrize(valid_permutations[0], valid_permutations[1],
                         ids=[p[0] for p in valid_permutations[1]])
def test_factorial_invalid(description, in_params, expected, docker_client, factorial):
    actual = factorial.run(docker_client, params=in_params, expect_error=True)
    assert actual.strip() == expected