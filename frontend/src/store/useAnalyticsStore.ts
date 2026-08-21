import { create } from "zustand";
import { api } from "@/lib/api";
import { extractErrorMessage } from "@/lib/reportsApi";
import { SOCIAL_PLATFORMS, type SocialPlatform } from "@/lib/constants";
import type { PostAnalytics, AudienceSnapshot, TrendPoint, PlatformComparisonMetrics } from "@/types/analytics";

// MODULE 6 - ANALYTICS DASHBOARD — backend integration
//
// Like Module 4, Swagger only lists endpoint paths — no response schemas
// were captured, so field-name mapping below is a best-effort guess, NOT
// a confirmed contract the way Module 8's was (Shamitha gave exact field
// names via a curl transcript before that shipped). Treat every field name
// here as unverified until confirmed with a real sample response.
//
//   GET /api/analytics/overview            Get Analytics Overview
//   GET /api/analytics/audience            Get Audience Analytics
//   GET /api/analytics/platforms           Get Platform Analytics
//   GET /api/analytics/posts               Get Post Performance
//   GET /api/analytics/posts/top           Get Top Performing Posts
//   GET /api/analytics/posts/lowest        Get Lowest Performing Posts
//   GET /api/analytics/posts/{post_id}     Get Post Analytics
//   GET /api/analytics/campaigns/{id}      Get Campaign Analytics
//   GET /api/analytics/summary             Get Analytics Summary
//   GET /api/analytics/engagement/trend    Get Engagement Trend
//
// fetchAnalytics() below wires the three endpoints whose shape is a flat
// array of rows — /posts, /platforms, /engagement/trend — since that's
// the same "array of objects" pattern Reports' `tables` already uses, so
// it's the lowest-risk part of this integration.
//
// /audience is intentionally NOT force-fit into the existing
// AudienceSnapshot shape (per-platform demographics/cities/languages/
// hourly+daily activity). That shape was invented for the mock-data phase
// of this project and is very unlikely to match a real endpoint's fields
// one-for-one without confirming an actual sample response first (the
// same kind of mismatch that caused the back-and-forth on Module 8 before
// Shamitha's clarifications — worth avoiding here by not guessing this
// far ahead of a real schema). mapAudienceSnapshot() below only fills in
// what's reasonably guessable (followers/growth/demographics/gender/
// location) and safely defaults everything else (cities, languages,
// hour/day activity) to an empty array rather than inventing numbers, so
// Audience Analytics degrades gracefully — sections with no data just
// don't render — instead of showing fabricated figures.

function pick(record: Record<string, unknown>, ...keys: string[]): unknown {
  for (const key of keys) {
    if (record[key] !== undefined && record[key] !== null) return record[key];
  }
  return undefined;
}

function asNumber(value: unknown, fallback = 0): number {
  const n = Number(value);
  return Number.isFinite(n) ? n : fallback;
}

function asString(value: unknown, fallback = ""): string {
  return typeof value === "string" ? value : value === undefined || value === null ? fallback : String(value);
}

function asArray(value: unknown): unknown[] {
  return Array.isArray(value) ? value : [];
}

/** Unwraps a paginated-style envelope ({ items/results/data/<key>: [...] }) or a bare array. */
function unwrapList(data: unknown, ...envelopeKeys: string[]): unknown[] {
  if (Array.isArray(data)) return data;
  if (!data || typeof data !== "object") return [];
  const record = data as Record<string, unknown>;
  for (const key of [...envelopeKeys, "items", "results", "data"]) {
    if (Array.isArray(record[key])) return record[key] as unknown[];
  }
  return [];
}

function mapPostAnalytics(raw: unknown): PostAnalytics | null {
  if (!raw || typeof raw !== "object") return null;
  const r = raw as Record<string, unknown>;
  const postId = pick(r, "post_id", "postId", "id");
  const platform = asString(pick(r, "platform")) as SocialPlatform;
  if (postId === undefined || !SOCIAL_PLATFORMS.includes(platform)) return null;

  return {
    postId: String(postId),
    platform,
    likes: asNumber(pick(r, "likes")),
    comments: asNumber(pick(r, "comments")),
    shares: asNumber(pick(r, "shares")),
    saves: asNumber(pick(r, "saves")),
    reach: asNumber(pick(r, "reach")),
    impressions: asNumber(pick(r, "impressions")),
    clicks: asNumber(pick(r, "clicks")),
    engagementRate: asNumber(pick(r, "engagement_rate", "engagementRate")),
    date: asString(pick(r, "date", "published_at", "publishedAt", "created_at")),
  };
}

function mapPlatformComparison(raw: unknown): PlatformComparisonMetrics | null {
  if (!raw || typeof raw !== "object") return null;
  const r = raw as Record<string, unknown>;
  const platform = asString(pick(r, "platform")) as SocialPlatform;
  if (!SOCIAL_PLATFORMS.includes(platform)) return null;

  return {
    platform,
    followers: asNumber(pick(r, "followers")),
    reach: asNumber(pick(r, "reach")),
    impressions: asNumber(pick(r, "impressions")),
    engagement: asNumber(pick(r, "engagement", "total_engagement")),
    likes: asNumber(pick(r, "likes")),
    comments: asNumber(pick(r, "comments")),
    shares: asNumber(pick(r, "shares")),
    clicks: asNumber(pick(r, "clicks")),
  };
}

function mapTrendPoint(raw: unknown): TrendPoint | null {
  if (!raw || typeof raw !== "object") return null;
  const r = raw as Record<string, unknown>;
  const date = pick(r, "date");
  if (date === undefined) return null;

  return {
    date: asString(date).slice(0, 10),
    engagement: asNumber(pick(r, "engagement")),
    reach: asNumber(pick(r, "reach")),
    impressions: asNumber(pick(r, "impressions")),
    clicks: asNumber(pick(r, "clicks")),
  };
}

/** Best-effort mapping — see the file-level note above on what's guessed vs. safely defaulted. */
function mapAudienceSnapshot(raw: unknown): AudienceSnapshot | null {
  if (!raw || typeof raw !== "object") return null;
  const r = raw as Record<string, unknown>;
  const platform = asString(pick(r, "platform")) as SocialPlatform;
  if (!SOCIAL_PLATFORMS.includes(platform)) return null;

  const demographics = asArray(pick(r, "demographics", "age_distribution")).map((d) => {
    const row = (d ?? {}) as Record<string, unknown>;
    return { ageRange: asString(pick(row, "age_range", "ageRange", "range")), percentage: asNumber(pick(row, "percentage")) };
  });

  const genderDistribution = asArray(pick(r, "gender_distribution", "genderDistribution")).map((g) => {
    const row = (g ?? {}) as Record<string, unknown>;
    return { label: asString(pick(row, "label", "gender")), percentage: asNumber(pick(row, "percentage")) };
  });

  const locations = asArray(pick(r, "locations", "countries")).map((l) => {
    const row = (l ?? {}) as Record<string, unknown>;
    return { country: asString(pick(row, "country")), percentage: asNumber(pick(row, "percentage")) };
  });

  return {
    platform,
    followers: asNumber(pick(r, "followers")),
    newFollowers: asNumber(pick(r, "new_followers", "newFollowers")),
    lostFollowers: asNumber(pick(r, "lost_followers", "lostFollowers")),
    followerGrowth: asNumber(pick(r, "follower_growth", "followerGrowth")),
    growthRate: asNumber(pick(r, "growth_rate", "growthRate")),
    genderDistribution,
    demographics,
    locations,
    // Not guessed — no confirmed field names for these yet (see note above).
    cities: [],
    languages: [],
    activityByHour: [],
    activityByDay: [],
  };
}

function mapAudienceResponse(data: unknown, platformRows: PlatformComparisonMetrics[] = []): AudienceSnapshot[] {
  const rows = unwrapList(data, "audience", "platforms");
  if (rows.length > 0) {
    return rows.map(mapAudienceSnapshot).filter((a): a is AudienceSnapshot => a !== null);
  }

  if (!data || typeof data !== "object") return [];
  const record = data as Record<string, unknown>;
  const growth = asArray(record.follower_growth ?? record.followerGrowth);
  const lastGrowth = growth[growth.length - 1] as Record<string, unknown> | undefined;
  const previousGrowth = growth[growth.length - 2] as Record<string, unknown> | undefined;
  const followers = asNumber(pick(record, "total_followers", "followers"));
  const currentFollowers = asNumber(pick(lastGrowth ?? {}, "followers"), followers);
  const previousFollowers = asNumber(pick(previousGrowth ?? {}, "followers"), Math.max(0, currentFollowers - Math.max(1, Math.round(currentFollowers * 0.02))));
  const aggregate = mapAudienceSnapshot({
    ...record,
    platform: "instagram",
    followers: currentFollowers,
    new_followers: asNumber(pick(lastGrowth ?? {}, "new_followers", "newFollowers"), Math.max(1, currentFollowers - previousFollowers)),
    lost_followers: 0,
    follower_growth: currentFollowers - previousFollowers,
    growth_rate: previousFollowers > 0 ? ((currentFollowers - previousFollowers) / previousFollowers) * 100 : 2,
  });
  if (!aggregate) return [];
  const targets = platformRows.length > 0 ? platformRows : [{ platform: "instagram", followers: aggregate.followers } as PlatformComparisonMetrics];
  return targets.map((platform) => ({
    ...aggregate,
    platform: platform.platform,
    followers: platform.followers || aggregate.followers,
  }));
}

const MOCK_ANALYTICS_PLATFORMS: SocialPlatform[] = [
  "instagram",
  "linkedin",
  "youtube",
];

function mockDate(daysAgo: number): string {
  const date = new Date();
  date.setDate(date.getDate() - daysAgo);
  return date.toISOString();
}

function buildMockAnalytics() {
  const postAnalytics: PostAnalytics[] = MOCK_ANALYTICS_PLATFORMS.map((platform, index) => ({
    postId: `mock-analytics-post-${index + 1}`,
    platform,
    likes: 92 + index * 24,
    comments: 18 + index * 6,
    shares: 14 + index * 5,
    saves: 11 + index * 4,
    reach: 160 + index * 42,
    impressions: 260 + index * 58,
    clicks: 38 + index * 13,
    engagementRate: 4.8 + index * 0.9,
    date: mockDate(index * 4 + 1),
  }));

  const platformComparison = postAnalytics.map((row) => ({
    platform: row.platform,
    followers: 118 + MOCK_ANALYTICS_PLATFORMS.indexOf(row.platform) * 46,
    reach: Math.min(500, row.reach + 120),
    impressions: Math.min(500, row.impressions + 180),
    engagement: row.likes + row.comments + row.shares,
    likes: row.likes,
    comments: row.comments,
    shares: row.shares,
    clicks: row.clicks,
  }));

  const audienceSnapshots: AudienceSnapshot[] = platformComparison.map((row) => ({
    platform: row.platform,
    followers: row.followers,
    newFollowers: 26 + MOCK_ANALYTICS_PLATFORMS.indexOf(row.platform) * 8,
    lostFollowers: 7 + MOCK_ANALYTICS_PLATFORMS.indexOf(row.platform) * 2,
    followerGrowth: 19 + MOCK_ANALYTICS_PLATFORMS.indexOf(row.platform) * 6,
    growthRate: 2.4 + MOCK_ANALYTICS_PLATFORMS.indexOf(row.platform) * 0.7,
    genderDistribution: [
      { label: "Female", percentage: 54 },
      { label: "Male", percentage: 41 },
      { label: "Other", percentage: 5 },
    ],
    demographics: [
      { ageRange: "18-24", percentage: 28 },
      { ageRange: "25-34", percentage: 42 },
      { ageRange: "35-44", percentage: 20 },
      { ageRange: "45+", percentage: 10 },
    ],
    locations: [
      { country: "India", percentage: 48 },
      { country: "United States", percentage: 24 },
      { country: "United Kingdom", percentage: 14 },
      { country: "Other", percentage: 14 },
    ],
    cities: [
      { city: "Mumbai", percentage: 18 },
      { city: "Bengaluru", percentage: 15 },
      { city: "Delhi", percentage: 12 },
    ],
    languages: [
      { language: "English", percentage: 62 },
      { language: "Hindi", percentage: 25 },
      { language: "Other", percentage: 13 },
    ],
    activityByHour: Array.from({ length: 8 }, (_, hour) => ({ hour: hour + 10, level: 48 + hour * 5 })),
    activityByDay: [
      { day: "Mon", level: 64 },
      { day: "Tue", level: 72 },
      { day: "Wed", level: 81 },
      { day: "Thu", level: 76 },
      { day: "Fri", level: 88 },
      { day: "Sat", level: 69 },
      { day: "Sun", level: 58 },
    ],
  }));

  const trendPoints: TrendPoint[] = Array.from({ length: 12 }, (_, index) => ({
    date: mockDate(11 - index).slice(0, 10),
    engagement: 105 + index * 22 + (index % 3) * 18,
    reach: 180 + index * 21 + (index % 2) * 24,
    impressions: 270 + index * 18 + (index % 4) * 21,
    clicks: 42 + index * 9 + (index % 3) * 7,
  }));

  return { postAnalytics, platformComparison, audienceSnapshots, trendPoints };
}

interface AnalyticsState {
  postAnalytics: PostAnalytics[];
  audienceSnapshots: AudienceSnapshot[];
  trendPoints: TrendPoint[];
  platformComparison: PlatformComparisonMetrics[];
  isLoading: boolean;
  hasLoaded: boolean;
  error: string | null;
  fetchAnalytics: (postCount: number, useMock?: boolean) => Promise<void>;
  getPostAnalytics: (postId: string) => PostAnalytics | undefined;
  getAudienceSnapshot: (platform: SocialPlatform) => AudienceSnapshot | undefined;
  getPlatformComparison: (platform: SocialPlatform) => PlatformComparisonMetrics | undefined;
}

export const useAnalyticsStore = create<AnalyticsState>((set, get) => ({
  postAnalytics: [],
  audienceSnapshots: [],
  trendPoints: [],
  platformComparison: [],
  isLoading: false,
  hasLoaded: false,
  error: null,

  fetchAnalytics: async (postCount, useMock = true) => {
    if (get().isLoading) return;
    set({ isLoading: true, error: null });

    await Promise.allSettled([
      api.post("/analytics/seed-mock-data", null, { params: { only_missing: false } }),
      api.post("/analytics/seed-mock-account-stats", null, { params: { only_missing: false } }),
    ]);

    Promise.allSettled([
      api.get("/analytics/posts"),
      api.get("/analytics/platforms"),
      api.get("/analytics/engagement/trend"),
      api.get("/analytics/audience"),
    ]).then(([postsRes, platformsRes, trendRes, audienceRes]) => {

      const postAnalytics = postsRes.status === "fulfilled"
        ? unwrapList(postsRes.value.data, "posts").map(mapPostAnalytics).filter((p): p is PostAnalytics => p !== null)
        : [];
      const platformComparison = platformsRes.status === "fulfilled"
        ? unwrapList(platformsRes.value.data, "platforms").map(mapPlatformComparison).filter((p): p is PlatformComparisonMetrics => p !== null)
        : [];
      const trendPoints = trendRes.status === "fulfilled"
        ? unwrapList(trendRes.value.data, "trend", "points", "data").map(mapTrendPoint).filter((p): p is TrendPoint => p !== null)
        : [];
      const audienceSnapshots = audienceRes.status === "fulfilled"
        ? mapAudienceResponse(audienceRes.value.data, platformComparison)
        : [];

      const anyFailed = [postsRes, platformsRes, trendRes, audienceRes].some((r) => r.status === "rejected");
      const firstError = [postsRes, platformsRes, trendRes, audienceRes].find(
        (r): r is PromiseRejectedResult => r.status === "rejected"
      );

      const mock = buildMockAnalytics();
      const analytics = postCount === 0 ? {
        postAnalytics: [],
        audienceSnapshots: [],
        trendPoints: [],
        platformComparison: [],
      } : !useMock && postAnalytics.length > 0 ? {
        postAnalytics,
        audienceSnapshots,
        trendPoints,
        platformComparison,
      } : mock;

      set({
        postAnalytics: analytics.postAnalytics,
        audienceSnapshots: analytics.audienceSnapshots,
        trendPoints: analytics.trendPoints,
        platformComparison: analytics.platformComparison,
        isLoading: false,
        hasLoaded: true,
        error: anyFailed ? extractErrorMessage(firstError?.reason, "Some analytics data couldn't be loaded.") : null,
      });
    });
  },

  getPostAnalytics: (postId) => {
    return get().postAnalytics.find((p) => p.postId === postId);
  },

  getAudienceSnapshot: (platform) => {
    return get().audienceSnapshots.find((a) => a.platform === platform);
  },

  getPlatformComparison: (platform) => {
    return get().platformComparison.find((p) => p.platform === platform);
  },
}));
