import numpy as np
import glm

class Camera:
    @staticmethod
    def rotate_pitch(camera_front, angle):
        yaw_pitch = np.radians(angle)

        R_pitch = np.array([[1, 0, 0],
                            [0, np.cos(yaw_pitch), -np.sin(yaw_pitch)],
                            [0, np.sin(yaw_pitch), np.cos(yaw_pitch)]])

        return glm.vec3(R_pitch @ camera_front)

    @staticmethod
    def rotate_yaw(camera_front, angle):
        yaw_rad = np.radians(angle)

        R_yaw = np.array([[np.cos(yaw_rad), 0, np.sin(yaw_rad)],
                          [0, 1, 0],
                          [-np.sin(yaw_rad), 0, np.cos(yaw_rad)]])

        return glm.vec3(R_yaw @ camera_front)

