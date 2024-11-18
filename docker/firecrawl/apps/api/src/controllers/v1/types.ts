import { Request, Response } from "express";
import { z } from "zod";
import { isUrlBlocked } from "../../scraper/WebScraper/utils/blocklist";
import { Action, ExtractorOptions, PageOptions } from "../../lib/entities";
import { protocolIncluded, checkUrl } from "../../lib/validateUrl";
import { PlanType } from "../../types";
import { countries } from "../../lib/validate-country";

export type Format =
  | "markdown"
  | "html"
  | "rawHtml"
  | "links"
  | "screenshot"
  | "screenshot@fullPage"
  | "extract";

export const url = z.preprocess(
  (x) => {
    if (!protocolIncluded(x as string)) {
      return `http://${x}`;
    }
    return x;
  },
  z
    .string()
    .url()
    .regex(/^https?:\/\//, "URL uses unsupported protocol")
    .refine(
      (x) => /\.[a-z]{2,}([\/?#]|$)/i.test(x),
      "URL must have a valid top-level domain or be a valid path"
    )
    .refine(
      (x) => {
        try {
          checkUrl(x as string)
          return true;
        } catch (_) {
          return false;
        }
      },
      "Invalid URL"
    )
    .refine(
      (x) => !isUrlBlocked(x as string),
      "Firecrawl currently does not support social media scraping due to policy restrictions. We're actively working on building support for it."
    )
);

const strictMessage = "Unrecognized key in body -- please review the v1 API documentation for request body changes";

export const extractOptions = z.object({
  mode: z.enum(["llm"]).default("llm"),
  schema: z.any().optional(),
  systemPrompt: z.string().default("Based on the information on the page, extract all the information from the schema. Try to extract all the fields even those that might not be marked as required."),
  prompt: z.string().optional()
}).strict(strictMessage);

export type ExtractOptions = z.infer<typeof extractOptions>;

export const actionsSchema = z.array(z.union([
  z.object({
    type: z.literal("wait"),
    milliseconds: z.number().int().positive().finite().optional(),
    selector: z.string().optional(),
  }).refine(
    (data) => (data.milliseconds !== undefined || data.selector !== undefined) && !(data.milliseconds !== undefined && data.selector !== undefined),
    {
      message: "Either 'milliseconds' or 'selector' must be provided, but not both.",
    }
  ),
  z.object({
    type: z.literal("click"),
    selector: z.string(),
  }),
  z.object({
    type: z.literal("screenshot"),
    fullPage: z.boolean().default(false),
  }),
  z.object({
    type: z.literal("write"),
    text: z.string(),
  }),
  z.object({
    type: z.literal("press"),
    key: z.string(),
  }),
  z.object({
    type: z.literal("scroll"),
    direction: z.enum(["up", "down"]),
  }),
  z.object({
    type: z.literal("scrape"),
  }),
]));

export const scrapeOptions = z.object({
  formats: z
    .enum([
      "markdown",
      "html",
      "rawHtml",
      "links",
      "screenshot",
      "screenshot@fullPage",
      "extract"
    ])
    .array()
    .optional()
    .default(["markdown"])
    .refine(x => !(x.includes("screenshot") && x.includes("screenshot@fullPage")), "You may only specify either screenshot or screenshot@fullPage"),
  headers: z.record(z.string(), z.string()).optional(),
  includeTags: z.string().array().optional(),
  excludeTags: z.string().array().optional(),
  onlyMainContent: z.boolean().default(true),
  timeout: z.number().int().positive().finite().safe().default(30000),
  waitFor: z.number().int().nonnegative().finite().safe().default(0),
  extract: extractOptions.optional(),
  mobile: z.boolean().default(false),
  parsePDF: z.boolean().default(true),
  actions: actionsSchema.optional(),
  // New
  location: z.object({
    country: z.string().optional().refine(
      (val) => !val || Object.keys(countries).includes(val.toUpperCase()),
      {
        message: "Invalid country code. Please use a valid ISO 3166-1 alpha-2 country code.",
      }
    ).transform(val => val ? val.toUpperCase() : 'US'),
    languages: z.string().array().optional(),
  }).optional(),
  
  // Deprecated
  geolocation: z.object({
    country: z.string().optional().refine(
      (val) => !val || Object.keys(countries).includes(val.toUpperCase()),
      {
        message: "Invalid country code. Please use a valid ISO 3166-1 alpha-2 country code.",
      }
    ).transform(val => val ? val.toUpperCase() : 'US'),
    languages: z.string().array().optional(),
  }).optional(),
  skipTlsVerification: z.boolean().default(false),
}).strict(strictMessage)


export type ScrapeOptions = z.infer<typeof scrapeOptions>;

export const scrapeRequestSchema = scrapeOptions.extend({
  url,
  origin: z.string().optional().default("api"),
}).strict(strictMessage).refine(
  (obj) => {
    const hasExtractFormat = obj.formats?.includes("extract");
    const hasExtractOptions = obj.extract !== undefined;
    return (hasExtractFormat && hasExtractOptions) || (!hasExtractFormat && !hasExtractOptions);
  },
  {
    message: "When 'extract' format is specified, 'extract' options must be provided, and vice versa",
  }
).transform((obj) => {
  if ((obj.formats?.includes("extract") || obj.extract) && !obj.timeout) {
    return { ...obj, timeout: 60000 };
  }
  return obj;
});

export type ScrapeRequest = z.infer<typeof scrapeRequestSchema>;

export const batchScrapeRequestSchema = scrapeOptions.extend({
  urls: url.array(),
  origin: z.string().optional().default("api"),
}).strict(strictMessage).refine(
  (obj) => {
    const hasExtractFormat = obj.formats?.includes("extract");
    const hasExtractOptions = obj.extract !== undefined;
    return (hasExtractFormat && hasExtractOptions) || (!hasExtractFormat && !hasExtractOptions);
  },
  {
    message: "When 'extract' format is specified, 'extract' options must be provided, and vice versa",
  }
).transform((obj) => {
  if ((obj.formats?.includes("extract") || obj.extract) && !obj.timeout) {
    return { ...obj, timeout: 60000 };
  }
  return obj;
});

export type BatchScrapeRequest = z.infer<typeof batchScrapeRequestSchema>;

const crawlerOptions = z.object({
  includePaths: z.string().array().default([]),
  excludePaths: z.string().array().default([]),
  maxDepth: z.number().default(10), // default?
  limit: z.number().default(10000), // default?
  allowBackwardLinks: z.boolean().default(false), // >> TODO: CHANGE THIS NAME???
  allowExternalLinks: z.boolean().default(false),
  ignoreSitemap: z.boolean().default(true),
}).strict(strictMessage);

// export type CrawlerOptions = {
//   includePaths?: string[];
//   excludePaths?: string[];
//   maxDepth?: number;
//   limit?: number;
//   allowBackwardLinks?: boolean; // >> TODO: CHANGE THIS NAME???
//   allowExternalLinks?: boolean;
//   ignoreSitemap?: boolean;
// };

export type CrawlerOptions = z.infer<typeof crawlerOptions>;

export const crawlRequestSchema = crawlerOptions.extend({
  url,
  origin: z.string().optional().default("api"),
  scrapeOptions: scrapeOptions.omit({ timeout: true }).default({}),
  webhook: z.string().url().optional(),
  limit: z.number().default(10000),
}).strict(strictMessage);

// export type CrawlRequest = {
//   url: string;
//   crawlerOptions?: CrawlerOptions;
//   scrapeOptions?: Exclude<ScrapeRequest, "url">;
// };

// export type ExtractorOptions = {
//   mode: "markdown" | "llm-extraction" | "llm-extraction-from-markdown" | "llm-extraction-from-raw-html";
//   extractionPrompt?: string;
//   extractionSchema?: Record<string, any>;
// }


export type CrawlRequest = z.infer<typeof crawlRequestSchema>;

export const mapRequestSchema = crawlerOptions.extend({
  url,
  origin: z.string().optional().default("api"),
  includeSubdomains: z.boolean().default(true),
  search: z.string().optional(),
  ignoreSitemap: z.boolean().default(false),
  limit: z.number().min(1).max(5000).default(5000).optional(),
}).strict(strictMessage);

// export type MapRequest = {
//   url: string;
//   crawlerOptions?: CrawlerOptions;
// };

export type MapRequest = z.infer<typeof mapRequestSchema>;

export type Document = {
  markdown?: string;
  extract?: string;
  html?: string;
  rawHtml?: string;
  links?: string[];
  screenshot?: string;
  actions?: {
    screenshots: string[];
  };
  warning?: string;
  metadata: {
    title?: string;
    description?: string;
    language?: string;
    keywords?: string;
    robots?: string;
    ogTitle?: string;
    ogDescription?: string;
    ogUrl?: string;
    ogImage?: string;
    ogAudio?: string;
    ogDeterminer?: string;
    ogLocale?: string;
    ogLocaleAlternate?: string[];
    ogSiteName?: string;
    ogVideo?: string;
    dcTermsCreated?: string;
    dcDateCreated?: string;
    dcDate?: string;
    dcTermsType?: string;
    dcType?: string;
    dcTermsAudience?: string;
    dcTermsSubject?: string;
    dcSubject?: string;
    dcDescription?: string;
    dcTermsKeywords?: string;
    modifiedTime?: string;
    publishedTime?: string;
    articleTag?: string;
    articleSection?: string;
    sourceURL?: string;
    statusCode?: number;
    error?: string;
    [key: string]: string | string[] | number | undefined;

  };
};

export type ErrorResponse = {
  success: false;
  error: string;
  details?: any;
};

export type ScrapeResponse =
  | ErrorResponse
  | {
      success: true;
      warning?: string;
      data: Document;
      scrape_id?: string;
    };

export interface ScrapeResponseRequestTest {
  statusCode: number;
  body: ScrapeResponse;
  error?: string;
}

export type CrawlResponse =
  | ErrorResponse
  | {
      success: true;
      id: string;
      url: string;
    };

export type MapResponse =
  | ErrorResponse
  | {
      success: true;
      links: string[];
      scrape_id?: string;
    };

export type CrawlStatusParams = {
  jobId: string;
};

export type ConcurrencyCheckParams = {
  teamId: string;
};

export type ConcurrencyCheckResponse =
  | ErrorResponse
  | {
      success: true;
      concurrency: number;
    };

export type CrawlStatusResponse =
  | ErrorResponse
  | {
      success: true;
      status: "scraping" | "completed" | "failed" | "cancelled";
      completed: number;
      total: number;
      creditsUsed: number;
      expiresAt: string;
      next?: string;
      data: Document[];
    };

type AuthObject = {
  team_id: string;
  plan: PlanType;
};

type Account = {
  remainingCredits: number;
};

export type AuthCreditUsageChunk = {
  api_key: string;
  team_id: string;
  sub_id: string | null;
  sub_current_period_start: string | null;
  sub_current_period_end: string | null;
  price_id: string | null;
  price_credits: number; // credit limit with assoicated price, or free_credits (500) if free plan
  credits_used: number;
  coupon_credits: number; // do not rely on this number to be up to date after calling a billTeam
  coupons: any[];
  adjusted_credits_used: number; // credits this period minus coupons used
  remaining_credits: number;
  sub_user_id: string | null;
  total_credits_sum: number;
};

export interface RequestWithMaybeACUC<
  ReqParams = {},
  ReqBody = undefined,
  ResBody = undefined
> extends Request<ReqParams, ReqBody, ResBody> {
  acuc?: AuthCreditUsageChunk,
}

export interface RequestWithACUC<
  ReqParams = {},
  ReqBody = undefined,
  ResBody = undefined
> extends Request<ReqParams, ReqBody, ResBody> {
  acuc: AuthCreditUsageChunk,
}

export interface RequestWithAuth<
  ReqParams = {},
  ReqBody = undefined,
  ResBody = undefined,
> extends Request<ReqParams, ReqBody, ResBody> {
  auth: AuthObject;
  account?: Account;
}

export interface RequestWithMaybeAuth<
  ReqParams = {},
  ReqBody = undefined,
  ResBody = undefined
> extends RequestWithMaybeACUC<ReqParams, ReqBody, ResBody> {
  auth?: AuthObject;
  account?: Account;
}

export interface RequestWithAuth<
  ReqParams = {},
  ReqBody = undefined,
  ResBody = undefined,
> extends RequestWithACUC<ReqParams, ReqBody, ResBody> {
  auth: AuthObject;
  account?: Account;
}

export interface ResponseWithSentry<
  ResBody = undefined,
> extends Response<ResBody> {
  sentry?: string,
}

export function legacyCrawlerOptions(x: CrawlerOptions) {
  return {
    includes: x.includePaths,
    excludes: x.excludePaths,
    maxCrawledLinks: x.limit,
    maxDepth: x.maxDepth,
    limit: x.limit,
    generateImgAltText: false,
    allowBackwardCrawling: x.allowBackwardLinks,
    allowExternalContentLinks: x.allowExternalLinks,
    ignoreSitemap: x.ignoreSitemap,
  };
}

export function legacyScrapeOptions(x: ScrapeOptions): PageOptions {
  return {
    includeMarkdown: x.formats.includes("markdown"),
    includeHtml: x.formats.includes("html"),
    includeRawHtml: x.formats.includes("rawHtml"),
    includeExtract: x.formats.includes("extract"),
    onlyIncludeTags: x.includeTags,
    removeTags: x.excludeTags,
    onlyMainContent: x.onlyMainContent,
    waitFor: x.waitFor,
    headers: x.headers,
    includeLinks: x.formats.includes("links"),
    screenshot: x.formats.includes("screenshot"),
    fullPageScreenshot: x.formats.includes("screenshot@fullPage"),
    parsePDF: x.parsePDF,
    actions: x.actions as Action[], // no strict null checking grrrr - mogery
    geolocation: x.location ?? x.geolocation,
    skipTlsVerification: x.skipTlsVerification,
    mobile: x.mobile,
  };
}

export function legacyExtractorOptions(x: ExtractOptions): ExtractorOptions {
  return {
    mode: x.mode ? "llm-extraction" : "markdown",
    extractionPrompt: x.prompt ?? "Based on the information on the page, extract the information from the schema.",
    extractionSchema: x.schema,
    userPrompt: x.prompt ?? "",
  };
}

export function legacyDocumentConverter(doc: any): Document {
  if (doc === null || doc === undefined) return null;

  if (doc.metadata) {
    if (doc.metadata.screenshot) {
      doc.screenshot = doc.metadata.screenshot;
      delete doc.metadata.screenshot;
    }

    if (doc.metadata.fullPageScreenshot) {
      doc.fullPageScreenshot = doc.metadata.fullPageScreenshot;
      delete doc.metadata.fullPageScreenshot;
    }
  }

  return {
    markdown: doc.markdown,
    links: doc.linksOnPage,
    rawHtml: doc.rawHtml,
    html: doc.html,
    extract: doc.llm_extraction,
    screenshot: doc.screenshot ?? doc.fullPageScreenshot,
    actions: doc.actions ?? undefined,
    warning: doc.warning ?? undefined,
    metadata: {
      ...doc.metadata,
      pageError: undefined,
      pageStatusCode: undefined,
      error: doc.metadata?.pageError,
      statusCode: doc.metadata?.pageStatusCode,
    },
  };
}
