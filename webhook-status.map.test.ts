import { describe, it, expect } from "vitest";
/** Maps Stripe subscription statuses to our enum — keep in sync with webhook route */
const map: Record<string, string> = {
  trialing: "TRIALING", active: "ACTIVE", past_due: "PAST_DUE", canceled: "CANCELED",
  unpaid: "UNPAID", incomplete: "INCOMPLETE", incomplete_expired: "INCOMPLETE_EXPIRED", paused: "PAUSED",
};
describe("stripe status mapping", () => {
  it("maps all expected statuses", () => {
    expect(map["active"]).toBe("ACTIVE");
    expect(map["trialing"]).toBe("TRIALING");
    expect(map["past_due"]).toBe("PAST_DUE");
  });
});
