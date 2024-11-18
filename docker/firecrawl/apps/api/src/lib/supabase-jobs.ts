import { supabase_service } from "../services/supabase";
import { Logger } from "./logger";
import * as Sentry from "@sentry/node";

/**
 * Get a single firecrawl_job by ID
 * @param jobId ID of Job
 * @returns {any | null} Job
 */
export const supabaseGetJobById = async (jobId: string) => {
  const { data, error } = await supabase_service
    .from("firecrawl_jobs")
    .select("*")
    .eq("job_id", jobId)
    .single();

  if (error) {
    return null;
  }

  if (!data) {
    return null;
  }

  return data;
};

/**
 * Get multiple firecrawl_jobs by ID. Use this if you're not requesting a lot (50+) of jobs at once.
 * @param jobIds IDs of Jobs
 * @returns {any[]} Jobs
 */
export const supabaseGetJobsById = async (jobIds: string[]) => {
  const { data, error } = await supabase_service
    .from("firecrawl_jobs")
    .select()
    .in("job_id", jobIds);

  if (error) {
    Logger.error(`Error in supabaseGetJobsById: ${error}`);
    Sentry.captureException(error);
    return [];
  }

  if (!data) {
    return [];
  }

  return data;
};

/**
 * Get multiple firecrawl_jobs by crawl ID. Use this if you need a lot of jobs at once.
 * @param crawlId ID of crawl
 * @returns {any[]} Jobs
 */
export const supabaseGetJobsByCrawlId = async (crawlId: string) => {
  const { data, error } = await supabase_service
    .from("firecrawl_jobs")
    .select()
    .eq("crawl_id", crawlId)

  if (error) {
    Logger.error(`Error in supabaseGetJobsByCrawlId: ${error}`);
    Sentry.captureException(error);
    return [];
  }

  if (!data) {
    return [];
  }

  return data;
};


export const supabaseGetJobByIdOnlyData = async (jobId: string) => {
  const { data, error } = await supabase_service
    .from("firecrawl_jobs")
    .select("docs, team_id")
    .eq("job_id", jobId)
    .single();

  if (error) {
    return null;
  }

  if (!data) {
    return null;
  }

  return data;
};