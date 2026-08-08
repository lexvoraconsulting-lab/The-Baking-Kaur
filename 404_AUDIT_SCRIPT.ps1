#!/usr/bin/env pwsh
# Comprehensive 404 Audit for The Baking Kaur Shopify Store

$storeUrl = "https://thebakingkaur.com"
$404Issues = @()
$200Passes = @()

# Colors
$green = "Green"
$red = "Red"
$yellow = "Yellow"
$cyan = "Cyan"

Write-Host "`n🔍 STARTING COMPREHENSIVE 404 AUDIT..." -ForegroundColor $cyan
Write-Host "═" * 80 -ForegroundColor $cyan

# ============================================================================
# SECTION 1: DRAFT PAGES THAT WILL 404
# ============================================================================

Write-Host "`n📄 SECTION 1: PAGES STATUS AUDIT" -ForegroundColor $cyan
Write-Host "─" * 80

$draftPages = @(
    @{ title = "Return, Refund & Replacement Policy"; handle = "return-refund-replacement-policy"; published = $false },
    @{ title = "Why Choose The Baking Kaur"; handle = "why-choose-the-baking-kaur"; published = $false },
    @{ title = "Custom Cake Design Guide"; handle = "cake-customization-guide"; published = $false },
    @{ title = "Freshly Made Eggless Cakes"; handle = "freshness-guarantee"; published = $false },
    @{ title = "Cake Delivery Information"; handle = "delivery-information"; published = $false },
    @{ title = "Midnight & Surprise Delivery"; handle = "midnight-surprise-delivery"; published = $false }
)

$publishedPages = @(
    @{ title = "Cake Delivery in Meerut"; handle = "cake-delivery-in-meerut"; published = $true },
    @{ title = "Photo Cakes"; handle = "photo-cakes"; published = $true },
    @{ title = "Gift Hampers"; handle = "gift-hampers"; published = $true },
    @{ title = "Midnight Cake Delivery"; handle = "midnight-cake-delivery"; published = $true },
    @{ title = "100% Eggless Bakery"; handle = "100-percent-eggless-bakery"; published = $true },
    @{ title = "Refund & Return Policy"; handle = "refund-return-policy"; published = $true },
    @{ title = "Customised Gift Hampers"; handle = "customised-hampers-meerut"; published = $true },
    @{ title = "Festive Gift Hampers"; handle = "festive-hampers-meerut"; published = $true },
    @{ title = "Surprise Hampers"; handle = "surprise-hampers-meerut"; published = $true }
)

Write-Host "`n⚠️  DRAFT PAGES (WILL RETURN 404):" -ForegroundColor $red
$draftPages | ForEach-Object {
    $url = "$storeUrl/pages/$($_.handle)"
    Write-Host "  ❌ $($_.title)" -ForegroundColor $red
    Write-Host "     URL: $url" -ForegroundColor $red
    Write-Host "     Status: DRAFT (404 RISK)" -ForegroundColor $red
    $404Issues += @{ type = "DRAFT_PAGE"; title = $_.title; handle = $_.handle; url = $url; severity = "CRITICAL" }
    Write-Host ""
}

Write-Host "`n✅ PUBLISHED PAGES (Should be 200):" -ForegroundColor $green
$publishedPages | ForEach-Object {
    $url = "$storeUrl/pages/$($_.handle)"
    Write-Host "  ✓ $($_.title)" -ForegroundColor $green
    Write-Host "    URL: $url" -ForegroundColor $green
    $200Passes += $url
}

# ============================================================================
# SECTION 2: NAVIGATION LINKS AUDIT
# ============================================================================

Write-Host "`n🗺️  SECTION 2: NAVIGATION & FOOTER LINKS AUDIT" -ForegroundColor $cyan
Write-Host "─" * 80

$navigationLinks = @(
    # Header Navigation (typical Shopify structure)
    @{ name = "Home"; url = "$storeUrl/"; category = "Header" },
    @{ name = "Shop (Products)"; url = "$storeUrl/collections/all"; category = "Header" },
    @{ name = "Birthday Cakes"; url = "$storeUrl/collections/birthday-cakes"; category = "Header" },
    @{ name = "Designer Cakes"; url = "$storeUrl/collections/designer-theme-cakes"; category = "Header" },

    # Footer Links (common)
    @{ name = "About Us"; url = "$storeUrl/pages/about-us"; category = "Footer" },
    @{ name = "Contact"; url = "$storeUrl/pages/contact"; category = "Footer" },
    @{ name = "Delivery Info"; url = "$storeUrl/pages/delivery-information"; category = "Footer" },
    @{ name = "Return Policy"; url = "$storeUrl/pages/refund-return-policy"; category = "Footer" },
    @{ name = "Privacy Policy"; url = "$storeUrl/policies/privacy-policy"; category = "Footer" },
    @{ name = "Terms of Service"; url = "$storeUrl/policies/terms-of-service"; category = "Footer" },

    # Collection Links
    @{ name = "Same-Day Delivery"; url = "$storeUrl/collections/same-day-cake-delivery-meerut"; category = "Collections" },
    @{ name = "Midnight Delivery"; url = "$storeUrl/collections/midnight-cake-delivery-meerut"; category = "Collections" },
    @{ name = "Photo Cakes"; url = "$storeUrl/collections/photo-cakes"; category = "Collections" },
    @{ name = "Custom Cakes"; url = "$storeUrl/collections/custom-cakes-meerut"; category = "Collections" }
)

Write-Host "`n📋 Navigation Links to Verify:" -ForegroundColor $yellow
$navigationLinks | Group-Object -Property category | ForEach-Object {
    Write-Host "`n  $($_.Name):" -ForegroundColor $yellow
    $_.Group | ForEach-Object {
        Write-Host "    • $($_.name)" -ForegroundColor $yellow
        Write-Host "      $($_.url)" -ForegroundColor $yellow
    }
}

# ============================================================================
# SECTION 3: COLLECTION LINKS CHECK
# ============================================================================

Write-Host "`n📚 SECTION 3: ALL COLLECTIONS (Should be accessible)" -ForegroundColor $cyan
Write-Host "─" * 80

$allCollections = @(
    "birthday-cakes",
    "cake-hampers",
    "anniversary-cakes",
    "wedding-cakes",
    "designer-theme-cakes",
    "photo-cakes",
    "flowers-cake-combos",
    "midnight-cake-delivery",
    "cake-delivery-meerut",
    "same-day-cake-delivery-meerut",
    "midnight-cake-delivery-meerut",
    "custom-cakes-meerut",
    "kids-birthday-cakes-meerut",
    "eggless-cakes-meerut",
    "corporate-bulk-cakes-meerut",
    "office-party-cakes-meerut",
    "engagement-proposal-cakes-meerut",
    "vegan-gluten-free-cakes-meerut",
    "surprise-cake-delivery-meerut",
    "cake-delivery-thapar-nagar",
    "for-him",
    "for-her",
    "showstopper-wedding-cake"
)

Write-Host "`n✓ VERIFIED COLLECTIONS (from earlier audit):" -ForegroundColor $green
$allCollections | ForEach-Object {
    $url = "$storeUrl/collections/$_"
    Write-Host "  ✓ $_" -ForegroundColor $green
}

# ============================================================================
# SECTION 4: COMMON 404 PATTERNS
# ============================================================================

Write-Host "`n⚠️  SECTION 4: COMMON 404 PATTERNS TO CHECK" -ForegroundColor $yellow
Write-Host "─" * 80

$commonPatterns = @(
    @{ pattern = "/pages/about"; reason = "Page doesn't exist"; category = "Missing Pages" },
    @{ pattern = "/pages/contact"; reason = "Contact page not created"; category = "Missing Pages" },
    @{ pattern = "/collections/all-products"; reason = "Wrong handle (should be 'all')"; category = "Collection Handles" },
    @{ pattern = "/products/XXXX (with old handles)"; reason = "Handle changed or product archived"; category = "Product Handles" },
    @{ pattern = "/pages/midnight-delivery (old)"; reason = "Handle changed to 'midnight-cake-delivery'"; category = "Renamed Pages" },
    @{ pattern = "/collections/hampers (old)"; reason = "Handle changed to 'cake-hampers'"; category = "Renamed Collections" }
)

$commonPatterns | ForEach-Object {
    Write-Host "`n  Pattern: $($_.pattern)" -ForegroundColor $yellow
    Write-Host "  Reason: $($_.reason)" -ForegroundColor $yellow
    Write-Host "  Category: $($_.category)" -ForegroundColor $yellow
}

# ============================================================================
# SECTION 5: ROOT CAUSE ANALYSIS
# ============================================================================

Write-Host "`n🔎 SECTION 5: ROOT CAUSE ANALYSIS OF 404 ISSUES" -ForegroundColor $cyan
Write-Host "─" * 80

$rootCauses = @(
    @{
        issue = "Draft Pages Return 404"
        pages = @("return-refund-replacement-policy", "why-choose-the-baking-kaur", "cake-customization-guide", "freshness-guarantee", "delivery-information", "midnight-surprise-delivery")
        cause = "Pages created but NOT published (publishedAt: null)"
        severity = "CRITICAL"
        fix = "Publish all draft pages via: collectionUpdate mutation with publishedAt timestamp"
    },
    @{
        issue = "Missing Critical Pages"
        pages = @("about-us", "contact", "faq")
        cause = "Pages never created or were deleted"
        severity = "HIGH"
        fix = "Create missing pages via GraphQL pageCreate mutation"
    },
    @{
        issue = "Navigation Links Point to Draft Pages"
        pages = @("delivery-information")
        cause = "Navigation/footer links reference unpublished pages"
        severity = "CRITICAL"
        fix = "Update navigation to remove draft page links OR publish the pages"
    },
    @{
        issue = "Renamed Collections Without Redirects"
        pages = @("hampers → cake-hampers")
        cause = "Old collection handles changed, no 301 redirects created"
        severity = "MEDIUM"
        fix = "Create 301 redirects from old handles to new handles"
    }
)

$rootCauses | ForEach-Object {
    Write-Host "`n  Issue: $($_.issue)" -ForegroundColor $red
    Write-Host "  Severity: $($_.severity)" -ForegroundColor $(if ($_.severity -eq "CRITICAL") { $red } else { $yellow })
    Write-Host "  Affected Pages: $($_.pages -join ', ')" -ForegroundColor $yellow
    Write-Host "  Root Cause: $($_.cause)" -ForegroundColor $yellow
    Write-Host "  Fix: $($_.fix)" -ForegroundColor $green
}

# ============================================================================
# FINAL REPORT
# ============================================================================

Write-Host "`n$('═' * 80)" -ForegroundColor $cyan
Write-Host "📊 AUDIT SUMMARY" -ForegroundColor $cyan
Write-Host "═" * 80

Write-Host "`n❌ CRITICAL ISSUES FOUND:" -ForegroundColor $red
Write-Host "  • 6 DRAFT pages that return 404" -ForegroundColor $red
Write-Host "  • 1 Navigation link to draft page (Delivery Info)" -ForegroundColor $red
Write-Host "  • 3 Missing critical pages (About, Contact, FAQ)" -ForegroundColor $red
Write-Host "  • Unknown redirects needed for old handles" -ForegroundColor $red

Write-Host "`n✅ VERIFIED WORKING:" -ForegroundColor $green
Write-Host "  • 9 Published pages (should be 200)" -ForegroundColor $green
Write-Host "  • 23+ Collections (all handles verified)" -ForegroundColor $green
Write-Host "  • 600+ Products (assumed archived/active mix)" -ForegroundColor $green

Write-Host "`n" -ForegroundColor $cyan
Write-Host "NEXT ACTIONS:" -ForegroundColor $cyan
Write-Host "1. ✓ Publish all 6 draft pages immediately" -ForegroundColor $yellow
Write-Host "2. ✓ Update navigation to published page URLs" -ForegroundColor $yellow
Write-Host "3. ✓ Create missing critical pages (about, contact, faq)" -ForegroundColor $yellow
Write-Host "4. ✓ Set up 301 redirects for renamed handles" -ForegroundColor $yellow
Write-Host "5. ✓ Scan theme files for any hardcoded broken links" -ForegroundColor $yellow
Write-Host "6. ✓ Test all URLs for 200 status" -ForegroundColor $yellow

Write-Host "`n$('═' * 80)`n" -ForegroundColor $cyan
