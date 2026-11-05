import Stripe from "stripe";
export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || "sk_test_placeholder", { apiVersion: "2024-12-18.acacia", typescript: true });

export const PLANS = {
  FREE: { name: "Free", monthly: 0, yearly: 0, features: ["2 courses", "Community access"], limits: { courses: 2, seats: 1 } },
  STUDENT: { name: "Student / Learner", monthly: 9, yearly: 79, priceIdMonthly: process.env.STRIPE_PRICE_STUDENT_MONTHLY, priceIdYearly: process.env.STRIPE_PRICE_STUDENT_YEARLY, features: ["20 courses", "Certificates", "Progress tracking"], limits: { courses: 20, seats: 1 }, trialDays: 14 },
  PRO: { name: "Pro", monthly: 29, yearly: 249, priceIdMonthly: process.env.STRIPE_PRICE_PRO_MONTHLY, priceIdYearly: process.env.STRIPE_PRICE_PRO_YEARLY, features: ["Unlimited courses", "Priority support", "API access"], limits: { courses: 100, seats: 1 }, trialDays: 14 },
  TEAM: { name: "Team", monthly: 99, yearly: 899, priceIdMonthly: process.env.STRIPE_PRICE_TEAM_MONTHLY, priceIdYearly: process.env.STRIPE_PRICE_TEAM_YEARLY, features: ["10 seats", "Admin dashboard", "SSO-ready"], limits: { courses: 500, seats: 10 }, trialDays: 14 },
  ENTERPRISE: { name: "Enterprise / Institutional", monthly: null, yearly: null, features: ["Custom seats", "SLA", "Dedicated success"], limits: { courses: -1, seats: -1 } },
} as const;

export type PlanKey = keyof typeof PLANS;
