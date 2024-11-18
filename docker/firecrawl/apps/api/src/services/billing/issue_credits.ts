import { Logger } from "../../lib/logger";
import { supabase_service } from "../supabase";

export async function issueCredits(team_id: string, credits: number) {
  // Add an entry to supabase coupons
  const { data, error } = await supabase_service.from("coupons").insert({
    team_id: team_id,
    credits: credits,
    status: "active",
    // indicates that this coupon was issued from auto recharge
    from_auto_recharge: true,
  });

  if (error) {
    Logger.error(`Error adding coupon: ${error}`);
    return false;
  }

  return true;
}
