from pdm2022.env.wall import WallObstacle
import numpy as np

# Wall obstacle
wallObs1Dict = {
    "type": "wall",
    "geometry": {
        "position": [-0.5, 1.0, 0.0],
        "rotation": 90 * np.pi / 180,
        "length": 3.0,
        "width": 0.1,
    },
    "movable": False,
}
wallObst1 = WallObstacle(name="wall1", content_dict=wallObs1Dict)

wallObs2Dict = {
    "type": "wall",
    "geometry": {
        "position": [1.5, -1.5, 0.0],
        "rotation": 90 * np.pi / 180,
        "length": 2.0,
        "width": 0.1,
    },
    "movable": False,
}
wallObst2 = WallObstacle(name="wall2", content_dict=wallObs2Dict)

wallObs3Dict = {
    "type": "wall",
    "geometry": {
        "position": [3.5, 2.0, 0.0],
        "rotation": 90 * np.pi / 180,
        "length": 3,
        "width": 0.1,
    },
    "movable": False,
}
wallObst3 = WallObstacle(name="wall3", content_dict=wallObs3Dict)