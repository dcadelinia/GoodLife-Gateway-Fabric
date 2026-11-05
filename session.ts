import { getServerSession } from "next-auth";
import { authOptions } from "./options";
import { redirect } from "next/navigation";
import { ADMIN_ROLES, INVESTOR_ROLES, SPONSOR_ROLES } from "@/lib/stripe/entitlements";

export async function getSession() {
  return getServerSession(authOptions);
}

export async function requireAuth() {
  const session = await getSession();
  if (!session?.user) redirect("/signin");
  return session;
}

export async function requireRole(allowed: string[]) {
  const session = await requireAuth();
  const role = (session.user as { role?: string }).role || "GUEST";
  if (!allowed.includes(role)) redirect("/dashboard/overview");
  return session;
}

export async function requireAdmin() {
  return requireRole(ADMIN_ROLES);
}

export async function requireInvestor() {
  return requireRole(INVESTOR_ROLES);
}

export async function requireSponsor() {
  return requireRole(SPONSOR_ROLES);
}
