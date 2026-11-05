import { describe, it, expect } from "vitest";
import { isSubscriptionActive, canAccessCourse, getPlanLimits, requireRole } from "../../src/lib/stripe/entitlements";

describe("entitlements", () => {
  it("treats ACTIVE and TRIALING as active", () => {
    expect(isSubscriptionActive("ACTIVE")).toBe(true);
    expect(isSubscriptionActive("TRIALING")).toBe(true);
    expect(isSubscriptionActive("CANCELED")).toBe(false);
    expect(isSubscriptionActive(null)).toBe(false);
  });
  it("enforces course limits by plan", () => {
    expect(canAccessCourse("FREE", 1)).toBe(true);
    expect(canAccessCourse("FREE", 2)).toBe(false);
    expect(canAccessCourse("PRO", 50)).toBe(true);
    expect(canAccessCourse("ENTERPRISE", 9999)).toBe(true);
  });
  it("returns plan limits", () => {
    expect(getPlanLimits("FREE").courses).toBe(2);
    expect(getPlanLimits("TEAM").seats).toBe(10);
  });
  it("checks roles", () => {
    expect(requireRole("PLATFORM_ADMIN", ["PLATFORM_ADMIN", "TEAM_ADMIN"])).toBe(true);
    expect(requireRole("FREE", ["PLATFORM_ADMIN"])).toBe(false);
  });
});
