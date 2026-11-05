import { NextResponse } from "next/server";
export async function GET() {
  return NextResponse.json({
    status: "healthy",
    service: "GoodLife Gateway Fabric",
    company: "Odynex Axis Logistics LLC",
    timestamp: new Date().toISOString(),
  });
}
