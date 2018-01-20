# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AhlCoach(models.Model):
    game = models.OneToOneField('AhlGame', models.DO_NOTHING, primary_key=True)
    home_head = models.TextField()
    home_a1 = models.TextField(blank=True, null=True)
    home_a2 = models.TextField(blank=True, null=True)
    home_a3 = models.TextField(blank=True, null=True)
    home_a4 = models.TextField(blank=True, null=True)
    visitor_head = models.TextField()
    visitor_a1 = models.TextField(blank=True, null=True)
    visitor_a2 = models.TextField(blank=True, null=True)
    visitor_a3 = models.TextField(blank=True, null=True)
    visitor_a4 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ahl_coaches'


class AhlGame(models.Model):
    game_id = models.IntegerField(primary_key=True)
    season = models.ForeignKey('AhlSeason', models.DO_NOTHING)
    game_date = models.DateField()
    home_team = models.IntegerField()
    visiting_team = models.IntegerField()
    home_goals = models.IntegerField()
    visiting_goals = models.IntegerField()
    overtime = models.IntegerField()
    shootout = models.IntegerField()
    attendance = models.IntegerField()
    period = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ahl_game'


class AhlGoal(models.Model):
    game = models.OneToOneField(AhlGame, models.DO_NOTHING, primary_key=True)
    period = models.IntegerField()
    time = models.FloatField(primary_key=True)
    team = models.IntegerField()
    scorer = models.ForeignKey('AhlPlayer', models.DO_NOTHING, db_column='scorer')
    a1 = models.IntegerField()
    a2 = models.IntegerField()
    pp = models.IntegerField()
    en = models.IntegerField()
    ps = models.IntegerField()
    sh = models.IntegerField()
    gf1 = models.IntegerField()
    gf2 = models.IntegerField()
    gf3 = models.IntegerField()
    gf4 = models.IntegerField()
    gf5 = models.IntegerField()
    gf6 = models.IntegerField()
    ga1 = models.IntegerField()
    ga2 = models.IntegerField()
    ga3 = models.IntegerField()
    ga4 = models.IntegerField()
    ga5 = models.IntegerField()
    ga6 = models.IntegerField()
    home_goals = models.IntegerField()
    visitor_goals = models.IntegerField()
    home = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ahl_goal'
        unique_together = (('game', 'time'),)


class AhlGoalieGame(models.Model):
    game = models.OneToOneField(AhlGame, models.DO_NOTHING, primary_key=True)
    player = models.OneToOneField('AhlPlayer', models.DO_NOTHING, primary_key=True)
    goals = models.IntegerField()
    assists = models.IntegerField()
    pims = models.IntegerField()
    toi = models.FloatField()
    shots = models.IntegerField()
    goals_against = models.IntegerField()
    saves = models.IntegerField()
    starter = models.IntegerField()
    status = models.TextField(blank=True, null=True)
    team_id = models.IntegerField()
    result = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ahl_goalie_games'
        unique_together = (('game', 'player'),)


class AhlLineComp(models.Model):
    player = models.OneToOneField('AhlPlayer', models.DO_NOTHING, primary_key=True)
    season = models.OneToOneField('AhlSeason', models.DO_NOTHING, primary_key=True)
    es_line = models.FloatField()
    es_comp = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ahl_line_comp'
        unique_together = (('player', 'season'),)


class AhlOfficial(models.Model):
    game = models.OneToOneField(AhlGame, models.DO_NOTHING, primary_key=True)
    referee1 = models.TextField()
    referee2 = models.TextField()
    linesman1 = models.TextField()
    linesman2 = models.TextField()

    class Meta:
        managed = False
        db_table = 'ahl_official'


class AhlPenalty(models.Model):
    game = models.OneToOneField(AhlGame, models.DO_NOTHING, primary_key=True)
    period = models.IntegerField()
    time = models.FloatField()
    player = models.OneToOneField('AhlPlayer', models.DO_NOTHING, db_column='player')
    team = models.IntegerField()
    pp = models.IntegerField()
    home = models.IntegerField()
    mins = models.FloatField()
    description = models.TextField()
    pen_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'ahl_penalty'
        unique_together = (('game', 'pen_id'),)


class AhlPlayer(models.Model):
    player_id = models.IntegerField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    birthdate = models.DateField()
    position = models.TextField()
    height = models.FloatField()
    weight = models.FloatField()
    shoots = models.TextField()
    player_name = models.TextField()
    birthplace = models.TextField()

    class Meta:
        managed = False
        db_table = 'ahl_player'


class AhlPxp(models.Model):
    game_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'ahl_pxp'


class AhlSeason(models.Model):
    season_id = models.IntegerField(primary_key=True)
    name = models.TextField()
    career = models.IntegerField()
    playoff = models.IntegerField()
    start_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ahl_season'


class AhlShootout(models.Model):
    game = models.OneToOneField(AhlGame, models.DO_NOTHING, primary_key=True)
    shooter = models.OneToOneField(AhlPlayer, models.DO_NOTHING, related_name="ahlshootout_shooter", db_column='shooter')
    shooter_team = models.IntegerField()
    goalie = models.OneToOneField(AhlPlayer, models.DO_NOTHING, related_name="ahlshootout_goalie", db_column='goalie')
    goalie_team = models.IntegerField()
    home = models.IntegerField()
    goal = models.IntegerField()
    winning_goal = models.IntegerField()
    s_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ahl_shootout'
        unique_together = (('game', 'shooter', 's_id'),)


class AhlSkaterGame(models.Model):
    game = models.OneToOneField(AhlGame, models.DO_NOTHING, primary_key=True)
    player = models.OneToOneField(AhlPlayer, models.DO_NOTHING)
    position = models.TextField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    pims = models.IntegerField()
    field_field = models.IntegerField(db_column='+/-')  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    shots = models.IntegerField()
    hits = models.IntegerField()
    starter = models.IntegerField()
    status = models.TextField(blank=True, null=True)
    team_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ahl_skater_games'
        unique_together = (('game', 'player'),)


class AhlStar(models.Model):
    game = models.OneToOneField(AhlGame, models.DO_NOTHING, primary_key=True)
    first = models.OneToOneField(AhlPlayer, models.DO_NOTHING, related_name="ahlstars_first", db_column='first')
    second = models.OneToOneField(AhlPlayer, models.DO_NOTHING, related_name="ahlstars_second", db_column='second')
    third = models.OneToOneField(AhlPlayer, models.DO_NOTHING, related_name="ahlstars_third", db_column='third')

    class Meta:
        managed = False
        db_table = 'ahl_stars'


class AhlTeam(models.Model):
    season = models.OneToOneField(AhlSeason, models.DO_NOTHING, primary_key=True)
    team = models.OneToOneField('self', models.DO_NOTHING)
    name = models.TextField()
    division_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ahl_team'
        unique_together = (('season', 'team'),)


class AhlTeamGameTotal(models.Model):
    game = models.OneToOneField(AhlGame, models.DO_NOTHING, primary_key=True)
    home_shots = models.IntegerField()
    home_hits = models.IntegerField()
    home_ppg = models.IntegerField()
    home_ppo = models.IntegerField()
    home_goals = models.IntegerField()
    home_assists = models.IntegerField()
    home_pims = models.IntegerField()
    home_penalties = models.IntegerField()
    visitor_shots = models.IntegerField()
    visitor_hits = models.IntegerField()
    visitor_ppg = models.IntegerField()
    visitor_ppo = models.IntegerField()
    visitor_goals = models.IntegerField()
    visitor_assists = models.IntegerField()
    visitor_pims = models.IntegerField()
    visitor_penalties = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ahl_team_game_totals'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class NhlBlock(models.Model):
    game = models.OneToOneField('NhlGame', models.DO_NOTHING, primary_key=True)
    event_id = models.IntegerField()
    team = models.ForeignKey('NhlTeam', models.DO_NOTHING)
    blocker = models.ForeignKey('NhlPlayer', models.DO_NOTHING, related_name="nhlblock_blocker", db_column='blocker')
    shooter = models.ForeignKey('NhlPlayer', models.DO_NOTHING, related_name="nhlblock_shooter", db_column='shooter')
    period = models.IntegerField()
    time = models.FloatField()
    away_goals = models.IntegerField()
    home_goals = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()

    class Meta:
        managed = False
        db_table = 'nhl_block'
        unique_together = (('game', 'event_id'),)


class NhlFaceoff(models.Model):
    game = models.OneToOneField('NhlGame', models.DO_NOTHING, primary_key=True)
    event_id = models.IntegerField()
    team = models.ForeignKey('NhlTeam', models.DO_NOTHING)
    winner = models.ForeignKey('NhlPlayer', models.DO_NOTHING, related_name="nhlfaceoff_winner", db_column='winner')
    loser = models.ForeignKey('NhlPlayer', models.DO_NOTHING, related_name="nhlfaceoff_loser", db_column='loser')
    period = models.IntegerField()
    time = models.FloatField()
    away_goals = models.IntegerField()
    home_goals = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()

    class Meta:
        managed = False
        db_table = 'nhl_faceoff'
        unique_together = (('game', 'event_id'),)


class NhlFranchise(models.Model):
    franchise_id = models.IntegerField(primary_key=True)
    first_season = models.IntegerField()
    recent_team = models.IntegerField()
    team_name = models.TextField()
    location = models.TextField()

    class Meta:
        managed = False
        db_table = 'nhl_franchise'


class NhlGame(models.Model):
    game_id = models.IntegerField(primary_key=True)
    season = models.ForeignKey('NhlSeason', models.DO_NOTHING)
    type = models.TextField()
    game_date = models.DateField()
    away_team = models.ForeignKey('NhlTeam', models.DO_NOTHING, related_name="nhlgame_away_team", db_column='away_team')
    away_goals = models.IntegerField()
    home_team = models.ForeignKey('NhlTeam', models.DO_NOTHING, related_name="nhlgame_home_team", db_column='home_team')
    home_goals = models.IntegerField()
    venue = models.TextField()

    class Meta:
        managed = False
        db_table = 'nhl_game'


class NhlGiveaway(models.Model):
    game = models.OneToOneField(NhlGame, models.DO_NOTHING, primary_key=True)
    event_id = models.IntegerField()
    team = models.ForeignKey('NhlTeam', models.DO_NOTHING)
    culprit = models.ForeignKey('NhlPlayer', models.DO_NOTHING, db_column='culprit')
    period = models.IntegerField()
    time = models.FloatField()
    away_goals = models.IntegerField()
    home_goals = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()

    class Meta:
        managed = False
        db_table = 'nhl_giveaway'
        unique_together = (('game', 'event_id'),)


class NhlGoal(models.Model):
    game = models.OneToOneField(NhlGame, models.DO_NOTHING, primary_key=True)
    event_id = models.IntegerField()
    team = models.ForeignKey('NhlTeam', models.DO_NOTHING)
    scorer = models.ForeignKey('NhlPlayer', models.DO_NOTHING, db_column='scorer')
    goalie = models.IntegerField()
    period = models.IntegerField()
    time = models.FloatField()
    away_goals = models.IntegerField()
    home_goals = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()
    shot = models.TextField()
    a1 = models.IntegerField()
    a2 = models.IntegerField()
    situation = models.TextField()
    gwg = models.BooleanField()
    en = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'nhl_goal'
        unique_together = (('game', 'event_id'),)


class NhlGoalieSummary(models.Model):
    game = models.OneToOneField(NhlGame, models.DO_NOTHING, primary_key=True)
    location = models.TextField()
    team = models.ForeignKey('NhlTeam', models.DO_NOTHING)
    player = models.ForeignKey('NhlPlayer', models.DO_NOTHING)
    num = models.IntegerField()
    toi = models.FloatField()
    assists = models.IntegerField()
    goals = models.IntegerField()
    pim = models.IntegerField()
    shots = models.IntegerField()
    saves = models.IntegerField()
    ppsv = models.IntegerField()
    shsv = models.IntegerField()
    evsv = models.IntegerField()
    shsa = models.IntegerField()
    evsa = models.IntegerField()
    ppsa = models.IntegerField()
    decision = models.TextField()
    svpct = models.FloatField()
    ev_svpct = models.FloatField()

    class Meta:
        managed = False
        db_table = 'nhl_goalie_summary'
        unique_together = (('game', 'player'),)


class NhlHeadCoach(models.Model):
    game = models.OneToOneField(NhlGame, models.DO_NOTHING, primary_key=True)
    away = models.TextField()
    home = models.TextField()

    class Meta:
        managed = False
        db_table = 'nhl_head_coach'


class NhlHit(models.Model):
    game = models.OneToOneField(NhlGame, models.DO_NOTHING, primary_key=True)
    event_id = models.IntegerField()
    team = models.ForeignKey('NhlTeam', models.DO_NOTHING)
    hitter = models.ForeignKey('NhlPlayer', models.DO_NOTHING, related_name="nhlhit_hitter", db_column='hitter')
    hittee = models.ForeignKey('NhlPlayer', models.DO_NOTHING, related_name="nhlhit_hittee", db_column='hittee')
    period = models.IntegerField()
    time = models.FloatField()
    away_goals = models.IntegerField()
    home_goals = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()

    class Meta:
        managed = False
        db_table = 'nhl_hit'
        unique_together = (('game', 'event_id'),)


class NhlMiss(models.Model):
    game = models.OneToOneField(NhlGame, models.DO_NOTHING, primary_key=True)
    event_id = models.IntegerField()
    team = models.ForeignKey('NhlTeam', models.DO_NOTHING)
    culprit = models.ForeignKey('NhlPlayer', models.DO_NOTHING, db_column='culprit')
    period = models.IntegerField()
    time = models.FloatField()
    away_goals = models.IntegerField()
    home_goals = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()

    class Meta:
        managed = False
        db_table = 'nhl_miss'
        unique_together = (('game', 'event_id'),)


class NhlOfficial(models.Model):
    game = models.OneToOneField(NhlGame, models.DO_NOTHING, primary_key=True)
    referee1_id = models.IntegerField()
    referee2_id = models.IntegerField()
    linesman1_id = models.IntegerField()
    linesman2_id = models.IntegerField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nhl_officials'


class NhlPenalty(models.Model):
    game = models.OneToOneField(NhlGame, models.DO_NOTHING, primary_key=True)
    event_id = models.IntegerField()
    team = models.ForeignKey('NhlTeam', models.DO_NOTHING)
    taker = models.ForeignKey('NhlPlayer', models.DO_NOTHING, related_name="nhlpenalty_taker", db_column='taker')
    drawer = models.ForeignKey('NhlPlayer', models.DO_NOTHING, related_name="nhlpenalty_drawer", db_column='drawer')
    period = models.IntegerField()
    time = models.FloatField()
    away_goals = models.IntegerField()
    home_goals = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()
    penalty = models.TextField()
    minutes = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nhl_penalty'
        unique_together = (('game', 'event_id'),)


class NhlPlayer(models.Model):
    player_id = models.IntegerField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    birthdate = models.DateField()
    shoots = models.TextField()  # This field type is a guess.
    player_name = models.TextField()
    town = models.TextField()
    province = models.TextField()
    country = models.TextField()

    class Meta:
        managed = False
        db_table = 'nhl_player'


class NhlPlayerBio(models.Model):
    player = models.OneToOneField(NhlPlayer, models.DO_NOTHING, primary_key=True)
    season = models.ForeignKey('NhlSeason', models.DO_NOTHING)
    height = models.FloatField()
    weight = models.IntegerField()
    active = models.BooleanField()
    rookie = models.BooleanField()
    roster_status = models.TextField()  # This field type is a guess.
    position = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'nhl_player_bio'
        unique_together = (('player', 'season'),)


class NhlPlayerDressed(models.Model):
    player = models.OneToOneField(NhlPlayer, models.DO_NOTHING, primary_key=True)
    game = models.ForeignKey(NhlGame, models.DO_NOTHING)
    num = models.IntegerField()
    age = models.IntegerField()
    assistant = models.BooleanField()
    captain = models.BooleanField()
    rookie = models.BooleanField()
    team = models.ForeignKey('NhlTeam', models.DO_NOTHING, db_column='team')
    position = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'nhl_player_dressed'
        unique_together = (('player', 'game'),)


class NhlRinkSide(models.Model):
    game = models.OneToOneField(NhlGame, models.DO_NOTHING, primary_key=True)
    period = models.IntegerField()
    team = models.ForeignKey('NhlTeam', models.DO_NOTHING)
    rink_side = models.TextField()

    class Meta:
        managed = False
        db_table = 'nhl_rink_side'
        unique_together = (('game', 'period', 'team'),)


class NhlSeason(models.Model):
    season_id = models.IntegerField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    games = models.IntegerField()
    ties = models.BooleanField()
    olympics = models.BooleanField()
    conferences = models.BooleanField()
    divisions = models.BooleanField()
    wild_cards = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'nhl_season'


class NhlShift(models.Model):
    game = models.OneToOneField(NhlGame, models.DO_NOTHING, primary_key=True)
    shift_id = models.IntegerField()
    player = models.ForeignKey(NhlPlayer, models.DO_NOTHING)
    team = models.ForeignKey('NhlTeam', models.DO_NOTHING)
    num = models.IntegerField()
    period = models.IntegerField()
    start_time = models.FloatField()
    end_time = models.FloatField()
    duration = models.FloatField()
    code = models.IntegerField()
    event = models.TextField()
    details = models.TextField()
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'nhl_shift'
        unique_together = (('game', 'shift_id', 'player', 'num'),)


class NhlShootout(models.Model):
    game = models.OneToOneField(NhlGame, models.DO_NOTHING, primary_key=True)
    event_id = models.IntegerField()
    team = models.ForeignKey('NhlTeam', models.DO_NOTHING)
    shooter = models.ForeignKey(NhlPlayer, models.DO_NOTHING, related_name="nhlshootout_shooter", db_column='shooter')
    goalie = models.ForeignKey(NhlPlayer, models.DO_NOTHING, related_name="nhlshootout_goalie", db_column='goalie')
    x = models.FloatField()
    y = models.FloatField()
    shot = models.TextField()
    result = models.TextField()

    class Meta:
        managed = False
        db_table = 'nhl_shootout'
        unique_together = (('game', 'event_id'),)


class NhlShot(models.Model):
    game = models.OneToOneField(NhlGame, models.DO_NOTHING, primary_key=True)
    event_id = models.IntegerField()
    team = models.ForeignKey('NhlTeam', models.DO_NOTHING)
    shooter = models.ForeignKey(NhlPlayer, models.DO_NOTHING, related_name="nhlshot_shooter", db_column='shooter')
    goalie = models.ForeignKey(NhlPlayer, models.DO_NOTHING, related_name="nhlshot_goalie", db_column='goalie')
    period = models.IntegerField()
    time = models.FloatField()
    away_goals = models.IntegerField()
    home_goals = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()
    shot = models.TextField()

    class Meta:
        managed = False
        db_table = 'nhl_shot'
        unique_together = (('game', 'event_id'),)


class NhlSkaterSummary(models.Model):
    game = models.OneToOneField(NhlGame, models.DO_NOTHING, primary_key=True)
    location = models.TextField()
    team = models.ForeignKey('NhlTeam', models.DO_NOTHING, db_column='team')
    player = models.ForeignKey(NhlPlayer, models.DO_NOTHING)
    num = models.IntegerField()
    position = models.TextField()
    toi = models.FloatField()
    assists = models.IntegerField()
    goals = models.IntegerField()
    shots = models.IntegerField()
    hits = models.IntegerField()
    ppg = models.IntegerField()
    ppa = models.IntegerField()
    pim = models.IntegerField()
    fow = models.IntegerField()
    fot = models.IntegerField()
    ta = models.IntegerField()
    ga = models.IntegerField()
    shg = models.IntegerField()
    sha = models.IntegerField()
    blocks = models.IntegerField()
    plus_minus = models.IntegerField()
    ev_toi = models.FloatField()
    pp_toi = models.FloatField()
    sh_toi = models.FloatField()

    class Meta:
        managed = False
        db_table = 'nhl_skater_summary'
        unique_together = (('game', 'player'),)


class NhlStar(models.Model):
    game = models.OneToOneField(NhlGame, models.DO_NOTHING, primary_key=True)
    first_star = models.ForeignKey(NhlPlayer, models.DO_NOTHING, related_name="nhlstars_first", db_column='first_star')
    second_star = models.ForeignKey(NhlPlayer, models.DO_NOTHING, related_name="nhlstars_second", db_column='second_star')
    third_star = models.ForeignKey(NhlPlayer, models.DO_NOTHING, related_name="nhlstars_third", db_column='third_star')

    class Meta:
        managed = False
        db_table = 'nhl_stars'


class NhlTakeaway(models.Model):
    game = models.OneToOneField(NhlGame, models.DO_NOTHING, primary_key=True)
    event_id = models.IntegerField()
    team = models.ForeignKey('NhlTeam', models.DO_NOTHING)
    taker = models.ForeignKey(NhlPlayer, models.DO_NOTHING, db_column='taker')
    period = models.IntegerField()
    time = models.FloatField()
    away_goals = models.IntegerField()
    home_goals = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()

    class Meta:
        managed = False
        db_table = 'nhl_takeaway'
        unique_together = (('game', 'event_id'),)


class NhlTeam(models.Model):
    team_id = models.IntegerField(primary_key=True)
    name = models.TextField()
    abbreviation = models.TextField()
    nickname = models.TextField()
    location = models.TextField()
    first_year = models.IntegerField()
    franchise = models.ForeignKey(NhlFranchise, models.DO_NOTHING)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'nhl_team'


class NhlTeamSummary(models.Model):
    away_team = models.OneToOneField(NhlTeam, models.DO_NOTHING, related_name="nhlteamsummary_away_team", db_column='away_team')
    home_team = models.ForeignKey(NhlTeam, models.DO_NOTHING, related_name="nhlteamsummary_home_team", db_column='home_team')
    away_goals = models.IntegerField()
    home_goals = models.IntegerField()
    away_pim = models.IntegerField()
    home_pim = models.IntegerField()
    away_shots = models.IntegerField()
    home_shots = models.IntegerField()
    away_ppg = models.IntegerField()
    home_ppg = models.IntegerField()
    away_ppo = models.IntegerField()
    home_ppo = models.IntegerField()
    away_blocks = models.IntegerField()
    home_blocks = models.IntegerField()
    away_ta = models.IntegerField()
    home_ta = models.IntegerField()
    away_ga = models.IntegerField()
    home_ga = models.IntegerField()
    away_hits = models.IntegerField()
    home_hits = models.IntegerField()
    game = models.OneToOneField(NhlGame, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'nhl_team_summary'


class OhlFaceoff(models.Model):
    game = models.OneToOneField('OhlGame', models.DO_NOTHING, primary_key=True)
    period = models.IntegerField()
    time = models.FloatField()
    home_player = models.ForeignKey('OhlPlayer', models.DO_NOTHING, related_name="ohlfaceoff_home_player", db_column='home_player')
    visitor_player = models.ForeignKey('OhlPlayer', models.DO_NOTHING, related_name="ohlfaceoff_away_player", db_column='visitor_player')
    home_win = models.IntegerField()
    location = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    home_team = models.IntegerField()
    visitor_team = models.IntegerField()
    home_goals = models.IntegerField()
    visitor_goals = models.IntegerField()
    fo_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ohl_faceoff'
        unique_together = (('game', 'fo_id'),)


class OhlGame(models.Model):
    game_id = models.IntegerField(primary_key=True)
    season = models.ForeignKey('OhlSeason', models.DO_NOTHING)
    game_date = models.DateField()
    home_team = models.ForeignKey('OhlTeam', models.DO_NOTHING, related_name="ohlgame_home_team", db_column='home_team')
    visiting_team = models.ForeignKey('OhlTeam', models.DO_NOTHING, related_name="ohlgame_visiting_team", db_column='visiting_team')
    home_goals = models.IntegerField()
    visiting_goals = models.IntegerField()
    period = models.IntegerField()
    overtime = models.IntegerField()
    shootout = models.IntegerField()
    attendance = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ohl_game'


class OhlGoal(models.Model):
    game = models.OneToOneField(OhlGame, models.DO_NOTHING, primary_key=True)
    period = models.IntegerField()
    time = models.FloatField()
    team = models.IntegerField()
    scorer = models.ForeignKey('OhlPlayer', models.DO_NOTHING, related_name="ohlgoal_scorer", db_column='scorer')
    a1 = models.ForeignKey('OhlPlayer', models.DO_NOTHING, related_name="ohlgoal_a1", db_column='a1')
    a2 = models.ForeignKey('OhlPlayer', models.DO_NOTHING, related_name="ohlgoal_a2", db_column='a2')
    x = models.IntegerField()
    y = models.IntegerField()
    location = models.IntegerField()
    pp = models.IntegerField()
    en = models.IntegerField()
    ps = models.IntegerField()
    sh = models.IntegerField()
    gf1 = models.IntegerField()
    gf2 = models.IntegerField()
    gf3 = models.IntegerField()
    gf4 = models.IntegerField()
    gf5 = models.IntegerField()
    gf6 = models.IntegerField()
    ga1 = models.IntegerField()
    ga2 = models.IntegerField()
    ga3 = models.IntegerField()
    ga4 = models.IntegerField()
    ga5 = models.IntegerField()
    ga6 = models.IntegerField()
    home_goals = models.IntegerField()
    visitor_goals = models.IntegerField()
    home = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ohl_goal'
        unique_together = (('game', 'time'),)


class OhlGoalieChange(models.Model):
    game = models.OneToOneField(OhlGame, models.DO_NOTHING, primary_key=True)
    goalie_in = models.IntegerField(blank=True, null=True)
    goalie_out = models.IntegerField(blank=True, null=True)
    period = models.IntegerField()
    time = models.FloatField()
    team = models.IntegerField()
    home_goals = models.IntegerField()
    visitor_goals = models.IntegerField()
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'ohl_goalie_change'
        unique_together = (('game', 'time', 'team', 'id'),)


class OhlPenalty(models.Model):
    game = models.OneToOneField(OhlGame, models.DO_NOTHING, primary_key=True)
    period = models.IntegerField()
    time = models.FloatField()
    player = models.ForeignKey('OhlPlayer', models.DO_NOTHING, db_column='player')
    team = models.IntegerField()
    offence = models.IntegerField()
    pp = models.IntegerField()
    ps = models.IntegerField()
    bench = models.IntegerField()
    home = models.IntegerField()
    mins = models.FloatField()
    description = models.TextField()
    class_field = models.TextField(db_column='class')  # Field renamed because it was a Python reserved word.
    home_goals = models.IntegerField()
    visitor_goals = models.IntegerField()
    pen_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ohl_penalty'
        unique_together = (('game', 'pen_id'),)


class OhlPenaltyshot(models.Model):
    game_id = models.IntegerField(primary_key=True)
    shooter = models.IntegerField()
    goalie = models.IntegerField()
    time = models.FloatField()
    home = models.IntegerField()
    period = models.IntegerField()
    goal = models.IntegerField()
    shooter_team = models.IntegerField()
    goalie_team = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ohl_penaltyshot'
        unique_together = (('game_id', 'time'),)


class OhlPlayer(models.Model):
    player_id = models.IntegerField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    birthdate = models.DateField()
    position = models.TextField()
    height = models.FloatField()
    weight = models.FloatField()
    shoots = models.TextField()
    player_name = models.TextField()
    town = models.TextField()
    province = models.TextField()
    country = models.TextField()

    class Meta:
        managed = False
        db_table = 'ohl_player'


class OhlPxp(models.Model):
    game = models.OneToOneField(OhlGame, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'ohl_pxp'


class OhlSeason(models.Model):
    season_id = models.IntegerField(primary_key=True)
    name = models.TextField()
    career = models.IntegerField()
    playoff = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'ohl_season'


class OhlShootout(models.Model):
    game = models.OneToOneField(OhlGame, models.DO_NOTHING, primary_key=True)
    shooter = models.ForeignKey(OhlPlayer, models.DO_NOTHING, related_name="ohlshootout_shooter", db_column='shooter')
    shooter_team = models.IntegerField()
    goalie = models.ForeignKey(OhlPlayer, models.DO_NOTHING, related_name="ohlshootout_goalie", db_column='goalie')
    goalie_team = models.IntegerField()
    home = models.IntegerField()
    shot_order = models.IntegerField()
    shot = models.IntegerField()
    goal = models.IntegerField()
    winning_goal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ohl_shootout'
        unique_together = (('game', 'shot'),)


class OhlShot(models.Model):
    game = models.OneToOneField(OhlGame, models.DO_NOTHING, primary_key=True)
    shooter = models.ForeignKey(OhlPlayer, models.DO_NOTHING, related_name="ohlshot_shooter", db_column='shooter')
    goalie = models.ForeignKey(OhlPlayer, models.DO_NOTHING, related_name="ohlshot_goalie", db_column='goalie')
    home = models.IntegerField()
    team = models.IntegerField()
    period = models.IntegerField()
    time = models.FloatField()
    x = models.IntegerField()
    y = models.IntegerField()
    shot = models.IntegerField()
    quality = models.IntegerField()
    goal = models.IntegerField()
    opponent = models.IntegerField()
    home_goals = models.IntegerField()
    visitor_goals = models.IntegerField()
    shot_id = models.IntegerField()
    adj_x = models.IntegerField(blank=True, null=True)
    adj_y = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ohl_shot'
        unique_together = (('game', 'shot_id'),)


class OhlTeam(models.Model):
    season = models.OneToOneField(OhlSeason, models.DO_NOTHING, primary_key=True)
    team_id = models.IntegerField()
    name = models.TextField()
    code = models.TextField()
    city = models.TextField()
    nickname = models.TextField()

    class Meta:
        managed = False
        db_table = 'ohl_team'
        unique_together = (('season', 'team_id'),)
