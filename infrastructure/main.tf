# ============================================
# NEXOVA — Terraform Configuration
# ============================================
# Infrastructure as Code for Google Cloud
# ============================================

terraform {
  required_version = ">= 1.9.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 6.0"
    }
  }

  backend "gcs" {
    bucket = "optical-realm-501607-n5-tf-state"
    prefix = "terraform/state"
  }
}

# ---- Variables ----

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be development, staging, or production."
  }
}

variable "gemini_model" {
  description = "Gemini model to use"
  type        = string
  default     = "gemini-2.5-pro"
}

# ---- Providers ----

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

# ---- Enable Required APIs ----

resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
    "firestore.googleapis.com",
    "secretmanager.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "aiplatform.googleapis.com",
    "storage.googleapis.com",
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
  ])

  service            = each.key
  disable_on_destroy = false
}

# ---- Artifact Registry ----

resource "google_artifact_registry_repository" "nexova" {
  location      = var.region
  repository_id = "nexova"
  description   = "NEXOVA Docker images"
  format        = "DOCKER"

  cleanup_policies {
    id     = "keep-last-10"
    action = "KEEP"

    most_recent_versions {
      keep_count = 10
    }
  }

  depends_on = [google_project_service.apis["artifactregistry.googleapis.com"]]
}

# ---- Service Accounts ----

resource "google_service_account" "nexova_api" {
  account_id   = "nexova-api"
  display_name = "NEXOVA API Service Account"
  description  = "Service account for NEXOVA backend API"
}

resource "google_service_account" "nexova_web" {
  account_id   = "nexova-web"
  display_name = "NEXOVA Web Service Account"
  description  = "Service account for NEXOVA frontend"
}

# ---- IAM Bindings (Least Privilege) ----

# API service account permissions
resource "google_project_iam_member" "api_firestore" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.nexova_api.email}"
}

resource "google_project_iam_member" "api_vertex_ai" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.nexova_api.email}"
}

resource "google_project_iam_member" "api_secret_manager" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.nexova_api.email}"
}

resource "google_project_iam_member" "api_logging" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.nexova_api.email}"
}

resource "google_project_iam_member" "api_monitoring" {
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = "serviceAccount:${google_service_account.nexova_api.email}"
}

resource "google_project_iam_member" "api_storage" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.nexova_api.email}"
}

# Web service account permissions (minimal)
resource "google_project_iam_member" "web_logging" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.nexova_web.email}"
}

# ---- Secret Manager ----

resource "google_secret_manager_secret" "secret_key" {
  secret_id = "nexova-secret-key"

  replication {
    auto {}
  }

  depends_on = [google_project_service.apis["secretmanager.googleapis.com"]]
}

resource "google_secret_manager_secret_version" "secret_key_version" {
  secret      = google_secret_manager_secret.secret_key.id
  secret_data = "CHANGE_ME_IN_PRODUCTION_${var.environment}"

  lifecycle {
    ignore_changes = [secret_data]
  }
}

# ---- Firestore Database ----

resource "google_firestore_database" "nexova" {
  provider    = google-beta
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"

  concurrency_mode            = "OPTIMISTIC"
  app_engine_integration_mode = "DISABLED"

  depends_on = [google_project_service.apis["firestore.googleapis.com"]]

  lifecycle {
    prevent_destroy = true
  }
}

# ---- Firestore Indexes ----

resource "google_firestore_index" "incidents_by_status" {
  provider   = google-beta
  database   = google_firestore_database.nexova.name
  collection = "incidents"

  fields {
    field_path = "status"
    order      = "ASCENDING"
  }
  fields {
    field_path = "created_at"
    order      = "DESCENDING"
  }

  depends_on = [google_firestore_database.nexova]
}

resource "google_firestore_index" "incidents_by_severity" {
  provider   = google-beta
  database   = google_firestore_database.nexova.name
  collection = "incidents"

  fields {
    field_path = "severity"
    order      = "ASCENDING"
  }
  fields {
    field_path = "created_at"
    order      = "DESCENDING"
  }

  depends_on = [google_firestore_database.nexova]
}

resource "google_firestore_index" "crowd_by_zone" {
  provider   = google-beta
  database   = google_firestore_database.nexova.name
  collection = "crowd_data"

  fields {
    field_path = "zone_id"
    order      = "ASCENDING"
  }
  fields {
    field_path = "timestamp"
    order      = "DESCENDING"
  }

  depends_on = [google_firestore_database.nexova]
}

resource "google_firestore_index" "notifications_by_role" {
  provider   = google-beta
  database   = google_firestore_database.nexova.name
  collection = "notifications"

  fields {
    field_path = "target_role"
    order      = "ASCENDING"
  }
  fields {
    field_path = "created_at"
    order      = "DESCENDING"
  }

  depends_on = [google_firestore_database.nexova]
}

# ---- Cloud Storage ----

resource "google_storage_bucket" "nexova_assets" {
  name     = "${var.project_id}-nexova-assets"
  location = var.region

  uniform_bucket_level_access = true

  cors {
    origin          = ["*"]
    method          = ["GET"]
    response_header = ["Content-Type"]
    max_age_seconds = 3600
  }

  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type = "Delete"
    }
  }
}

# ---- Cloud Run Services ----

resource "google_cloud_run_v2_service" "api" {
  name     = "nexova-api"
  location = var.region
  deletion_protection = false

  template {
    service_account = google_service_account.nexova_api.email

    scaling {
      min_instance_count = var.environment == "production" ? 1 : 0
      max_instance_count = 10
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/nexova/nexova-api:latest"

      ports {
        container_port = 8080
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "1Gi"
        }
        cpu_idle          = true
        startup_cpu_boost = true
      }

      env {
        name  = "BACKEND_ENV"
        value = var.environment
      }
      env {
        name  = "GCP_PROJECT_ID"
        value = var.project_id
      }
      env {
        name  = "GCP_REGION"
        value = var.region
      }
      env {
        name  = "GEMINI_MODEL"
        value = var.gemini_model
      }
      env {
        name  = "ENABLE_AI"
        value = "true"
      }
      env {
        name  = "ENABLE_SIMULATION"
        value = "true"
      }
      env {
        name = "SECRET_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.secret_key.secret_id
            version = "latest"
          }
        }
      }

      startup_probe {
        http_get {
          path = "/health"
        }
        initial_delay_seconds = 5
        timeout_seconds       = 3
        period_seconds        = 5
        failure_threshold     = 10
      }

      liveness_probe {
        http_get {
          path = "/health"
        }
        period_seconds    = 30
        timeout_seconds   = 5
        failure_threshold = 3
      }
    }

    timeout = "300s"
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [
    google_project_service.apis["run.googleapis.com"],
    google_artifact_registry_repository.nexova,
    google_secret_manager_secret_iam_member.api_secret_access
  ]

  lifecycle {
    ignore_changes = [
      template[0].containers[0].image,
    ]
  }
}

resource "google_cloud_run_v2_service" "web" {
  name     = "nexova-web"
  location = var.region
  deletion_protection = false

  template {
    service_account = google_service_account.nexova_web.email

    scaling {
      min_instance_count = 0
      max_instance_count = 10
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/nexova/nexova-web:latest"

      ports {
        container_port = 3000
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
        cpu_idle          = true
        startup_cpu_boost = true
      }

      env {
        name  = "NEXT_PUBLIC_API_URL"
        value = google_cloud_run_v2_service.api.uri
      }

      startup_probe {
        http_get {
          path = "/"
        }
        initial_delay_seconds = 5
        timeout_seconds       = 3
        period_seconds        = 5
        failure_threshold     = 10
      }
    }

    timeout = "60s"
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [
    google_project_service.apis["run.googleapis.com"],
    google_cloud_run_v2_service.api,
  ]

  lifecycle {
    ignore_changes = [
      template[0].containers[0].image,
    ]
  }
}

# ---- Make Services Public ----

resource "google_cloud_run_v2_service_iam_member" "api_public" {
  name     = google_cloud_run_v2_service.api.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_v2_service_iam_member" "web_public" {
  name     = google_cloud_run_v2_service.web.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# ---- Cloud Monitoring Alerts ----

resource "google_monitoring_alert_policy" "api_error_rate" {
  display_name = "NEXOVA API Error Rate > 5%"
  combiner     = "OR"

  conditions {
    display_name = "Error rate exceeds 5%"

    condition_threshold {
      filter          = "resource.type = \"cloud_run_revision\" AND resource.labels.service_name = \"nexova-api\" AND metric.type = \"run.googleapis.com/request_count\" AND metric.labels.response_code_class = \"5xx\""
      comparison      = "COMPARISON_GT"
      threshold_value = 0.05
      duration        = "300s"

      aggregations {
        alignment_period     = "60s"
        per_series_aligner   = "ALIGN_RATE"
        cross_series_reducer = "REDUCE_SUM"
      }
    }
  }

  notification_channels = []

  depends_on = [google_project_service.apis["monitoring.googleapis.com"]]
}

resource "google_monitoring_alert_policy" "api_latency" {
  display_name = "NEXOVA API P99 Latency > 5s"
  combiner     = "OR"

  conditions {
    display_name = "P99 latency exceeds 5s"

    condition_threshold {
      filter          = "resource.type = \"cloud_run_revision\" AND resource.labels.service_name = \"nexova-api\" AND metric.type = \"run.googleapis.com/request_latencies\""
      comparison      = "COMPARISON_GT"
      threshold_value = 5000
      duration        = "300s"

      aggregations {
        alignment_period     = "60s"
        per_series_aligner   = "ALIGN_PERCENTILE_99"
        cross_series_reducer = "REDUCE_MAX"
      }
    }
  }

  notification_channels = []

  depends_on = [google_project_service.apis["monitoring.googleapis.com"]]
}

# ---- Outputs ----

output "api_url" {
  description = "NEXOVA API URL"
  value       = google_cloud_run_v2_service.api.uri
}

output "web_url" {
  description = "NEXOVA Web URL"
  value       = google_cloud_run_v2_service.web.uri
}

output "artifact_registry" {
  description = "Docker registry URL"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/nexova"
}

output "api_service_account" {
  description = "API service account email"
  value       = google_service_account.nexova_api.email
}

resource "google_secret_manager_secret_iam_member" "api_secret_access" {
  secret_id = google_secret_manager_secret.secret_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.nexova_api.email}"
}
resource "google_monitoring_dashboard" "nexova_dashboard" {
  project        = var.project_id
  dashboard_json = <<EOF
{
  "displayName": "NEXOVA Production Metrics",
  "gridLayout": {
    "columns": "2",
    "widgets": [
      {
        "title": "Cloud Run Request Count",
        "xyChart": {
          "dataSets": [
            {
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "metric.type=\"run.googleapis.com/request_count\" resource.type=\"cloud_run_revision\" resource.label.\"service_name\"=\"nexova-api\"",
                  "aggregation": {
                    "perSeriesAligner": "ALIGN_RATE",
                    "crossSeriesReducer": "REDUCE_SUM",
                    "alignmentPeriod": "60s"
                  }
                }
              }
            }
          ]
        }
      },
      {
        "title": "Cloud Run Latency (99th Percentile)",
        "xyChart": {
          "dataSets": [
            {
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "metric.type=\"run.googleapis.com/request_latencies\" resource.type=\"cloud_run_revision\" resource.label.\"service_name\"=\"nexova-api\"",
                  "aggregation": {
                    "perSeriesAligner": "ALIGN_PERCENTILE_99",
                    "crossSeriesReducer": "REDUCE_NONE",
                    "alignmentPeriod": "60s"
                  }
                }
              }
            }
          ]
        }
      },
      {
        "title": "Firestore Document Read Ops",
        "xyChart": {
          "dataSets": [
            {
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "metric.type=\"firestore.googleapis.com/document/read_ops_count\" resource.type=\"firestore_instance\"",
                  "aggregation": {
                    "perSeriesAligner": "ALIGN_RATE",
                    "crossSeriesReducer": "REDUCE_SUM",
                    "alignmentPeriod": "60s"
                  }
                }
              }
            }
          ]
        }
      },
      {
        "title": "Firestore Document Write Ops",
        "xyChart": {
          "dataSets": [
            {
              "timeSeriesQuery": {
                "timeSeriesFilter": {
                  "filter": "metric.type=\"firestore.googleapis.com/document/write_ops_count\" resource.type=\"firestore_instance\"",
                  "aggregation": {
                    "perSeriesAligner": "ALIGN_RATE",
                    "crossSeriesReducer": "REDUCE_SUM",
                    "alignmentPeriod": "60s"
                  }
                }
              }
            }
          ]
        }
      }
    ]
  }
}
EOF
}
