import numpy as np
import glm

# Global camera state
CAM_MOV_UP = False
CAM_MOV_DOWN = False
CAM_MOV_LEFT = False
CAM_MOV_RIGHT = False
CAM_MOV_FRONT = False
CAM_MOV_BACK = False

# Global camera vectors
camera_pos = glm.vec3(1.0, 1.0, 3.0)
camera_front = glm.vec3(-0.5, 0.0, -1.0)
camera_up = glm.vec3(0.0, 1.0, 0.0)

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

    @staticmethod
    def camera_movement(cam_mov_up, cam_mov_down, cam_mov_left, cam_mov_right, cam_move_front, cam_move_back):
        global camera_pos, camera_front, camera_up

        if cam_mov_up:
            camera_pos += 0.05 * camera_up
        if cam_mov_down:
            camera_pos -= 0.05 * camera_up
        if cam_mov_left:
            camera_pos -= glm.normalize(glm.cross(camera_front, camera_up)) * 0.05
        if cam_mov_right:
            camera_pos += glm.normalize(glm.cross(camera_front, camera_up)) * 0.05
        if cam_move_front:
            print("Moving front")
            camera_pos += 0.05 * camera_front
        if cam_move_back:
            print("Moving back")
            camera_pos -= 0.05 * camera_front

