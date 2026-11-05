import Stripe from "stripe";

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY || "sk_test_placeholder", {
  apiVersion: "2024-12-18.acacia",
  typescript: true,
});

export const PLANS = {
  FREE: { name: "Free", priceId: null, limits: { courses: 2, seats: 1 } },
  STUDENT: {
    name: "Student / Learner",
    monthlyPriceId: process.env.STRIPE_PRICE_STUDENT_MONTHLY,
    yearlyPriceId: process.env.STRIPE_PRICE_STUDENT_YEARLY,
    limits: { courses: 20, seats: 1 },
  },
  PRO: {
    name: "Pro",
    monthlyPriceId: process.env.STRIPE_PRICE_PRO_MONTHLY,
    yearlyPriceId: process.env.STRIPE_PRICE_PRO_YEARLY,
    limits: { courses: 100, seats: 1 },
  },
  TEAM: {
    name: "Team",
    monthlyPriceId: process.env.STRIPE_PRICE_TEAM_MONTHLY,
    yearlyPriceId: process.env.STRIPE_PRICE_TEAM_YEARLY,
    limits: { courses: 500, seats: 10 },
  },
  ENTERPRISE: { name: "Enterprise / Institutional", priceId: null, limits: { courses: -1, seats: -1 } },
} as const;
