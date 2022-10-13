from MotionPlanningGoal.staticSubGoal import StaticSubGoal

goal1Dict = {
    "weight": 1.0, "is_primary_goal": True, 'indices': [0, 1, 2], 'parent_link': 0, 'child_link': 3,
    'desired_position': [1, 0, 0.1], 'epsilon': 0.02, 'type': "staticSubGoal", 
}

goal1 = StaticSubGoal(name="goal1", content_dict=goal1Dict)

