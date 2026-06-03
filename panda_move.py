import pybullet as p
import pybullet_data
import time

# 1. 初始化仿真环境
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)

# 2. 加载模型
plane_id = p.loadURDF("plane.urdf")
robot_id = p.loadURDF("franka_panda/panda.urdf", useFixedBase=1)
box_id = p.loadURDF("cube_small.urdf", [0.5, 0.2, 0.05], [0, 0, 0, 1])

# 3. 逆运动学求解（核心函数）
target_pos = [0.5, 0.2, 0.3]
joint_positions = p.calculateInverseKinematics(robot_id, 11, target_pos)

# 4. 关节位置控制
for i in range(200):
    for j, idx in enumerate([0,1,2,3,4,5,6]):
        p.setJointMotorControl2(
            robot_id, idx, p.POSITION_CONTROL,
            targetPosition=joint_positions[j]
        )
    p.stepSimulation()
    time.sleep(1/240.)

# 5. 夹爪控制（抓取/释放）
def control_gripper(robot_id, position):
    p.setJointMotorControl2(robot_id, 9, p.POSITION_CONTROL, targetPosition=position)
    p.setJointMotorControl2(robot_id, 10, p.POSITION_CONTROL, targetPosition=position)
    for _ in range(50):
        p.stepSimulation()
        time.sleep(1/240.)
