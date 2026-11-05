import type { PlanTier, SubscriptionStatus } from "@prisma/client";
import { PLANS, type PlanKey } from "./index";

const ACTIVE: SubscriptionStatus[] = ["ACTIVE", "TRIALING"];

export function isSubscriptionActive(status: SubscriptionStatus | null | undefined): boolean {
  return !!status && ACTIVE.includes(status);
}

export function getPlanLimits(plan: PlanTier | PlanKey | null | undefined) {
  const key = (plan || "FREE") as PlanKey;
  return PLANS[key]?.limits ?? PLANS.FREE.limits;
}

export function canAccessCourse(plan: PlanTier | null | undefined, enrolledCount: number): boolean {
  const limits = getPlanLimits(plan);
  if (limits.courses < 0) return true;
  return enrolledCount < limits.courses;
}

export function requireRole(userRole: string, allowed: string[]): boolean {
  return allowed.includes(userRole);
}

export const ADMIN_ROLES = ["PLATFORM_ADMIN", "INSTITUTIONAL_ADMIN", "TEAM_ADMIN"];
export const INVESTOR_ROLES = ["INVESTOR", "STRATEGIC_PARTNER", "PLATFORM_ADMIN"];
export const SPONSOR_ROLES = ["SPONSOR", "PLATFORM_ADMIN"];
