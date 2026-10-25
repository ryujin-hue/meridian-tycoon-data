package com.meridian.tycoon.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * Models.kt - data class Kotlin sepadan dengan skema JSON di folder schema/.
 * Salin bersama game-data/ ke app. Guna kotlinx.serialization:
 *   Json { ignoreUnknownKeys = true } untuk muat setiap fail.
 */

// ---------------------------------------------------------------- balance --
@Serializable
data class BalanceFile(
    val dataVersion: String,
    val auctionFeePct: Double,
    val auctionStartPctOfNT: Double,
    val leverageMaxPct: Double,
    val leverageInterestWeeklyPct: Double,
    val leverageCapDailyNetMultiplier: Double,
    val auctionDurationHours: Double,
    val offlineCapHours: Double,
    val upgradeCostGrowth: Double,
    val purchasedCompanyNetContributionPct: Double,
    val lostTargetRespawnHours: Double,
    val legacyPremiumMinPct: Double,
    val legacyPremiumMaxPct: Double,
    val calibration: Calibration,
    val currencies: List<Currency>,
)

@Serializable
data class Calibration(
    val activeHoursPerDay: Double,
    val salaryShareOfGrossPct: Double,
    val companyCoverageOfTargetPct: Double,
    val opsCoverageOfTargetPct: Double,
    val tolerancePct: Double,
)

@Serializable
data class Currency(
    val id: String,
    val nameKey: String,
    val descKey: String,
    val premium: Boolean,
)

// ------------------------------------------------------------------ tiers --
@Serializable
data class TiersFile(val dataVersion: String, val tiers: List<Tier>)

@Serializable
data class Tier(
    val id: String,
    val titleKey: String,
    val maxOperations: Int,
    val maxStaff: Int,
    val baseValueA: Long,
    val targetDailyNetIncome: Long,
    val reputationThreshold: Int? = null,
    val tierUpRewardDP: Int? = null,
    val rewardKey: String? = null,
)

// ---------------------------------------------------------------- sectors --
@Serializable
data class SectorsFile(val dataVersion: String, val sectors: List<Sector>)

@Serializable
data class Sector(
    val id: String,
    val nameKey: String,
    val descKey: String,
    val multiplier: Double,
    val synergySectors: List<String>,
    val colorHex: String,
)

// ------------------------------------------------------------- operations --
@Serializable
data class OperationsFile(val dataVersion: String, val operations: List<Operation>)

@Serializable
data class Operation(
    val id: String,
    val sector: String,
    val unlockTier: Int,
    val nameKey: String,
    val descKey: String,
    val baseCost: Long,
    val costGrowth: Double,
    val baseIncomePerHour: Double,
    val incomeGrowthPerLevel: Double,
    val maxLevel: Int,
)

// -------------------------------------------------------------- companies --
@Serializable
data class CompaniesFile(val dataVersion: String, val companies: List<Company>)

@Serializable
data class Company(
    val id: String,
    val nameKey: String,
    val sector: String,
    val tier: Int,
    val category: String,
    val grossIncomePerHourK: Double,
    val reputation: Int,
    val foundedYear: Int,
    val hqCityKey: String,
    val staffCount: Int,
    val descKey: String,
    val historyKey: String,
    val tags: List<String>,
    val synergySector: String,
    val ntValue: Long,
    val auctionStartPriceTM: Long,
    val paybackDays: Double,
    val formerOwnerCeoId: String? = null,
    val premiumPct: Double? = null,
)

// ---------------------------------------------------------------- ai_ceos --
@Serializable
data class AiCeosFile(val dataVersion: String, val ceos: List<AiCeo>)

@Serializable
data class AiCeo(
    val id: String,
    val nameKey: String,
    val profile: String,
    val aggression: Double,
    val maxPremiumOverNT: Double,
    val bidIncrementPct: Double,
    val entryDelayMinutes: Int,
    val favoriteSectors: List<String>,
    val tierSpeed: String,
    val bioKey: String,
    val auctionBoss: Boolean,
)

// ------------------------------------------------------------ staff_roles --
@Serializable
data class StaffRolesFile(val dataVersion: String, val roles: List<StaffRole>)

@Serializable
data class StaffRole(
    val id: String,
    val nameKey: String,
    val descKey: String,
    val passive: StaffPassive,
    val activeSkill: ActiveSkill,
    val salaryByTier: List<Int>,
    val hireBaseCostPerStarTM: Int,
    val hireTierScale: List<Int>,
)

@Serializable
data class StaffPassive(
    val statKey: String,
    val perStarPct: Double,
    val hardCapPct: Double,
    val descKey: String,
)

@Serializable
data class ActiveSkill(
    val skillId: String,
    val nameKey: String,
    val descKey: String,
    val cooldownHours: Double,
    val unlockStar: Int,
)

// ------------------------------------------------------------- staff_pool --
@Serializable
data class StaffPoolFile(val dataVersion: String, val staff: List<StaffMember>)

@Serializable
data class StaffMember(
    val id: String,
    val role: String,
    val star: Int,
    val nameKey: String,
    val bioKey: String,
)

// --------------------------------------------------------------- research --
@Serializable
data class ResearchFile(val dataVersion: String, val nodes: List<ResearchNode>)

@Serializable
data class ResearchNode(
    val id: String,
    val tree: String,
    val stage: Int,
    val nameKey: String,
    val descKey: String,
    val costDP: Int,
    val unlockTier: Int,
    val effect: ResearchEffect,
)

@Serializable
data class ResearchEffect(
    val type: String,
    val perStageValue: Double,
    val hardCapValue: Double,
)

// ----------------------------------------------------------------- events --
@Serializable
data class EventsFile(
    val dataVersion: String,
    @SerialName("stock_out") val stockOut: List<StockOut>,
    @SerialName("bidding_war") val biddingWar: List<BiddingWar>,
    @SerialName("daily_contract") val dailyContract: List<DailyContract>,
    @SerialName("weekly_target") val weeklyTarget: List<WeeklyTarget>,
    @SerialName("market_news") val marketNews: List<MarketNews>,
    @SerialName("micro_event") val microEvent: List<MicroEvent>,
)

@Serializable
data class StockOut(
    val id: String,
    val sector: String,
    val titleKey: String,
    val descKey: String,
    val durationHours: Double,
    val incomePenaltyPct: Double,
)

@Serializable
data class BiddingWar(
    val id: String,
    val titleKey: String,
    val descKey: String,
    val durationHours: Double,
    val extraCompetitorCount: Int,
    val aggressionBoostPct: Double,
)

@Serializable
data class DailyContract(
    val id: String,
    val tierBand: Int,
    val sector: String,
    val titleKey: String,
    val descKey: String,
    val durationHours: Double,
    val goal: Goal,
    val reward: DailyReward,
)

@Serializable
data class Goal(val type: String, val amount: Long)

@Serializable
data class DailyReward(val tm: Long, val dp: Int)

@Serializable
data class WeeklyTarget(
    val id: String,
    val tierBand: Int,
    val titleKey: String,
    val descKey: String,
    val durationHours: Double,
    val goal: Goal,
    val reward: WeeklyReward,
)

@Serializable
data class WeeklyReward(val dp: Int, val cosmeticRef: String? = null)

@Serializable
data class MarketNews(
    val id: String,
    val scope: String,
    val titleKey: String,
    val effect: NewsEffect? = null,
    val weight: Int,
)

@Serializable
data class NewsEffect(val incomePercentPct: Double, val durationHours: Double)

@Serializable
data class MicroEvent(
    val id: String,
    val titleKey: String,
    val descKey: String,
    val durationMinutes: Int,
    val effect: MicroEffect,
    val weight: Int,
)

@Serializable
data class MicroEffect(val type: String, val value: Double)

// ---------------------------------------------------------------- seasons --
@Serializable
data class SeasonsFile(val dataVersion: String, val seasons: List<Season>)

@Serializable
data class Season(
    val id: String,
    val nameKey: String,
    val descKey: String,
    val weeksPerSeason: Int,
    val seasonMultiplier: Double,
    val freeTrack: Track,
    val premiumTrack: Track,
)

@Serializable
data class Track(val steps: List<TrackStep>)

@Serializable
data class TrackStep(val step: Int, val rewards: List<Reward>)

@Serializable
data class Reward(val type: String, val amount: Int? = null, val ref: String? = null)

// -------------------------------------------------------------- cosmetics --
@Serializable
data class CosmeticsFile(val dataVersion: String, val cosmetics: List<Cosmetic>)

@Serializable
data class Cosmetic(
    val id: String,
    val type: String,
    val nameKey: String,
    val descKey: String,
    val fixedRarity: String,
    val priceKM: Int,
    val tierRef: Int? = null,
)

// ------------------------------------------------------------- milestones --
@Serializable
data class MilestonesFile(val dataVersion: String, val milestones: List<Milestone>)

@Serializable
data class Milestone(
    val id: String,
    val core: Boolean,
    val nameKey: String,
    val descKey: String,
    val goal: MilestoneGoal,
    val reward: MilestoneReward,
)

@Serializable
data class MilestoneGoal(val type: String, val value: Long, val sector: String? = null)

@Serializable
data class MilestoneReward(val dp: Int, val cosmeticRef: String? = null)

// --------------------------------------------------------------- tutorial --
@Serializable
data class TutorialFile(
    val dataVersion: String,
    val steps: List<TutorialStep>,
    val starterGrant: StarterGrant,
    val starterTarget: StarterTarget,
)

@Serializable
data class TutorialStep(
    val step: Int,
    val id: String,
    val titleKey: String,
    val descKey: String,
    val uiElement: String,
    val requiredAction: String,
    val rewardTM: Int? = null,
)

@Serializable
data class StarterGrant(val tm: Long, val noteKey: String? = null)

@Serializable
data class StarterTarget(
    val special: Boolean,
    val featuredTier: Int,
    val maxStartPriceTM: Long,
    val noAiBidsMinutes: Int,
    val firstPurchaseWithinMinutes: Int,
    val noteKey: String? = null,
)

// ------------------------------------------------------- leaderboard_bots --
@Serializable
data class LeaderboardFile(
    val dataVersion: String,
    val leagueSize: Int,
    val bots: List<LeaderboardBot>,
    val namePool: List<NamePoolEntry>,
)

@Serializable
data class LeaderboardBot(
    val id: String,
    val nameKey: String,
    val tier: Int,
    val weeklyScoreBase: Long,
    val weeklyScoreVariance: Long,
    val style: String,
)

@Serializable
data class NamePoolEntry(val index: Int, val nameKey: String)

// ------------------------------------------------------------------- i18n --
@Serializable
data class I18nFile(
    val dataVersion: String,
    val lang: String,
    val strings: Map<String, String>,
)
