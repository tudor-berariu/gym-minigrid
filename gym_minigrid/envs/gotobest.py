""" Here we define our Go To The Best Object environment.
    It's some kind of Multi-Armed Bandit hidden on a map.
"""

from gym_minigrid.minigrid import COLOR_NAMES, MiniGridEnv, Grid, Key, Ball, Box
from gym_minigrid.register import register


class GoToBestObjectEnv(MiniGridEnv):
    """ Environment in which the agent is instructed to go to a given object
        named using an English text string
    """

    def __init__(self, size=7, num_objs=2, target="random"):
        valid_targets = (
            ["random", "random_color", "random_type"]
            + COLOR_NAMES
            + ["key", "ball", "box"]
        )
        if target not in valid_targets:
            raise ValueError(f"Expected target to be one of {', '.join(valid_targets)}")

        self.target = target
        self.num_objs = num_objs

        super().__init__(
            grid_size=size,
            max_steps=5 * size ** 2,
            # Set this to True for maximum speed
            see_through_walls=True,
        )

    def _gen_grid(self, width, height):
        # pylint: disable=attribute-defined-outside-init
        self.grid = Grid(width, height)
        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Types and colors of objects we can generate
        types = ["key", "ball", "box"]

        objs = []
        self.obj_pos = obj_pos = []

        target = self.target
        if target == "random":
            target = self._rand_elem(["random_color", "random_type"])
        if target == "random_color":
            target = self._rand_elem(COLOR_NAMES)
        elif target == "random_type":
            target = self._rand_elem(types)

        # Until we have generated all the objects
        obj_idx = 0
        while len(objs) < self.num_objs:
            obj_type = self._rand_elem(types)
            obj_color = self._rand_elem(COLOR_NAMES)
            if obj_idx == 0:
                if target in types:
                    obj_type = target
                elif target in COLOR_NAMES:
                    obj_color = target
                else:
                    raise ValueError("Shouldn't...")
            elif obj_type == target or obj_color == target:
                continue
            # If this object already exists, try again
            if (obj_type, obj_color) in objs:
                continue

            if obj_type == "key":
                obj = Key(obj_color)
            elif obj_type == "ball":
                obj = Ball(obj_color)
            elif obj_type == "box":
                obj = Box(obj_color)

            pos = self.place_obj(obj)
            objs.append((obj_type, obj_color))
            obj_pos.append(pos)
            obj_idx += 1

        # Randomize the agent start position and orientation
        self.place_agent()

        # Choose a random object to be picked up
        self.target_type, self.target_color = objs[0]
        self.target_pos = obj_pos[0]

        desc_str = "%s %s" % (self.target_color, self.target_type)
        self.mission = "go to the %s" % desc_str
        # print(self.mission)

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)

        ag_x, ag_y = self.agent_pos
        target_x, target_y = self.target_pos

        # Toggle/pickup action terminates the episode
        if action == self.actions.toggle:
            done = True

        # Reward performing the done action next to the target object
        if action == self.actions.done:
            if abs(ag_x - target_x) <= 1 and abs(ag_y - target_y) <= 1:
                reward = self._reward()
            else:
                for (obj_x, obj_y) in self.obj_pos:
                    if abs(ag_x - obj_x) <= 1 and abs(ag_y - obj_y) <= 1:
                        reward = self._reward() * 0.1
            done = True

        return obs, reward, done, info


# Environments with a specific object as a target.


class GotoEnv7x7N3Key(GoToBestObjectEnv):
    """ Here we generate a 7x7 grid with 3 objects where the target is the KEY.
    """

    def __init__(self):
        super().__init__(size=7, num_objs=3, target="key")


class GotoEnv7x7N3Box(GoToBestObjectEnv):
    """ Here we generate a 7x7 grid with 3 objects where the target is the BOX.
    """

    def __init__(self):
        super().__init__(size=7, num_objs=3, target="box")


class GotoEnv7x7N3Ball(GoToBestObjectEnv):
    """ Here we generate a 7x7 grid with 3 objects where the target is the BALL.
    """

    def __init__(self):
        super().__init__(size=7, num_objs=3, target="ball")


# Colors 'red', 'green', 'blue', 'purple', 'yellow', 'grey'


class GotoEnv7x7N3Red(GoToBestObjectEnv):
    """ Here we generate a 7x7 grid with 3 objects where the target is the RED thing.
    """

    def __init__(self):
        super().__init__(size=7, num_objs=3, target="red")


class GotoEnv7x7N3Green(GoToBestObjectEnv):
    """ Here we generate a 7x7 grid with 3 objects where the target is the GREEN thing.
    """

    def __init__(self):
        super().__init__(size=7, num_objs=3, target="green")


class GotoEnv7x7N3Blue(GoToBestObjectEnv):
    """ Here we generate a 7x7 grid with 3 objects where the target is the BLUE thing.
    """

    def __init__(self):
        super().__init__(size=7, num_objs=3, target="blue")


class GotoEnv7x7N3Purple(GoToBestObjectEnv):
    """ Here we generate a 7x7 grid with 3 objects where the target is the PURPLE thing.
    """

    def __init__(self):
        super().__init__(size=7, num_objs=3, target="purple")


class GotoEnv7x7N3Yellow(GoToBestObjectEnv):
    """ Here we generate a 7x7 grid with 3 objects where the target is the YELLOW thing.
    """

    def __init__(self):
        super().__init__(size=7, num_objs=3, target="yellow")


class GotoEnv7x7N3Grey(GoToBestObjectEnv):
    """ Here we generate a 7x7 grid with 3 objects where the target is the GREY thing.
    """

    def __init__(self):
        super().__init__(size=7, num_objs=3, target="grey")


for tgt in ["Red", "Green", "Blue", "Purple", "Yellow", "Grey", "Ball", "Key", "Box"]:
    register(
        id=f"MiniGrid-GoToBest-7x7-N3-{tgt}-v0",
        entry_point=f"gym_minigrid.envs:GotoEnv7x7N3{tgt}",
    )


class GotoEnv7x7N3Color(GoToBestObjectEnv):
    """ Here we generate a 7x7 grid with 3 objects where the target is a random color.
    """

    def __init__(self):
        super().__init__(size=7, num_objs=3, target="random_color")


class GotoEnv7x7N3Type(GoToBestObjectEnv):
    """ Here we generate a 7x7 grid with 3 objects where the target is a random type.
    """

    def __init__(self):
        super().__init__(size=7, num_objs=3, target="random_type")


class GotoEnv7x7N3Random(GoToBestObjectEnv):
    """ Here we generate a 7x7 grid with 3 objects where the target is random something.
    """

    def __init__(self):
        super().__init__(size=7, num_objs=3, target="random")


for smtg in ["Random", "Color", "Type"]:
    register(
        id=f"MiniGrid-GoToBest-7x7-N3-{smtg}-v0",
        entry_point=f"gym_minigrid.envs:GotoEnv7x7N3{smtg}",
    )
