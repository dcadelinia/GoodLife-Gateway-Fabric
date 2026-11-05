/** Transactional email templates — wire with Resend when RESEND_API_KEY is set */
export const templates = {
  welcome: (name: string) => ({
    subject: "Welcome to GoodLife Gateway Fabric",
    html: `<p>Hello ${name},</p><p>Welcome to GoodLife Gateway Fabric by Odynex Axis Logistics LLC.</p>`,
  }),
  trialEnding: (name: string, endsAt: string) => ({
    subject: "Your trial ends soon",
    html: `<p>Hello ${name},</p><p>Your trial ends on ${endsAt}. Upgrade to keep full access.</p>`,
  }),
  paymentFailed: (name: string) => ({
    subject: "Payment issue on your account",
    html: `<p>Hello ${name},</p><p>We could not process your latest payment. Update billing in the Customer Portal.</p>`,
  }),
  paymentSuccess: (name: string) => ({
    subject: "Payment received",
    html: `<p>Hello ${name},</p><p>Thank you — your payment was successful.</p>`,
  }),
};
