import unittest
import torch
import torch_testing as tt
from all.environments.state import State, DONE
from all.bodies import TimeFeature


class TestAgent():
    def __init__(self):
        self.last_state = None

    def act(self, state, _):
        self.last_state = state
        return torch.zeros(len(state))


class TimeFeatureTest(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(2)
        self.test_agent = TestAgent()
        self.agent = TimeFeature(self.test_agent)

    def test_init(self):
        state = State(torch.randn(1, 4))
        self.agent.act(state, 0)
        tt.assert_allclose(self.test_agent.last_state.features, torch.tensor(
            [[0.3923, -0.2236, -0.3195, -1.2050, 0.0000]]), atol=1e-04)

    def test_single_env(self):
        state = State(torch.randn(1, 4))
        self.agent.act(state, 0)
        tt.assert_allclose(self.test_agent.last_state.features, torch.tensor(
            [[0.3923, -0.2236, -0.3195, -1.2050, 0.0000]]), atol=1e-04)
        self.agent.act(state, 0)
        tt.assert_allclose(self.test_agent.last_state.features, torch.tensor(
            [[0.3923, -0.2236, -0.3195, -1.2050, 1.0000]]), atol=1e-04)
        self.agent.act(state, 0)
        tt.assert_allclose(self.test_agent.last_state.features, torch.tensor(
            [[0.3923, -0.2236, -0.3195, -1.2050, 2.0000]]), atol=1e-04)

    def test_reset(self):
        state = State(torch.randn(1, 4))
        self.agent.act(state, 0)
        tt.assert_allclose(self.test_agent.last_state.features, torch.tensor(
            [[0.3923, -0.2236, -0.3195, -1.2050, 0.0000]]), atol=1e-04)
        self.agent.act(state, 0)
        tt.assert_allclose(self.test_agent.last_state.features, torch.tensor(
            [[0.3923, -0.2236, -0.3195, -1.2050, 1.0000]]), atol=1e-04)
        self.agent.act(State(state.features, DONE), 0)
        tt.assert_allclose(self.test_agent.last_state.features, torch.tensor(
            [[0.3923, -0.2236, -0.3195, -1.2050, 2.0000]]), atol=1e-04)
        self.agent.act(State(state.features), 0)
        tt.assert_allclose(self.test_agent.last_state.features, torch.tensor(
            [[0.3923, -0.2236, -0.3195, -1.2050, 0.0000]]), atol=1e-04)
        self.agent.act(state, 0)
        tt.assert_allclose(self.test_agent.last_state.features, torch.tensor(
            [[0.3923, -0.2236, -0.3195, -1.2050, 1.0000]]), atol=1e-04)

    def test_multi_env(self):
        state = State(torch.randn(2, 2))
        self.agent.act(state, 0)
        tt.assert_allclose(self.test_agent.last_state.features, torch.tensor(
            [[0.3923, -0.2236, 0.], [-0.3195, -1.2050, 0.]]), atol=1e-04)
        self.agent.act(state, 0)
        tt.assert_allclose(self.test_agent.last_state.features, torch.tensor(
            [[0.3923, -0.2236, 1.], [-0.3195, -1.2050, 1.]]), atol=1e-04)
        self.agent.act(State(state.features, torch.tensor([1., 0.])), 0)
        tt.assert_allclose(self.test_agent.last_state.features, torch.tensor(
            [[0.3923, -0.2236, 2.], [-0.3195, -1.2050, 2.]]), atol=1e-04)
        self.agent.act(state, 0)
        tt.assert_allclose(self.test_agent.last_state.features, torch.tensor(
            [[0.3923, -0.2236, 3.], [-0.3195, -1.2050, 0.]]), atol=1e-04)
        self.agent.act(state, 0)
        tt.assert_allclose(self.test_agent.last_state.features, torch.tensor(
            [[0.3923, -0.2236, 4.], [-0.3195, -1.2050, 1.]]), atol=1e-04)

if __name__ == '__main__':
    unittest.main()