terraform {
  required_providers {
    google = {
        source = "hashicorp/google"
    }
  }
}
provider "google" {
  credentials = file("TODO")

  project     = "beacon"
  region      = "us-east4"
  zone        = "us-east4-c"
}

resource "google_compute_instance" "grass-vm" {
  name = "beacon"
  machine_type = "e2-small"
  zone        = "us-east4-c"

  boot_disk {
    auto_delete = true
    device_name = "grass-vm-disk"
    initialize_params {
      image = "projects/ubuntu-os-cloud/global/images/ubuntu-2204-jammy-v20240614"
      size = 10
      type = "pd-balanced"
    }
    mode = "READ_WRITE"
  }
  
  can_ip_forward      = false
  deletion_protection = false
  enable_display      = false

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }

  network_interface {
    access_config {
      network_tier = "STANDARD"
    }

    queue_count = 0
    stack_type  = "IPV4_ONLY"
    subnetwork  = "projects/upc-space-program/regions/us-east4/subnetworks/default"
  }
  tags = ["http-server", "https-server"]

}