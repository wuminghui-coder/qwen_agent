use std::fmt::Display;

use serde::{Deserialize, Serialize};
use serde_json::Value;
use thiserror::Error;

use crate::crawl::CrawlStatus;

#[derive(Debug, Deserialize, Serialize, Clone)]
pub struct FirecrawlAPIError {
    /// Always false.
    success: bool,

    /// Error message
    pub error: String,

    /// Additional details of this error. Schema depends on the error itself.
    pub details: Option<Value>,
}

impl Display for FirecrawlAPIError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        if let Some(details) = self.details.as_ref() {
            write!(f, "{} ({})", self.error, details)
        } else {
            write!(f, "{}", self.error)
        }
    }
}

#[derive(Error, Debug)]
pub enum FirecrawlError {
    #[error("{0} failed: HTTP error {1}: {2}")]
    HttpRequestFailed(String, u16, String),
    #[error("{0} failed: HTTP error: {1}")]
    HttpError(String, reqwest::Error),
    #[error("Failed to parse response as text: {0}")]
    ResponseParseErrorText(reqwest::Error),
    #[error("Failed to parse response: {0}")]
    ResponseParseError(serde_json::Error),
    #[error("{0} failed: {1}")]
    APIError(String, FirecrawlAPIError),
    #[error("Crawl job failed: {0}")]
    CrawlJobFailed(String, CrawlStatus),
}
