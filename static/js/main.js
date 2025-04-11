// Main JavaScript file for CivicPulse

document.addEventListener("DOMContentLoaded", () => {
  // Initialize all interactive elements
  initializeDropdowns()
  initializeMobileMenu()
  initializeTabSwitching()
  initializeFormSteps()
  setupMapInteraction()
  setupImageUpload()

  // Add current year to footer
  updateFooterYear()
})

// Initialize dropdown menus
function initializeDropdowns() {
  const dropdowns = document.querySelectorAll(".dropdown")

  dropdowns.forEach((dropdown) => {
    const trigger = dropdown.querySelector(".dropdown-trigger")
    const menu = dropdown.querySelector(".dropdown-menu")

    if (trigger && menu) {
      trigger.addEventListener("click", (e) => {
        e.preventDefault()
        e.stopPropagation()

        // Close all other dropdowns
        document.querySelectorAll(".dropdown-menu.active").forEach((activeMenu) => {
          if (activeMenu !== menu) {
            activeMenu.classList.remove("active")
          }
        })

        // Toggle this dropdown
        menu.classList.toggle("active")
      })
    }
  })

  // Close dropdowns when clicking outside
  document.addEventListener("click", () => {
    document.querySelectorAll(".dropdown-menu.active").forEach((menu) => {
      menu.classList.remove("active")
    })
  })
}

// Initialize mobile menu
function initializeMobileMenu() {
  const mobileMenuButton = document.querySelector(".mobile-menu-button")
  const mobileMenu = document.querySelector(".mobile-menu")

  if (mobileMenuButton && mobileMenu) {
    mobileMenuButton.addEventListener("click", () => {
      mobileMenu.classList.toggle("active")
      document.body.classList.toggle("menu-open")
    })
  }
}

// Initialize tab switching
function initializeTabSwitching() {
  const tabTriggers = document.querySelectorAll(".tabs-trigger")

  tabTriggers.forEach((trigger) => {
    trigger.addEventListener("click", () => {
      // Remove active class from all triggers and contents
      document.querySelectorAll(".tabs-trigger").forEach((t) => t.classList.remove("active"))
      document.querySelectorAll(".tabs-content").forEach((c) => c.classList.remove("active"))

      // Add active class to clicked trigger and corresponding content
      trigger.classList.add("active")
      const tabName = trigger.getAttribute("data-tab")
      const tabContent = document.querySelector(`.tabs-content[data-tab="${tabName}"]`)

      if (tabContent) {
        tabContent.classList.add("active")
      }
    })
  })
}

// Initialize multi-step forms
function initializeFormSteps() {
  const nextButtons = document.querySelectorAll('[id^="next-to-step-"]')
  const backButtons = document.querySelectorAll('[id^="back-to-step-"]')
  const progressBar = document.getElementById("progress-bar")

  nextButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const currentStep = Number.parseInt(button.id.split("-").pop())
      const nextStep = currentStep + 1
      goToStep(nextStep)
    })
  })

  backButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const targetStep = Number.parseInt(button.id.split("-").pop())
      goToStep(targetStep)
    })
  })

  function goToStep(step) {
    // Hide all steps
    document.querySelectorAll('[id^="step-"]').forEach((stepEl) => {
      stepEl.classList.add("hidden")
    })

    // Show target step
    const targetStep = document.getElementById(`step-${step}`)
    if (targetStep) {
      targetStep.classList.remove("hidden")
    }

    // Update step indicators
    updateStepIndicators(step)

    // Update progress bar if it exists
    if (progressBar) {
      progressBar.style.width = `${(step - 1) * 50}%`
    }
  }

  function updateStepIndicators(currentStep) {
    document.querySelectorAll('[id^="step-indicator-"]').forEach((indicator, index) => {
      const stepNum = index + 1

      if (stepNum <= currentStep) {
        indicator.classList.remove("bg-white", "border-gray-300", "text-gray-400")
        indicator.classList.add("bg-teal-600", "border-teal-600", "text-white")

        // Update step text
        if (indicator.nextElementSibling) {
          indicator.nextElementSibling.classList.remove("text-gray-400")
          indicator.nextElementSibling.classList.add("text-teal-600")
        }

        // If past this step, show checkmark
        if (stepNum < currentStep) {
          indicator.innerHTML = `
            <svg class="icon-xs" viewBox="0 0 24 24">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
          `
        } else {
          indicator.textContent = stepNum
        }
      } else {
        indicator.classList.remove("bg-teal-600", "border-teal-600", "text-white")
        indicator.classList.add("bg-white", "border-gray-300", "text-gray-400")

        // Update step text
        if (indicator.nextElementSibling) {
          indicator.nextElementSibling.classList.remove("text-teal-600")
          indicator.nextElementSibling.classList.add("text-gray-400")
        }

        indicator.textContent = stepNum
      }
    })
  }
}

// Setup map interaction for issue reporting
function setupMapInteraction() {
  const mapContainer = document.querySelector(".border.rounded-md.overflow-hidden")
  const mapMarker = document.getElementById("map-marker")
  const locationCoordinates = document.getElementById("location-coordinates")
  const locationMapInput = document.getElementById("location-map")

  if (mapContainer && mapMarker && locationCoordinates && locationMapInput) {
    mapContainer.addEventListener("click", (e) => {
      const rect = mapContainer.getBoundingClientRect()
      const x = e.clientX - rect.left
      const y = e.clientY - rect.top

      // Position the marker
      mapMarker.style.left = `${x}px`
      mapMarker.style.top = `${y}px`
      mapMarker.style.transform = "translate(-50%, -50%)"

      // Convert to fake coordinates (simplified for demo)
      const lat = 40.712 + (rect.height / 2 - y) * 0.0001
      const lng = -74.006 + (x - rect.width / 2) * 0.0001

      const locationText = `${lat.toFixed(6)}, ${lng.toFixed(6)}`
      locationCoordinates.textContent = `Selected location: ${locationText}`
      locationMapInput.value = locationText
    })
  }

  // Address verification
  const verifyAddressButton = document.getElementById("verify-address")
  if (verifyAddressButton) {
    verifyAddressButton.addEventListener("click", function () {
      const street = document.getElementById("street").value
      const city = document.getElementById("city").value
      const zip = document.getElementById("zip").value

      if (!street || !city || !zip) {
        showToast("Please fill in all address fields", "error")
        return
      }

      const fullAddress = `${street}, ${city}, ${zip}`
      const locationAddressInput = document.getElementById("location-address")
      if (locationAddressInput) {
        locationAddressInput.value = fullAddress
      }

      // Show success message
      this.innerHTML = `
        <svg class="icon-sm mr-2 text-green-600" viewBox="0 0 24 24">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
          <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
        Address Verified
      `
      this.classList.remove("btn-outline")
      this.classList.add("btn-primary")

      showToast("Address verified successfully", "success")
    })
  }
}

// Setup image upload functionality
function setupImageUpload() {
  const imageUpload = document.getElementById("image-upload")
  const imagePreviewContainer = document.getElementById("image-preview-container")
  const reviewImages = document.getElementById("review-images")

  if (imageUpload && imagePreviewContainer) {
    imageUpload.addEventListener("change", function () {
      if (this.files && this.files.length > 0) {
        // Clear existing previews if needed
        if (imagePreviewContainer) {
          imagePreviewContainer.innerHTML = ""
        }

        if (reviewImages) {
          reviewImages.innerHTML = ""
        }

        // Create previews
        Array.from(this.files)
          .slice(0, 4)
          .forEach((file, index) => {
            const reader = new FileReader()

            reader.onload = (e) => {
              // Create preview for upload section
              if (imagePreviewContainer) {
                const preview = document.createElement("div")
                preview.className = "aspect-square rounded-md overflow-hidden bg-gray-100 relative"
                preview.innerHTML = `<img src="${e.target.result}" alt="Uploaded image ${index + 1}" class="w-full h-full object-cover">`
                imagePreviewContainer.appendChild(preview)
              }

              // Create preview for review section
              if (reviewImages) {
                const reviewPreview = document.createElement("div")
                reviewPreview.className = "w-16 h-16 rounded overflow-hidden bg-gray-100"
                reviewPreview.innerHTML = `<img src="${e.target.result}" alt="Issue image ${index + 1}" class="w-full h-full object-cover">`
                reviewImages.appendChild(reviewPreview)
              }
            }

            reader.readAsDataURL(file)
          })
      }
    })
  }

  // Update review section when proceeding to step 3
  const nextToStep3Button = document.getElementById("next-to-step-3")
  if (nextToStep3Button) {
    nextToStep3Button.addEventListener("click", () => {
      updateReviewSection()
    })
  }

  function updateReviewSection() {
    const categoryEl = document.getElementById("category")
    const titleEl = document.getElementById("title")
    const descriptionEl = document.getElementById("description")
    const locationEl =
      document.querySelector(".tabs-content.active").getAttribute("data-tab") === "map"
        ? document.getElementById("location-map")
        : document.getElementById("location-address")
    const landmarkEl = document.getElementById("landmark")

    if (!categoryEl || !titleEl || !descriptionEl || !locationEl) {
      return
    }

    // Update review fields
    const reviewCategory = document.getElementById("review-category")
    const reviewTitle = document.getElementById("review-title")
    const reviewDescription = document.getElementById("review-description")
    const reviewLocationText = document.getElementById("review-location-text")

    if (reviewCategory) reviewCategory.textContent = categoryEl.value
    if (reviewTitle) reviewTitle.textContent = titleEl.value
    if (reviewDescription) reviewDescription.textContent = descriptionEl.value

    if (reviewLocationText) {
      const landmark = landmarkEl ? landmarkEl.value : ""
      const locationText = landmark ? `${locationEl.value}, near ${landmark}` : locationEl.value
      reviewLocationText.textContent = locationText
    }
  }
}

// Update footer year
function updateFooterYear() {
  const yearElements = document.querySelectorAll(".current-year")
  const currentYear = new Date().getFullYear()

  yearElements.forEach((element) => {
    element.textContent = currentYear
  })
}

// Show toast notification
function showToast(message, type = "info", duration = 5000) {
  let toastContainer = document.getElementById("toast-container")

  if (!toastContainer) {
    // Create toast container if it doesn't exist
    toastContainer = document.createElement("div")
    toastContainer.id = "toast-container"
    toastContainer.className = "toast-container"
    document.body.appendChild(toastContainer)
  }

  // Create toast element
  const toast = document.createElement("div")
  toast.className = `toast toast-${type}`

  // Get icon based on type
  let icon = ""
  switch (type) {
    case "success":
      icon =
        '<svg class="icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>'
      break
    case "error":
      icon =
        '<svg class="icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>'
      break
    case "warning":
      icon =
        '<svg class="icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>'
      break
    default:
      icon =
        '<svg class="icon-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>'
  }

  toast.innerHTML = `
    <div class="toast-icon">${icon}</div>
    <div class="toast-content">
      <p class="toast-message">${message}</p>
    </div>
    <button class="toast-close" onclick="this.parentElement.remove()">
      <svg class="icon-xs" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="18" y1="6" x2="6" y2="18"></line>
        <line x1="6" y1="6" x2="18" y2="18"></line>
      </svg>
    </button>
  `

  // Add toast to container
  toastContainer.appendChild(toast)

  // Remove toast after duration
  setTimeout(() => {
    toast.style.animation = "slideOut 0.3s forwards"
    setTimeout(() => {
      if (toast.parentElement) {
        toast.remove()
      }
    }, 300)
  }, duration)

  return toast
}

// Admin dashboard functions
function initializeAdminDashboard() {
  // Toggle dialog visibility
  window.viewComplaintDetail = (complaintId) => {
    fetch(`/admin/complaint/${complaintId}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          const complaint = data.complaint
          const dialog = document.getElementById("complaintDetailDialog")
          const title = document.getElementById("complaintDetailTitle")
          const content = document.getElementById("complaintDetailContent")

          // Set title with ID
          title.innerHTML = `
            ${complaint.title}
            <span class="text-sm text-gray-500">(${complaint.reference_id})</span>
          `

          // Generate complaint details HTML
          content.innerHTML = generateComplaintDetailHTML(complaint)

          // Store complaint ID for status updates
          document.getElementById("updateComplaintId").value = complaint.id

          // Show dialog
          dialog.classList.add("show")
        } else {
          showToast("Failed to load complaint details", "error")
        }
      })
      .catch((error) => {
        console.error("Error fetching complaint details:", error)
        showToast("Failed to load complaint details", "error")
      })
  }

  window.closeDialog = (dialogId) => {
    const dialog = document.getElementById(dialogId)
    if (dialog) {
      dialog.classList.remove("show")
    }
  }

  window.showUpdateStatusDialog = () => {
    const dialog = document.getElementById("updateStatusDialog")
    if (dialog) {
      dialog.classList.add("show")
    }
  }

  window.updateComplaintStatus = () => {
    const form = document.getElementById("updateStatusForm")
    const formData = new FormData(form)

    fetch("/admin/update_complaint", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          showToast("Complaint status updated successfully", "success")
          closeDialog("updateStatusDialog")
          closeDialog("complaintDetailDialog")

          // Refresh complaints list
          const department = document.getElementById("selectedDepartment").textContent
          fetchComplaints(department)
        } else {
          showToast("Failed to update complaint status", "error")
        }
      })
      .catch((error) => {
        console.error("Error updating complaint status:", error)
        showToast("Failed to update complaint status", "error")
      })
  }

  // Fetch complaints based on department filter
  window.fetchComplaints = (department) => {
    const searchTerm = document.getElementById("searchInput")?.value || ""

    fetch(`/api/complaints?department=${encodeURIComponent(department)}&search=${encodeURIComponent(searchTerm)}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          updateComplaintsTable(data.data)
        }
      })
      .catch((error) => {
        console.error("Error fetching complaints:", error)
        showToast("Failed to fetch complaints", "error")
      })
  }

  // Search complaints
  window.searchComplaints = () => {
    const department = document.getElementById("selectedDepartment")?.textContent || "All Departments"
    fetchComplaints(department)
  }

  // Helper functions for admin dashboard
  function generateComplaintDetailHTML(complaint) {
    const formattedDate = new Date(complaint.created_at).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    })

    return `
      <div class="mb-4">
        ${getStatusBadge(complaint.status)}
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div>
          <h4 class="font-medium text-gray-700 mb-2">Details</h4>
          <dl class="space-y-2">
            <div class="flex gap-2">
              <dt class="font-medium text-gray-500">Category:</dt>
              <dd>${complaint.category}</dd>
            </div>
            <div class="flex gap-2">
              <dt class="font-medium text-gray-500">Priority:</dt>
              <dd>${getPriorityBadge(complaint.priority)}</dd>
            </div>
            <div class="flex gap-2">
              <dt class="font-medium text-gray-500">Date Reported:</dt>
              <dd>${formattedDate}</dd>
            </div>
          </dl>
        </div>
        
        <div>
          <h4 class="font-medium text-gray-700 mb-2">Location</h4>
          <p class="text-sm">${complaint.location}</p>
          ${complaint.landmark ? `<p class="text-sm text-gray-500 mt-1">Near: ${complaint.landmark}</p>` : ""}
        </div>
      </div>
      
      <div class="mb-6">
        <h4 class="font-medium text-gray-700 mb-2">Description</h4>
        <p class="text-sm">${complaint.description}</p>
      </div>
      
      <div class="mb-6">
        <h4 class="font-medium text-gray-700 mb-2">Timeline</h4>
        <div class="border-l-2 border-gray-200 pl-4 space-y-4">
          ${complaint.updates
            .map((update) => {
              const updateDate = new Date(update.timestamp).toLocaleDateString("en-US", {
                year: "numeric",
                month: "short",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit",
              })

              return `
              <div class="relative">
                <div class="absolute -left-6 mt-1 w-2 h-2 rounded-full bg-${getStatusColor(update.status)}"></div>
                <div class="mb-1 flex items-center gap-2">
                  <span class="font-medium">${update.status}</span>
                  <span class="text-xs text-gray-500">${updateDate}</span>
                </div>
                <p class="text-sm">${update.message}</p>
              </div>
            `
            })
            .join("")}
        </div>
      </div>
      
      ${
        complaint.images && complaint.images.length > 0
          ? `
        <div>
          <h4 class="font-medium text-gray-700 mb-2">Images</h4>
          <div class="grid grid-cols-4 gap-2">
            ${complaint.images
              .map(
                (image) => `
              <div class="aspect-square rounded overflow-hidden bg-gray-100">
                <img src="${image}" alt="Issue image" class="w-full h-full object-cover">
              </div>
            `,
              )
              .join("")}
          </div>
        </div>
      `
          : ""
      }
    `
  }

  function updateComplaintsTable(complaints) {
    const tableBody = document.querySelector("#complaintsTable tbody")
    if (!tableBody) return

    tableBody.innerHTML = ""

    complaints.forEach((complaint) => {
      const row = document.createElement("tr")
      row.className = "table-row"

      row.innerHTML = `
        <td class="font-medium">${complaint.reference_id}</td>
        <td>${complaint.title}</td>
        <td>${complaint.category}</td>
        <td>${getStatusBadge(complaint.status)}</td>
        <td>${getPriorityBadge(complaint.priority)}</td>
        <td>${complaint.date}</td>
        <td class="text-right">
          <div class="flex justify-end gap-2">
            <button class="btn-ghost" onclick="viewComplaintDetail('${complaint.id}')">
              <svg class="icon-sm" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
            </button>
            <button class="btn-ghost">
              <svg class="icon-sm" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
            </button>
            <button class="btn-ghost">
              <svg class="icon-sm" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                <line x1="10" y1="11" x2="10" y2="17"></line>
                <line x1="14" y1="11" x2="14" y2="17"></line>
              </svg>
            </button>
          </div>
        </td>
      `

      tableBody.appendChild(row)
    })
  }
}

// Helper functions for status and priority badges
function getStatusBadge(status) {
  let color = ""
  let icon = ""

  switch (status) {
    case "New":
      color = "blue"
      icon = '<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path>'
      break
    case "Assigned":
      color = "orange"
      icon = '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle>'
      break
    case "In Progress":
      color = "purple"
      icon = '<circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>'
      break
    case "Resolved":
      color = "green"
      icon = '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>'
      break
    default:
      color = "gray"
      icon = '<circle cx="12" cy="12" r="10"></circle>'
  }

  return `
    <span class="badge badge-${status.toLowerCase().replace(" ", "-")}">
      <svg class="icon-xs mr-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        ${icon}
      </svg>
      ${status}
    </span>
  `
}

function getPriorityBadge(priority) {
  let color = ""

  switch (priority) {
    case "Low":
      color = "green"
      break
    case "Medium":
      color = "orange"
      break
    case "High":
      color = "red"
      break
    default:
      color = "gray"
  }

  return `<span class="badge badge-${priority.toLowerCase()}">${priority}</span>`
}

function getStatusColor(status) {
  switch (status) {
    case "New":
      return "blue-500"
    case "Assigned":
      return "orange-500"
    case "In Progress":
      return "purple-500"
    case "Resolved":
      return "green-500"
    default:
      return "gray-500"
  }
}

// Initialize admin dashboard if on admin page
if (document.querySelector(".admin-badge")) {
  document.addEventListener("DOMContentLoaded", () => {
    initializeAdminDashboard()
  })
}

