#!/usr/bin/env pwsh
# Create all missing Shopify collections via CLI

$collections = @(
    @{
        title = "Corporate & Bulk Cake Orders Meerut"
        handle = "corporate-bulk-cakes-meerut"
        desc = "<h1>Corporate & Bulk Cake Orders in Meerut</h1><p>The Baking Kaur specializes in bulk and corporate cake orders for office celebrations, employee appreciation, team events, and corporate gifting across Meerut.</p><h2>Why Choose TBK for Corporate Orders?</h2><ul><li>✅ Bulk discounts on large orders</li><li>✅ Customization for team themes and branding</li><li>✅ Reliable same-day and next-day delivery</li><li>✅ Professional packaging and setup</li><li>✅ 4.8⭐ rated by corporate clients</li></ul><h2>Occasions & Services</h2><ul><li>Office birthday celebrations</li><li>Team milestone events</li><li>Employee appreciation cakes</li><li>Conference & event catering</li><li>Corporate gifting hampers</li><li>Annual celebration cakes</li></ul><h2>Bulk Order Benefits</h2><p>Order 5+ cakes and receive 10-15% bulk discount. Customizable designs, flavors, and packaging. Delivery coordination for multiple locations. Professional invoice and GST billing available.</p><h2>FAQ - Corporate Orders</h2><ul><li><strong>What's your minimum bulk order?</strong> Minimum 5 cakes for bulk pricing. Smaller orders welcome at regular pricing.</li><li><strong>Do you offer corporate discounts?</strong> Yes! 10-15% bulk discount on orders of 5+ cakes.</li><li><strong>Can you handle large office parties?</strong> Yes! We've catered events of 50+ people. Contact us for custom catering quotes.</li><li><strong>What about delivery coordination?</strong> We handle multi-location delivery and setup coordination. Discuss details when ordering.</li><li><strong>How long does a bulk order take?</strong> Bulk orders need 2-3 days lead time for optimal quality. Urgent orders discussed on a case-by-case basis.</li></ul>"
    },
    @{
        title = "Office Party Cakes Meerut"
        handle = "office-party-cakes-meerut"
        desc = "<h1>Office Party Cakes in Meerut</h1><p>Celebrate every office milestone with fresh, custom-designed cakes from The Baking Kaur. Perfect for team celebrations, birthday parties, work anniversaries, and corporate events.</p><h2>Why Choose TBK for Office Parties?</h2><ul><li>✅ Same-day and next-day delivery</li><li>✅ Bulk-friendly pricing</li><li>✅ Professional presentation</li><li>✅ Customizable themes and flavors</li><li>✅ Trusted by Meerut offices</li></ul><h2>Office Party Options</h2><ul><li>Team birthday cakes (single or multiple)</li><li>Office milestone celebration cakes</li><li>Professional thank-you cakes for clients</li><li>Conference and event catering</li><li>Work anniversary celebration cakes</li></ul><h2>FAQ - Office Party Cakes</h2><ul><li><strong>How many days notice do you need?</strong> Same-day and next-day available for single cakes. Bulk orders need 2-3 days notice.</li><li><strong>Can you coordinate delivery to office?</strong> Yes, we handle office delivery and setup coordination.</li><li><strong>Do you have a setup service?</strong> Yes, we offer setup and serving coordination for large office events.</li></ul>"
    },
    @{
        title = "Engagement & Proposal Cakes Meerut"
        handle = "engagement-proposal-cakes-meerut"
        desc = "<h1>Engagement & Proposal Cakes in Meerut</h1><p>Celebrate your engagement or proposal moment with a custom-designed, handcrafted cake from The Baking Kaur. Make the announcement sweeter with an engagement or proposal cake tailored to your love story.</p><h2>Why Choose TBK for Engagement Cakes?</h2><ul><li>✅ Custom designs for your special moment</li><li>✅ Same-day and midnight delivery available</li><li>✅ Romantic, elegant designs</li><li>✅ 4.8⭐ Trusted for milestone moments</li></ul><h2>Engagement Cake Options</h2><ul><li>Custom ring designs</li><li>Romantic floral arrangements</li><li>Couple-themed designs</li><li>Personalized message toppers</li><li>Multi-tier romantic cakes</li><li>Photo-enhanced designs</li></ul><h2>FAQ - Engagement & Proposal Cakes</h2><ul><li><strong>How much notice do you need?</strong> 2-3 days for custom designs. Urgent orders discussed on request.</li><li><strong>Can you add a hidden ring?</strong> Yes! We can safely hide a ring. Discuss safety details when ordering.</li><li><strong>Do you have romantic design ideas?</strong> Yes! Share your style or we'll suggest romantic designs matching your budget.</li></ul>"
    },
    @{
        title = "Vegan & Gluten-Free Cakes Meerut"
        handle = "vegan-gluten-free-cakes-meerut"
        desc = "<h1>Vegan & Gluten-Free Cakes in Meerut</h1><p>Celebrate dietary preferences without compromising on taste. The Baking Kaur offers premium vegan and gluten-free cakes for every occasion in Meerut.</p><h2>Why Choose TBK for Dietary Cakes?</h2><ul><li>✅ 100% Vegan (plant-based, no animal products)</li><li>✅ 100% Gluten-Free (safe for celiac)</li><li>✅ Premium taste, no compromise</li><li>✅ All designs available in dietary options</li><li>✅ Same-day and midnight delivery</li></ul><h2>Available Dietary Options</h2><ul><li>Vegan cakes (plant-based butter, almond milk, aquafaba)</li><li>Gluten-free cakes (certified gluten-free flour)</li><li>Vegan + Gluten-Free (fully inclusive)</li></ul><h2>FAQ - Vegan & Gluten-Free Cakes</h2><ul><li><strong>Are vegan cakes as delicious?</strong> Yes! Our vegan cakes use premium plant-based ingredients and taste identical to traditional cakes.</li><li><strong>Are gluten-free cakes safe for celiac?</strong> Yes, we use certified gluten-free flour and handle with care to avoid cross-contamination.</li><li><strong>Do both options cost more?</strong> Same pricing as regular cakes. Premium ingredients don't increase cost due to efficient sourcing.</li><li><strong>Can you combine vegan + gluten-free?</strong> Yes! Fully vegan and gluten-free cakes available for all occasions.</li></ul>"
    },
    @{
        title = "Surprise Cake Delivery Meerut"
        handle = "surprise-cake-delivery-meerut"
        desc = "<h1>Surprise Cake Delivery in Meerut</h1><p>Create an unforgettable moment with a surprise cake delivery from The Baking Kaur. Midnight deliveries, mystery cakes, and surprise setups for birthdays, anniversaries, and special occasions across Meerut.</p><h2>Why Choose TBK for Surprise Deliveries?</h2><ul><li>✅ Midnight surprise delivery (12 AM exactly)</li><li>✅ Mystery cake options</li><li>✅ Decorated surprise setups</li><li>✅ Coordinated with flowers and gifts</li><li>✅ Guaranteed freshness and on-time delivery</li></ul><h2>Surprise Cake Options</h2><ul><li>Midnight birthday surprise at 12 AM</li><li>Anniversary surprise delivery</li><li>Mystery cake (customer chooses flavor, we design)</li><li>Surprise setup with flowers and decorations</li><li>Engagement surprise cakes</li></ul><h2>FAQ - Surprise Cake Delivery</h2><ul><li><strong>How does midnight delivery work?</strong> You book in advance, we arrive at exactly 12 AM with a fresh cake.</li><li><strong>Can you coordinate with flowers?</strong> Yes! We can coordinate with local florists for combined surprise packages.</li><li><strong>How do I ensure it's a surprise?</strong> You provide recipient details, we coordinate separately with you for timing and location.</li><li><strong>What if the recipient isn't home?</strong> You arrange access or we wait briefly. Discuss contingency when ordering.</li></ul>"
    },
    @{
        title = "Cake Delivery Thapar Nagar Meerut"
        handle = "cake-delivery-thapar-nagar"
        desc = "<h1>Cake Delivery in Thapar Nagar, Meerut</h1><p>Same-day and midnight cake delivery right to your doorstep in Thapar Nagar. The Baking Kaur specializes in ultra-local delivery across all Thapar Nagar neighborhoods with guaranteed freshness.</p><h2>Why Choose TBK for Thapar Nagar?</h2><ul><li>✅ Fastest delivery in Thapar Nagar (30-45 minutes)</li><li>✅ Fresh-baked cakes for same-day orders</li><li>✅ Midnight delivery available</li><li>✅ All cake styles available</li><li>✅ Local expertise and service</li></ul><h2>Thapar Nagar Delivery Coverage</h2><p>We deliver across all Thapar Nagar areas including residential colonies, commercial areas, and multi-rise complexes. Order before 12 PM for same-day delivery by 5 PM.</p><h2>Order Process</h2><ul><li>Order online or via WhatsApp +91-821-886-2928</li><li>Confirm flavor, design, and delivery time</li><li>Fresh baking starts on order confirmation</li><li>Guaranteed delivery to your Thapar Nagar location</li></ul><h2>FAQ - Thapar Nagar Delivery</h2><ul><li><strong>What's the fastest delivery time?</strong> 30-45 minutes for same-day orders placed before 12 PM.</li><li><strong>Is midnight delivery available in Thapar Nagar?</strong> Yes! Book midnight slots in advance via WhatsApp.</li><li><strong>What's the minimum order?</strong> Minimum ₹350 for Thapar Nagar delivery.</li></ul>"
    }
)

Write-Host "🚀 Creating remaining collections...$n" -ForegroundColor Cyan

foreach ($collection in $collections) {
    Write-Host "Creating: $($collection.title)..." -ForegroundColor Yellow

    $graphql = @"
mutation {
  collectionCreate(input: {
    title: "$($collection.title)"
    handle: "$($collection.handle)"
    descriptionHtml: "$($collection.desc -replace '"', '\"')"
  }) {
    collection {
      id
      title
      handle
    }
    userErrors {
      field
      message
    }
  }
}
"@

    $graphqlPath = "$env:TEMP\collection_$($collection.handle).graphql"
    Set-Content -Path $graphqlPath -Value $graphql

    $result = & shopify store execute --store ae86ba-2a.myshopify.com --query-file $graphqlPath --allow-mutations --json 2>&1 | ConvertFrom-Json

    if ($result.collectionCreate.collection) {
        Write-Host "✅ Created: $($result.collectionCreate.collection.title)" -ForegroundColor Green
    } elseif ($result.collectionCreate.userErrors) {
        Write-Host "❌ Error: $($result.collectionCreate.userErrors[0].message)" -ForegroundColor Red
    }

    Remove-Item -Path $graphqlPath -Force
    Start-Sleep -Milliseconds 500
}

Write-Host "`n✅ Collection creation complete!" -ForegroundColor Green
