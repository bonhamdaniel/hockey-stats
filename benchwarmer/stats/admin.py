from django.contrib import admin
from .models import AhlCoach, AhlGame, AhlGoal, AhlGoalieGame, AhlOfficial, AhlPenalty, AhlPlayer, AhlPxp, AhlSeason, AhlShootout, AhlSkaterGame, AhlStar, AhlTeam, AhlTeamGameTotal, NhlBlock, NhlFaceoff, NhlFranchise, NhlGame, NhlGiveaway, NhlGoal, NhlGoalieSummary, NhlHeadCoach, NhlHit, NhlMiss, NhlOfficial, NhlPenalty, NhlPlayer, NhlPlayerBio, NhlPlayerDressed, NhlRinkSide, NhlSeason, NhlShift, NhlShootout, NhlShot, NhlSkaterSummary, NhlStar, NhlTakeaway, NhlTeam, NhlTeamSummary

# Register your models here.
# AHL Models
admin.site.register(AhlCoach)
admin.site.register(AhlGame)
admin.site.register(AhlGoal)
admin.site.register(AhlGoalieGame)
admin.site.register(AhlOfficial)
admin.site.register(AhlPenalty)
admin.site.register(AhlPlayer)
admin.site.register(AhlPxp)
admin.site.register(AhlSeason)
admin.site.register(AhlShootout)
admin.site.register(AhlSkaterGame)
admin.site.register(AhlStar)
admin.site.register(AhlTeam)
admin.site.register(AhlTeamGameTotal)

# NHL Models

admin.site.register(NhlBlock)
admin.site.register(NhlFaceoff)
admin.site.register(NhlFranchise)
admin.site.register(NhlGame)
admin.site.register(NhlGiveaway)
admin.site.register(NhlGoal)
admin.site.register(NhlGoalieSummary)
admin.site.register(NhlHeadCoach)
admin.site.register(NhlHit)
admin.site.register(NhlMiss)
admin.site.register(NhlOfficial)
admin.site.register(NhlPenalty)
admin.site.register(NhlPlayer)
admin.site.register(NhlPlayerBio)
admin.site.register(NhlPlayerDressed)
admin.site.register(NhlRinkSide)
admin.site.register(NhlSeason)
admin.site.register(NhlShift)
admin.site.register(NhlShootout)
admin.site.register(NhlShot)
admin.site.register(NhlSkaterSummary)
admin.site.register(NhlStar)
admin.site.register(NhlTakeaway)
admin.site.register(NhlTeam)
admin.site.register(NhlTeamSummary)

# OHL Models