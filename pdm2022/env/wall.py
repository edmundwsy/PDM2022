from dataclasses import dataclass
import numpy as np
import os
import csv

from MotionPlanningEnv.collisionObstacle import CollisionObstacle, CollisionObstacleConfig

from MotionPlanningSceneHelpers.motionPlanningComponent import (
    DimensionNotSuitableForEnv,
)

from omegaconf import OmegaConf
from typing import List, Optional

class WallObstacleMissmachException(Exception):
    pass


@dataclass
class GeometryConfig:
    """Configuration dataclass for geometry.

    This configuration class holds information about position
    and radius of a sphere obstacle.

    Parameters:
    ------------

    position: list: Position of the obstacle
    radius: float: Radius of the obstacle
    """

    position: List[float]
    rotation: float
    length: float
    width: float


@dataclass
class WallObstacleConfig(CollisionObstacleConfig):
    """Configuration dataclass for sphere obstacle.
        TODO: add docstring
    """    

    geometry: GeometryConfig
    movable: bool = False
    low: Optional[GeometryConfig] = None
    high: Optional[GeometryConfig] = None

class WallObstacle(CollisionObstacle):
    """Class for a spherical obstacle.
    """
    def __init__(self, **kwargs):
        schema = OmegaConf.structured(WallObstacleConfig)
        super().__init__(schema, **kwargs)
        self.check_completeness()
    
    def dimension(self):
        return len(self._config.geometry.position)
    
    def limit_low(self):
        if self._config.low:
            return [
                np.array(self._config.low.position),
                self._config.low.rotation,
                self._config.low.length,
                self._config.low.width
            ]
        else:
            return [np.ones(self.dimension()) * -1, 0]

    def limit_high(self):
        if self._config.high:
            return [
                np.array(self._config.high.position),
                self._config.high.rotation,
                self._config.high.length,
                self._config.high.width
            ]
        else:
            return [np.ones(self.dimension()) * 1, 1]
    
    def position(self, **kwargs) -> np.ndarray:
        return np.array(self._config.geometry.position)
    
    def velocity(self, **kwargs):
        return np.zeros(self.dimension())
    
    def acceleration(self, **kwargs):
        return np.zeros(self.dimension())
    
    def rotation(self, **kwargs) -> float:
        return self._config.geometry.rotation
    
    def length(self, **kwargs) -> float:
        return self._config.geometry.length
    
    def width(self, **kwargs) -> float:
        return self._config.geometry.width

    def shuffle(self):
        random_pos = np.random.uniform(
            self.limit_low()[0], self.limit_high()[0], self.dimension()
        )
        random_rotation= np.random.uniform(
            self.limit_low()[1], self.limit_high()[1], 1
        )
        random_width = np.random.uniform(
            self.limit_low()[3], self.limit_high()[3], 1
        )
        random_length = np.random.uniform(
            self.limit_low()[2], self.limit_high()[2], 1
        )
        self._config.geometry.position = random_pos.tolist()
        self._config.geometry.rotation = float(random_rotation.tolist())
        self._config.geometry.width = float(random_width.tolist())
        self._config.geometry.length = float(random_length.tolist())

    
    def movable(self):
        return self._config.movable

    def csv(self, file_name, samples=100): # TODO
        theta = np.arange(-np.pi, np.pi + np.pi / samples, step=np.pi / samples)
        x = self.position()[0] + (self.radius() - 0.1) * np.cos(theta)
        y = self.position()[1] + (self.radius() - 0.1) * np.sin(theta)
        with open(file_name, mode="w") as file:
            csv_writer = csv.writer(file, delimiter=",")
            for i in range(2 * samples):
                csv_writer.writerow([x[i], y[i]])
    
    def render_gym(self, viewer, rendering, **kwargs):
        if self.dimension() != 2:
            raise DimensionNotSuitableForEnv(
                "PlanarGym only supports two dimensional obstacles"
            )
        x = self.position()
        r = self.rotation()
        start = x + np.array([np.cos(r), np.sin(r)]) * self.length() / 2
        end = x - np.array([np.cos(r), np.sin(r)]) * self.length() / 2
        tf = rendering.Transform(rotation=r, translation=(x[0], x[1]))
        joint = viewer.draw_line(start, end) # TODO
        print("joint: start: ", start, " end: ", end)
        joint.add_attr(tf)

    def add_to_bullet(self, pybullet):
        if self.dimension() == 2:
            base_position = self.position().tolist() + [0.0]
        elif self.dimension() == 3:
            base_position = self.position().tolist()
        else:
            raise DimensionNotSuitableForEnv(
                "Pybullet only supports three dimensional obstacles"
            )
        collision_shape = pybullet.createCollisionShape(
            pybullet.GEOM_BOX, halfExtents=[self.length()/2, self.width()/2, 2.0]
        )
        visual_shape_id = -1
        base_orientation = pybullet.getQuaternionFromEuler([0, 0, self.rotation()])
        mass = int(self.movable())
        assert isinstance(base_position, list)
        # assert isinstance(base_orientation, list)
        pybullet.createMultiBody(
            mass,
            collision_shape,
            visual_shape_id,
            base_position,
            base_orientation,
        )
