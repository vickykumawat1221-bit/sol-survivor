"""
Database models for Sol Survivor: AI-Powered Mars Mission Digital Twin & Space Academy.
Stores mission sessions, step-by-step history replay logs, active repair missions,
STEM quiz progress, and Space Academy educational mini-game profiles, scores, and badges.
"""

from django.db import models
import uuid

class MissionSession(models.Model):
    ROLE_CHOICES = [
        ('COMMANDER', 'Mission Commander'),
        ('ENGINEER', 'Flight & Power Engineer'),
        ('SCIENTIST', 'Astrobiologist & Life Support Specialist'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active Mission'),
        ('WON', 'Mission Accomplished'),
        ('LOST', 'Mission Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_key = models.CharField(max_length=128, db_index=True)
    commander_name = models.CharField(max_length=64, default='Junior Commander')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='COMMANDER')
    level = models.IntegerField(default=1)
    unlocked_level = models.IntegerField(default=1)
    sol = models.IntegerField(default=1)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='ACTIVE')
    fail_reason = models.TextField(blank=True, default='')
    xp = models.IntegerField(default=0)
    crises_handled = models.IntegerField(default=0)
    clutch_count = models.IntegerField(default=0)
    state_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.commander_name} ({self.role}) - Level {self.level} Sol {self.sol} [{self.status}]"


class MissionStepLog(models.Model):
    """
    Immutable step-by-step log of every Sol turn for complete replay and post-mission analysis.
    """
    mission = models.ForeignKey(MissionSession, on_delete=models.CASCADE, related_name='steps')
    sol = models.IntegerField()
    action_taken = models.CharField(max_length=64)
    action_label = models.CharField(max_length=128, blank=True, default='')
    resources_before = models.JSONField(default=dict)
    resources_after = models.JSONField(default=dict)
    active_crises = models.JSONField(default=list, blank=True)
    ai_recommendation = models.JSONField(default=dict, blank=True)
    log_messages = models.JSONField(default=list, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sol']

    def __str__(self):
        return f"Mission {self.mission.id} - Sol {self.sol} ({self.action_taken})"


class RepairMission(models.Model):
    """
    Optional EVA or robotic field repair missions with deadlines, resource costs, and habitat health restoration.
    """
    mission = models.ForeignKey(MissionSession, on_delete=models.CASCADE, related_name='repairs')
    title = models.CharField(max_length=128)
    subsystem = models.CharField(max_length=64)
    description = models.TextField()
    sol_issued = models.IntegerField()
    sol_deadline = models.IntegerField()
    power_cost = models.IntegerField(default=10)
    water_cost = models.IntegerField(default=0)
    status = models.CharField(max_length=16, default='AVAILABLE')  # AVAILABLE, ACTIVE, COMPLETED, FAILED
    health_restore = models.IntegerField(default=25)
    xp_reward = models.IntegerField(default=150)

    def __str__(self):
        return f"{self.title} [{self.status}] for Sol {self.sol_deadline}"


class STEMQuizRecord(models.Model):
    """
    Records student educational quiz attempts, mastery scores, and age-adapted learning achievements.
    """
    session = models.ForeignKey(MissionSession, on_delete=models.CASCADE, related_name='quizzes')
    topic = models.CharField(max_length=64)
    question = models.TextField()
    user_answer = models.CharField(max_length=128)
    correct_answer = models.CharField(max_length=128)
    is_correct = models.BooleanField()
    xp_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic}: {'PASS' if self.is_correct else 'FAIL'}"


# ==============================================================================
# SPACE ACADEMY MODELS
# ==============================================================================

class AcademyProfile(models.Model):
    """
    Learner profile for Space Academy tracking age group, selected difficulty,
    total earned Academy XP, and overall completion statistics.
    """
    AGE_CHOICES = [
        ('8-10', 'Junior Cadet (Ages 8-10)'),
        ('11-13', 'Flight Specialist (Ages 11-13)'),
        ('14-16', 'Mission Commander (Ages 14-16)'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'Cadet (Easy)'),
        ('medium', 'Engineer (Medium)'),
        ('hard', 'Commander (Hard)'),
    ]

    session_key = models.CharField(max_length=128, unique=True, db_index=True)
    callsign = models.CharField(max_length=64, default='Space Cadet')
    age_group = models.CharField(max_length=16, choices=AGE_CHOICES, default='11-13')
    difficulty = models.CharField(max_length=16, choices=DIFFICULTY_CHOICES, default='medium')
    total_academy_xp = models.IntegerField(default=0)
    games_completed_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-total_academy_xp']

    def __str__(self):
        return f"{self.callsign} [{self.age_group} | {self.difficulty}] - {self.total_academy_xp} XP"


class AcademyGameScore(models.Model):
    """
    Stores individual game attempt scores, time spent, completion status, and validated XP.
    """
    GAME_IDS = [
        ('planet_explorer', 'Planet Explorer'),
        ('zero_gravity', 'Zero Gravity Challenge'),
        ('rocket_builder', 'Rocket Builder'),
        ('mars_rover', 'Mars Rover Adventure'),
        ('asteroid_defender', 'Asteroid Defender'),
        ('save_astronaut', 'Save The Astronaut'),
        ('gravity_orbit_lab', 'Gravity & Orbit Lab'),
        ('space_quiz_battle', 'Space Quiz Battle'),
    ]

    profile = models.ForeignKey(AcademyProfile, on_delete=models.CASCADE, related_name='scores')
    game_id = models.CharField(max_length=64, db_index=True)
    score = models.IntegerField(default=0)
    max_possible_score = models.IntegerField(default=100)
    completed = models.BooleanField(default=False)
    accuracy_pct = models.FloatField(default=0.0)
    time_seconds = models.IntegerField(default=0)
    xp_awarded = models.IntegerField(default=0)
    details_json = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', '-timestamp']

    def __str__(self):
        return f"{self.profile.callsign} - {self.game_id}: {self.score} pts (+{self.xp_awarded} XP)"


class AcademyAchievement(models.Model):
    """
    Unlocked achievement badges with NASA learning milestones and dates earned.
    """
    profile = models.ForeignKey(AcademyProfile, on_delete=models.CASCADE, related_name='achievements')
    achievement_id = models.CharField(max_length=64, db_index=True)
    title = models.CharField(max_length=128)
    description = models.TextField()
    icon = models.CharField(max_length=32, default='🏆')
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'achievement_id')
        ordering = ['-unlocked_at']

    def __str__(self):
        return f"{self.profile.callsign} earned {self.title}"


class AcademyDailyChallenge(models.Model):
    """
    Rotating daily educational challenges to encourage daily engagement.
    """
    profile = models.ForeignKey(AcademyProfile, on_delete=models.CASCADE, related_name='challenges')
    challenge_date = models.DateField(db_index=True)
    challenge_key = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    description = models.TextField()
    target_count = models.IntegerField(default=1)
    current_count = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    xp_reward = models.IntegerField(default=150)

    class Meta:
        unique_together = ('profile', 'challenge_date', 'challenge_key')

    def __str__(self):
        return f"{self.title} ({self.current_count}/{self.target_count}) [{'DONE' if self.is_completed else 'ACTIVE'}]"
